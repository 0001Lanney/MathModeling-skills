---
name: solution-package-builder
description: Assemble a submission-ready writer package from final method, result, robustness, figure, and human-decision artifacts, then freeze approved numerical claims with provenance.
---

# Purpose

Create the writer's single source package and immutable numerical snapshot. Do not manufacture missing judgments or freeze unapproved claims.

# Preconditions

- `rigor_profile` is `submission`.
- Final method explanation, final result analysis, robustness report, and figure plan exist.
- Human method, result, stability, and claim-scope decisions exist in `qx_decisions.jsonl`.
- Canonical sources are current.

# Evidence and Sequencing

- Reconcile original task/source, supported parse and parent manifest mappings, actual current code plan and genuine content-linked confirmation. Check Required Main Model, Required Baseline, Required Validation Experiments, and authorized Non-required Exploratory Methods against real code, execution records, metrics/units, outputs, and acceptance findings. No probe PASS, code existence, fitting result, or method-level success substitutes for required validation.
- Missing source coverage is COVERAGE_UNVERIFIABLE; missing required results/validation or unverifiable plan approval blocks dependent claims/freeze, not independent evidence preparation. Report exact task/item, source, absent/conflicting evidence, owner, and re-entry requirement through Orchestrator. Do not alter task scope or requiredness to finish a package.
- Preserve the original order: collect and draft the solution package, obtain a real package_signoff decision, then generate frozen_numbers.json. Do not require already passed G4 or a pre-existing freeze to perform the steps that create them; G4 final completion still needs all original artifacts. User keep/downgrade/drop changes claim scope only within genuine authority, not the truth of underlying results.
- Verify actual human sign-off against this package's content/version and evidence, including effective supersession. Fallback replacement additionally needs real trigger plus specific human authorization and an updated confirmed plan; do not switch methods, invent authorization, or use a new digest as retrospective approval.
- Keep successful, failed, partial, rerun, Warning and NOT RUN evidence traceable. A Warning alone is not failure; optional exploration failure alone need not veto satisfied required work, but material effects on selection/comparison/claims require disclosure and may block unsupported claims.
- Preserve Exempt requirements as Exempt with actual scoped human decision and limitation disclosure, never Completed or automatic G6. Missing data or runtime is not exemption. Do not freeze unexecuted/inconclusive/failed validation as a successful scientific claim, fabricate numerical values, or hide contradictory results.
- Use existing solution-package/freeze paths, JSON entry meanings and fields without extending Schema, statuses, ledger or Manifest. Cite genuine canonical sources and stable locators. Downstream Writer, Completeness, Consistency and QA retain their roles; report gaps for Orchestrator rather than repairing others' evidence or approving G6.

# Workflow

1. Collect final method structure, result claims, limitations, figures, tables, and decision provenance.
2. Draft `results/Qx/reports/qx_solution_package_for_writer.md`.
3. Flag every proposed top-line claim with:
   - value and unit;
   - canonical source path and location;
   - robustness support;
   - decision ID for claim scope or rationale;
   - confidence/limitation.
4. Invoke one final choice card when package sign-off is missing:
   - keep;
   - downgrade;
   - drop.
5. Route the human answer to `modeler-decision-logger` as `package_signoff`.
6. Only after sign-off, generate `results/Qx/reports/frozen_numbers.json`.
7. Verify every numerical package claim resolves to the freeze and every judgment claim resolves to a human decision ID.

# Frozen Number Contract

Each entry contains:

```json
{
  "claim_id": "q1_main_rmse",
  "value": 2.4,
  "unit": "units",
  "source_file": "results/Q1/experiments/final/metrics/main.json",
  "source_locator": "$.rmse",
  "frozen_at": "ISO-8601",
  "frozen_by_skill": "solution-package-builder",
  "decision_id": "q1_package_signoff"
}
```

Use a source line only for stable text files; use a JSON path, table key, or row/column identifier for structured data.

# Rules

- Do not create `solution-package-builder_modeler_decision.md`.
- Do not emit `frozen_numbers.json` before human package sign-off.
- Never edit an existing freeze by hand.
- Transcribe human rationales; do not re-compose them as stronger claims.
- The package may cite the compact method-card history but must not depend on a separate iteration log.
- Do not copy raw exploratory outputs into the package without final validation.

# Change and Re-freeze

When a canonical source changes after freeze:

1. append the reason to `freeze_change_log.md`;
2. update and rerun the canonical source;
3. obtain renewed human judgment when the evidence changed materially;
4. regenerate the freeze;
5. run scoped consistency for Qx.

# Verification

- All prerequisites are final and current.
- Package sign-off exists in the JSONL ledger.
- Every frozen value has a real canonical source and stable locator.
- Every package number matches the freeze.
- Every modeling judgment traces to a human decision.
- Writer can use the package without searching scattered results.
