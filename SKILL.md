---
name: tsqx-gen
description: Generate TSQX geometry code from Chinese or English problem statements, diagram descriptions, or provided images; use when the user wants a fast, repeatable workflow from natural language or figure content to valid TSQX, including batch generation, normalization, ambiguity handling, and optional compile-check against local tsqx and asymptote toolchains.
---

# TSQX Generator

Use this skill when the task is to convert a geometry problem into TSQX source, especially when the input is:

- a text-only problem statement
- a rough figure description
- an existing diagram image that needs to be reconstructed
- a batch of similar problems that should be normalized to one output style

This skill is for **TSQX generation**, not for explaining TSQX syntax in the abstract.

## Goal

Produce TSQX that is:

- geometrically faithful to the problem
- structurally clean and reusable
- consistent across multiple problems
- ready for `tsqx -> asy -> pdf` verification when local tools are available

## Inputs

Accept any of these:

- full problem statement
- partial problem statement plus figure notes
- image only
- image plus text
- a batch list of problems

If an image is provided, inspect the visible geometry first and only infer missing facts when the diagram strongly suggests them. Clearly label inferences.

## Output Contract

Default output should contain these sections in order:

1. `Assumptions`
2. `Geometry Parse`
3. `TSQX`
4. `Checks`
5. `Open Questions`

If the user explicitly wants only code, return only the `TSQX` section.

Read [references/output-contract.md](references/output-contract.md) for the exact section format.
Read [references/idioms.md](references/idioms.md) when choosing constructions and TSQX phrasing.
Read [references/few-shot.md](references/few-shot.md) when the task resembles a known geometry pattern.
Read [references/evan-style.md](references/evan-style.md) for concise TSQX style anchored by preserved handout examples from Evan Chen.

## Core Workflow

1. Parse the problem into atomic geometry facts.
2. Separate **stated facts** from **diagram-only guesses**.
3. Decide the construction order:
   - base points
   - derived points
   - supporting objects
   - highlight or annotation objects
4. Choose coordinates or symbolic constructions that preserve the intended constraints with minimal complexity.
5. Write TSQX in a normalized style.
6. If local verification is feasible, compile through the TSQX toolchain and fix obvious breakage.
7. Report unresolved ambiguity instead of hiding it in code.

Use [references/geometry-checklist.md](references/geometry-checklist.md) as the parsing checklist.

## Normalization Rules

- Prefer simple, robust constructions over overfitted coordinates.
- Keep a stable naming scheme from the problem statement unless it is internally inconsistent.
- Do not encode unstated equalities, perpendicularities, or cyclic relations unless they are explicit or visually unavoidable.
- When a diagram is not metrically reliable, preserve incidence and relative position first.
- Use auxiliary constructions only when they materially improve faithfulness or readability.
- Prefer standard TSQX built-ins over raw injected Asymptote whenever the geometry is already expressible in TSQX.
- Keep code compact, but not cryptic.

## Ambiguity Policy

When the source is underspecified:

- provide the best faithful version
- list every nontrivial inference in `Assumptions`
- list blocking uncertainties in `Open Questions`

Do not pretend the source determines more than it does.

## Batch Mode

For multiple problems:

- normalize naming and style across all outputs
- keep the same section layout for each problem
- flag which items were fully determined and which required inference
- if asked for machine-friendly output, emit one fenced `tsqx` block per problem with a short identifier

## Local Verification

When local tools are available, prefer this pipeline:

```bash
tsqx -p < input.tsqx > output.asy
asy output.asy
```

If a local TSQX source repository is available, inspect its `examples` or personal corpus for idiomatic patterns before inventing syntax from scratch.

In the author's current workspace, useful references include:

- a `tsqx` repository containing language source, examples, and Chinese reference material
- a `tsqx-compiler` repository containing compile/preview workflow and diagnostics behavior

Treat those repositories as optional context, not required dependencies of this skill.
Use `scripts/verify_tsqx_pipeline.py` for quick local validation when you have written a `.tsqx` file to disk.

If compilation fails:

- fix syntax or construction issues when the intent is still clear
- otherwise keep the best draft and explain the blocker in `Checks`

## Image-Driven Tasks

For image-based reconstruction:

1. identify named points, lines, circles, and marked relations
2. distinguish printed labels from visual decoration
3. recover the likely incidence graph before writing code
4. only then choose coordinates or constructions

If the image contains text, reconcile the text with the drawing. Prefer explicit text over approximate visual proportions.

## When To Escalate Beyond This Skill

This skill is enough for:

- one-off TSQX generation
- repeated TSQX generation in the same session
- small batch conversions
- consistent output formatting

Consider a plugin or MCP only if the user needs one of these:

- a persistent custom UI, commands, or one-click workflow inside Codex or VS Code
- a service that ingests folders or datasets and runs unattended conversions
- external model orchestration, OCR, or dataset-backed retrieval
- queueing, job state, caching, or multi-stage pipelines across many sessions

Until those are required, keep the system as a skill.
