---
name: paper-section-writer
description: Draft submission-ready mathematical-modeling paper sections from the approved solution package, frozen numbers, human decision ledger, and verified figures without searching scattered exploratory outputs or inventing interpretation.
---

# Preconditions

- `rigor_profile` is `submission`.
- Final method explanation exists.
- Final result analysis exists.
- Solution package and current frozen numbers exist.
- Required human claim-scope and physical/domain-meaning decisions are recorded.

If any prerequisite is missing, return to its producer rather than drafting around the gap.

# Primary Sources

Use, in order:

1. `qx_solution_package_for_writer.md`
2. `frozen_numbers.json`
3. `qx_decisions.jsonl`
4. verified paper figures/tables
5. final method explanation and robustness report for clarification

Do not hunt through raw experiment folders to invent a narrative.

# Workflow

1. Resolve the requested section and contest format.
2. Build a claim map:
   - claim ID;
   - frozen value/source;
   - robustness support;
   - human decision ID;
   - figure/table reference;
   - limitation.
3. Draft the method description to match the final explanation and code.
4. Draft results with:
   - value and comparison;
   - human-confirmed physical/domain meaning;
   - uncertainty or robustness;
   - limitation and applicable scope.
5. Mention the baseline and eliminated alternatives only when they explain a real decision.
6. Use only Type 2–4 figures as appropriate; never place Type 1 diagnostics in the paper.
7. Save `paper/sections/qx.tex` or the requested Markdown section.

# Human-Owned Content

The AI must not originate:

- why the method was chosen;
- what the headline number means physically;
- confidence and claim scope;
- contribution framing.

Transcribe these from the decision ledger with provenance. If absent, invoke a compact choice card and stop the final draft until answered; do not fill the paper with repeated sentinels.

# Original-Task Answers and Evidence

- Maintain visibility of the complete original-task coverage map, but write substantive answers only for the original tasks and claims assigned to the requested section. Use real source/task IDs, supported parse/parent manifest mapping, the confirmed plan, genuine results, and the writer package. Do not infer complete task scope from existing Qx files, invent missing requirements, treat a section heading as an answer, or claim whole-paper coverage from one section. Report missing, conflicting, or unassigned task-to-section mappings through Handoff for Orchestrator and final coverage auditors; when source identity or required scope is unreliable, report COVERAGE_UNVERIFIABLE and request clarification rather than silently omitting or reallocating tasks.
- Preserve every original Preconditions requirement and the solution-package-first source order. Numerical claims use current frozen values/units/locators, methods match the approved explanation and actual confirmed plan, and human interpretation/claim scope stays human-owned. If any prerequisite required for the requested final section is missing or unverifiable, follow the original return-to-producer rule and do not deliver that section as final or draft around the gap. Independent preparatory source checks, coverage mapping, and missing-evidence Handoff may continue where reliable, but must be clearly separated from approved final section content. Do not infer evidence from scattered exploratory outputs.
- Distinguish Required Main Model, Required Baseline, Required Validation Experiments, and authorized exploration in the actual current plan. G2.5 choice is not full-plan approval; rely on genuine decision references linked to actual content/revision, not a newly computed digest or generic continuation.
- Describe a validation as completed only with implemented and actually executed design, traceable input/script/logs, real metrics/outputs, and satisfied criteria. Fit is not independent prediction validation; risk probes are not formal tests; sensitivity is not automatically uncertainty. Do not turn planned/code-only/NOT RUN/failed/inconclusive work into successful paper experiments.
- Retain limitations, failed methods, relevant original Warnings, reruns and partial outcomes in the evidence chain. Material exploratory failure affecting choices/comparisons/conclusions belongs in experiment analysis/limitations; immaterial exploration may be disclosed in appendix/records. Do not add unsupported numbers, stronger scientific meaning, or successful labels to failed attempts.
- Keep genuine scoped Exempt original requirements visible with reason, authority and limitations. Exempt is not Completed and does not certify complete original-task coverage or G6. Conditional requires the agreed delivery actually met and limits disclosed; unmet key requirements remain Partial/Incomplete. Do not grant exemptions or change requiredness.
- R5: check placeholders/fragments, missing task responses, abstract/body parameter/metric/conclusion agreement, formulas/numbering/references and required deliverables. R6: use actual verified figure files and real result origins with consistent units/axes/captions/references; file presence alone does not prove correctness. Request required DOCX/PDF post-export evidence rather than claiming checks not performed.
- This Skill writes approved evidence-backed sections; it does not run missing experiments, create a new ledger/Schema/Gate, change frozen values or manifest states, or replace final auditors. Report exact affected claims, missing evidence, repair owner and safe independent work through Handoff for Orchestrator scheduling.

# Rules

- Every numerical claim must match `frozen_numbers.json`.
- Do not overclaim against untested methods or populations.
- Do not fabricate citations or causal meaning.
- Avoid procedural diary prose and ceremonial detail.
- Keep formulas, symbols, units, captions, and filenames consistent.
- Do not create a new decision artifact.

# Verification

- Three writer prerequisites pass.
- Claim map resolves all numbers and judgments.
- Method, results, and figures match canonical artifacts.
- Physical meaning and contribution are human-owned.
- Limitations and uncertainty are visible.
- No Type 1 figure appears.
