"""Dependency-free tests for the TSQX -> Asymptote verifier.

External compilers are stubbed so that failure paths are deterministic.
The real toolchain remains a separate smoke-test concern.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_tsqx_pipeline.py"
SPEC = importlib.util.spec_from_file_location("tsqx_verifier", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class VerifyPipelineTests(unittest.TestCase):
    def run_case(self, *, asy_pdf: bytes | None = b"%PDF-1.4\nexample", tsqx_text: str = "pair A = (0,0);\n", existing: bytes | None = None):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = directory / "example.tsqx"
            source.write_text("A = dir 110\n", encoding="utf-8")
            destination = directory / "out"
            destination.mkdir()
            final_pdf = destination / "example.pdf"
            if existing is not None:
                final_pdf.write_bytes(existing)
            observed_commands = []

            def fake_run(cmd, stdin_path=None):
                observed_commands.append(cmd)
                if cmd[0] == "python3":
                    self.assertEqual(cmd[:3], ["python3", "-m", "tsqx"])
                    self.assertEqual(stdin_path, source)
                    return subprocess.CompletedProcess(cmd, 0, tsqx_text, "")
                if cmd[0] == "asy":
                    self.assertIn("-f", cmd)
                    if asy_pdf is not None:
                        pdf_base = Path(cmd[cmd.index("-o") + 1])
                        pdf_base.with_suffix(".pdf").write_bytes(asy_pdf)
                    return subprocess.CompletedProcess(cmd, 0, "", "")
                self.fail(f"Unexpected executable: {cmd}")

            argv = [
                "verify_tsqx_pipeline.py",
                str(source),
                "--output-dir", str(destination),
                "--tsqx-cmd", "python3 -m tsqx",
                "--pre",
            ]
            with (
                patch.object(sys, "argv", argv),
                patch.object(verifier, "run", side_effect=fake_run),
                patch.object(verifier.shutil, "which", return_value="/fake/executable"),
            ):
                status = verifier.main()

            result_pdf = final_pdf.read_bytes() if final_pdf.exists() else None
            result_asy = (destination / "example.asy").read_text() if (destination / "example.asy").exists() else None
            # Staging artifacts must be removed after both success and failure.
            self.assertEqual(list(destination.glob(".example-verify-*")), [])
            return status, result_pdf, result_asy, observed_commands

    def test_success_with_quoted_command_components(self):
        status, pdf, asy, cmds = self.run_case()
        self.assertEqual(status, 0)
        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertIn("pair A", asy)
        self.assertIn("-p", cmds[0])

    def test_missing_pdf_does_not_replace_previous_output(self):
        status, pdf, asy, _ = self.run_case(asy_pdf=None, existing=b"old PDF")
        self.assertEqual(status, 1)
        self.assertEqual(pdf, b"old PDF")
        self.assertIsNone(asy)

    def test_empty_asy_is_failure(self):
        status, pdf, asy, cmds = self.run_case(tsqx_text="", existing=b"old PDF")
        self.assertEqual(status, 1)
        self.assertEqual(pdf, b"old PDF")
        self.assertIsNone(asy)
        self.assertEqual(len(cmds), 1)

    def test_pdf_must_have_valid_header(self):
        status, pdf, asy, _ = self.run_case(asy_pdf=b"not a PDF")
        self.assertEqual(status, 1)
        self.assertIsNone(pdf)
        self.assertIsNone(asy)


if __name__ == "__main__":
    unittest.main()
