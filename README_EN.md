# 3D Structure Review Skill

Language: [English](README_EN.md) · [简体中文](README.md)

A reusable Codex Skill for reviewing STEP/STP files and native CAD assemblies against product requirements. It guides structural and pre-tooling checks, injection-molding risk analysis, and the creation of traceable reports and issue-closure lists. Stress simulation and finished-product reliability analysis are included only when requested for the current task.

## What it covers

- Trace input versions and requirements to specific parts, interfaces, and checks.
- Open the actual model in a local CAD application; verify units, assembly hierarchy, placements, and solid validity.
- Check nominal interferences, clearances, local wall thickness, and relevant sections using CAD geometry.
- Identify potential molding risks around thick or thin areas, ribs, bosses, draft, and overmolding, with the evidence needed to close each issue.
- When in scope, plan or perform simulation and reliability work with explicit material, load, boundary-condition, and test assumptions.
- Deliver an editable review report supported by locations, measurements, independent checks, and a follow-up list.

The Skill supplies a review process and evidence rules. It does not supply a material grade, tool design, load case, or solver. A local geometry measurement is not a mold-flow result or a physical product test.

## Install

Place the whole repository in the Codex skills directory:

```bash
git clone https://github.com/SvenKunkka/3d-structure-review.git
mkdir -p ~/.codex/skills
cp -R 3d-structure-review ~/.codex/skills/
```

If a skill with the same name is already installed, inspect and back it up before replacing it. The entry point is [`SKILL.md`](SKILL.md). Invoke it explicitly with `$3d-structure-review`; [`agents/openai.yaml`](agents/openai.yaml) provides the display name and allows automatic discovery.

Example request:

> Use $3d-structure-review to review this STEP assembly against the product requirements in my local CAD software. For this round, focus on structural and injection-molding risks. Deliver an editable report, a PDF, and an issue-closure list.

The Skill instructions and detailed reference modules are currently written in Chinese. The review scope and requested report language can be set in the task prompt.

## Repository layout

| Path | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Scope selection, review sequence, independent verification, and delivery rules |
| [`references/`](references/) | Guides for native CAD, structure and assembly, injection molding, simulation and reliability, and report delivery |
| [`scripts/source_guard.py`](scripts/source_guard.py) | Standard-library tool for recording and checking input-file SHA-256 hashes without changing those files |

Example input baseline check:

```bash
python3 scripts/source_guard.py snapshot --manifest review/evidence/input_manifest.json --files model.stp requirements.xlsx
python3 scripts/source_guard.py verify --manifest review/evidence/input_manifest.json
```

This tool only checks whether file bytes have changed. CAD import, geometry measurements, figures, and report validation follow the instructions in the Skill.

## Provenance and limits

This Skill was distilled from a real structural and injection-molding review. It does not contain that product's CAD files, requirements, face IDs, measurements, or private reports. Findings for a new project must be verified against that project's current inputs.

Licensed under [MIT](LICENSE).
