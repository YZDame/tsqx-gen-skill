#!/usr/bin/env python3
"""
Compile a TSQX file through the local tsqx -> asy pipeline.

This script is intentionally small and deterministic so the skill can reuse it
across sessions without re-deriving shell commands.
"""

from __future__ import annotations

import argparse
import shutil
import shlex
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def run(cmd: list[str], stdin_path: Path | None = None) -> subprocess.CompletedProcess[str]:
    if stdin_path is None:
        return subprocess.run(cmd, text=True, capture_output=True, check=False)
    with stdin_path.open("r", encoding="utf-8") as fh:
        return subprocess.run(cmd, stdin=fh, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a TSQX file with local tools.")
    parser.add_argument("input", help="Path to the .tsqx file")
    parser.add_argument("--tsqx-cmd", default="python3 -m tsqx", help="Command used to run tsqx")
    parser.add_argument("--asy-cmd", default="asy", help="Command used to run Asymptote")
    parser.add_argument(
        "--output-dir",
        help="Directory for generated .asy/.pdf files; defaults to the input file directory",
    )
    parser.add_argument("--no-pdf", action="store_true", help="Stop after generating .asy")
    parser.add_argument("--pre", action="store_true", help="Pass -p/--pre to tsqx")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"[ERROR] Input not found: {input_path}", file=sys.stderr)
        return 1

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else input_path.parent
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    out_asy = output_dir / f"{input_path.stem}.asy"
    out_pdf = output_dir / f"{input_path.stem}.pdf"

    # shlex handles quoted command arguments without launching a shell.
    try:
        tsqx_cmd = shlex.split(args.tsqx_cmd)
        asy_cmd = shlex.split(args.asy_cmd)
    except ValueError as error:
        print(f"[ERROR] Invalid command argument: {error}", file=sys.stderr)
        return 1

    if not tsqx_cmd or shutil.which(tsqx_cmd[0]) is None:
        print(f"[ERROR] tsqx command not found: {args.tsqx_cmd}", file=sys.stderr)
        return 1
    if not args.no_pdf and (not asy_cmd or shutil.which(asy_cmd[0]) is None):
        print(f"[ERROR] asy command not found: {args.asy_cmd}", file=sys.stderr)
        return 1

    # Stage outputs away from the public paths: failed/partial runs must
    # never be mistaken for a successfully verified previous PDF.
    with TemporaryDirectory(prefix=f".{input_path.stem}-verify-", dir=output_dir) as workdir:
        staging = Path(workdir)
        staged_asy = staging / f"{input_path.stem}.asy"
        staged_pdf = staging / f"{input_path.stem}.pdf"

        tsqx_full = [*tsqx_cmd]
        if args.pre:
            tsqx_full.append("-p")
        tsqx_result = run(tsqx_full, stdin_path=input_path)
        if tsqx_result.returncode != 0:
            print("[ERROR] tsqx step failed", file=sys.stderr)
            if tsqx_result.stderr.strip():
                print(tsqx_result.stderr.strip(), file=sys.stderr)
            return tsqx_result.returncode

        if not tsqx_result.stdout.strip():
            print("[ERROR] tsqx reported success but generated empty ASY", file=sys.stderr)
            return 1
        staged_asy.write_text(tsqx_result.stdout, encoding="utf-8")

        if not args.no_pdf:
            asy_full = [*asy_cmd, "-f", "pdf", "-o", str(staged_pdf.with_suffix("")), str(staged_asy)]
            asy_result = run(asy_full)
            if asy_result.returncode != 0:
                print("[ERROR] asy step failed", file=sys.stderr)
                if asy_result.stderr.strip():
                    print(asy_result.stderr.strip(), file=sys.stderr)
                return asy_result.returncode
            if not staged_pdf.is_file() or staged_pdf.stat().st_size == 0:
                print("[ERROR] asy reported success but did not produce a nonempty PDF", file=sys.stderr)
                return 1
            with staged_pdf.open("rb") as stream:
                if stream.read(5) != b"%PDF-":
                    print("[ERROR] generated file is not a PDF", file=sys.stderr)
                    return 1

        staged_asy.replace(out_asy)
        print(f"[OK] Generated ASY: {out_asy}")
        if not args.no_pdf:
            staged_pdf.replace(out_pdf)
            print(f"[OK] Generated PDF: {out_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
