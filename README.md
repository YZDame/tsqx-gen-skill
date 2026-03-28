# TSQX Gen Skill

A Codex skill for turning geometry problem statements, figure descriptions, or images into clean TSQX code.

This repository packages a reusable skill with:

- a triggerable [SKILL.md](./SKILL.md)
- style references distilled from local TSQX usage
- a small extracted dataset from Evan Chen handouts
- helper scripts for local `tsqx -> asy -> pdf` verification

## What This Skill Does

Use this skill when you want Codex to:

- convert a geometry problem statement into TSQX
- reconstruct a figure from diagram text or an image
- normalize output format across multiple problems
- keep track of assumptions instead of hiding diagram guesses
- optionally verify the generated TSQX with local tools

## Repository Structure

```text
tsqx-gen-skill/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
  testdata/
```

- `SKILL.md`: the skill definition and workflow
- `agents/openai.yaml`: Codex UI metadata
- `references/`: style guides, output contract, few-shot patterns
- `scripts/`: dataset extraction and local compile helpers
- `testdata/`: extracted Evan-handout TSQX cases and manifest

## Installation

Clone or copy this repository into your Codex skills directory.

Typical path:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cd "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/YZDame/tsqx-gen-skill.git
```

After that, Codex can invoke the skill by name:

```text
Use $tsqx-gen to turn this geometry problem into TSQX.
```

## Local Validation

This repository includes a small verifier for the local toolchain.

Example:

```bash
python3 scripts/verify_tsqx_pipeline.py \
  /path/to/example.tsqx \
  --pre \
  --output-dir /tmp/tsqx-skill-check
```

This runs:

1. `tsqx -p`
2. `asy -f pdf`

and writes generated artifacts to the chosen output directory.

## Evan Handout Dataset

The repository includes an extracted dataset from:

- `/Users/leyudame/Downloads/web.evanchen.cc-main/handouts`

The preserved TSQX subset is intentionally small but high-quality. See:

- [testdata/evan-handouts/README.md](./testdata/evan-handouts/README.md)
- [references/evan-style.md](./references/evan-style.md)

## Dependencies

For full local verification, install:

- `tsqx`
- `asy`
- `python3`

The skill itself remains useful even without local compilation.

## License

[MIT](LICENSE)
