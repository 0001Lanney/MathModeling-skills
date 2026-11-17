---
name: model-code-analyzer
description: Prepare language-neutral modeling code plans covering the human-selected main method, usable baseline, required validation experiments, and authorized exploration. Verify plan scope and evidence, obtain explicit human confirmation before execution release, and hand off to Python or MATLAB generators.
---

# Purpose

Define exactly what code must implement and save. Do not expand the approved experiment scope or fully plan a dormant fallback.

# Preconditions

- `methods/Qx/qx_method_card.md` and probe summary exist.
- `methods/Qx/qx_decisions.jsonl` contains a human `DECIDED` method choice.
- A usable baseline is identified.
- Cleaned data and `data_profile.json` are ready when data is required.
- Implementation target and round are known.

Read legacy candidate/decision artifacts only when the new artifacts are absent.

## Authorization Sources and Responsibilities

- Read the actual Qx method-choice record from `methods/Qx/qx_decisions.jsonl`; replace both Qx and the qx filename component with the real question identifier. Verify its actual `decision_id`, `decision_type`, `status`, `decided_by`, `choice`, evidence, and applicable supersession or revocation.
- Read `planning/framing_decisions.jsonl` only if it exists and is relevant to a global or pre-Qx decision. If no relevant decision depends on an uncreated ledger, its absence alone is not an error.
- If relied-on authorization is missing, unreadable, untraceable, conflicting, or revoked, report that authorization cannot be verified; do not assume either that authorization never occurred or that it is valid.
- This Skill must not create or modify either designated ledger, use an undesignated alternative authorization ledger, or manufacture missing fields, timestamps, decision types, references, or human wording. Qx and global authorization do not substitute for each other.
- `method-selector` proposes candidates, baseline, validation suggestions, and risk probes. The human chooses methods. This Skill prepares the code plan and proposed required-method list; the human confirms them. `modeler-decision-logger` faithfully records actual decisions under its existing contract, while `workflow-orchestrator` schedules subsequent work.
- G2.5 method selection is not confirmation of the complete code plan or its required-method list. Permission to continue is not approval of every method or experiment.

## First Plan, Revision, and Execution Release

- For the first candidate code plan, verify the genuine G2.5 method choice, method card, probes, required inputs, parameters, baseline comparability, and budget. Do not require prior approval of a plan that does not yet exist.
- Generate the complete candidate plan and four-category list for human review. State `pending_confirmation` in the Markdown plan or Handoff; this is a document description, not a JSON enum, Schema field, Gate, or ledger status. Missing confirmation of this first candidate alone is not `BLOCKING_ERROR`.
- Present the actual plan and its revision for explicit human confirmation. Request faithful recording by `modeler-decision-logger` through the Handoff for orchestrator scheduling; do not write the ledger or approve the plan yourself.
- Before relying on an existing confirmation, read the actual current plan and the historical content the decision approved. Verify the plan path, `plan_revision` or another reliable revision reference, task IDs, four-category list, requiredness, substantive conditions, and actual decision evidence.
- Compute SHA-256 for the actual plan content, or resolve a reliable immutable revision reference to exact historical content. A newly computed SHA-256, identical version label, or mutable path alone does not prove historical human approval. Require a genuine recorded digest, immutable reference, or other verifiable evidence linking the decision to exactly what the human approved; do not backfill historical evidence.
- Read real existing ledger fields and references, including `choice`, `decision_type`, `status`, `decided_by`, `decision_id`, `evidence_refs`, and applicable `supersedes`. Task IDs, approval wording, plan revision, and content identity must be traceable through those real records and referenced evidence; do not assume dedicated optional fields or introduce unauthorized decision types. The proposed `code_plan_confirmation` type may be relied upon only after its contract has been separately approved and formally deployed in `modeler-decision-logger`; before deployment, preserve genuine confirmation evidence through the existing Handoff and report the unresolved recording interface without treating method choice as full-plan confirmation.
- A revision changing methods, categories, requiredness, task scope, validation conditions, or another substantive constraint requires a new explicit human decision covering the updated plan and a traceable supersession relationship. Preserve prior decisions and failure evidence. Analyzer may draft the revised candidate while approval is pending, but must not release it as approved.
- Release a plan for Generator execution only after explicit confirmation is verifiably linked to its current content, revision, full four-category list, and scope, with relevant supersession and revocation checked. Until then, hand off only for human review, never for execution, and never derive overall success from an unconfirmed list.
- Report affected `BLOCKING_ERROR` when required G2.5 choice cannot be verified; a relied-on authorization is unreadable, materially conflicting, or revoked; required inputs, parameters, or baseline comparability prevent a credible plan; or an action would release an unconfirmed plan or bypass a decision, requiredness, or supersession.
- Do not label normal waiting for first-plan approval as an authorization failure. Missing runtime alone need not prevent a credible plan when execution conditions can be specified truthfully; unresolved execution prerequisites must remain explicit and must not become fabricated execution results.

# Workflow

1. Read the approved choice, method card, probe conditions, and experiment budget.
2. Plan only within the genuine human-selected method scope and applicable task requirements:
   - the selected `main`, proposed as Required Main Model;
   - the selected `usable_baseline`, proposed as Required Baseline;
   - task-applicable Required Validation Experiments, with proposed requiredness explicitly submitted for confirmation;
   - explicitly authorized Non-required Exploratory Methods, or an empty category when none are authorized;
   - shared helpers and comparison logic.
   Do not add candidate methods or exploration to fill categories. These are proposed plan classifications until the human confirms the complete list under Preconditions.
3. Record the fallback ID and trigger, but do not plan its full implementation unless the trigger is already evidenced and the human chose activation.
4. Map mathematical definitions to inputs, processing steps, intermediate evidence, outputs, and validation checks.
5. Define a directly comparable metric/output contract for main and baseline.
6. Define the round output:

```text
results/Qx/experiments/roundN/
├── figures/
├── tables/
├── metrics/
└── run_summary.json
```

Create `logs/` only for failures, warnings, or reproducibility needs.
7. Write `code/Qx/qx_code_plan.md` for Python or `code/matlab/Qx/qx_code_plan.md` for MATLAB.
8. Present the complete candidate plan and revision for human review. Hand off to the matching language generator only after the execution-release checks in Preconditions pass; otherwise report pending confirmation or the actual blocking finding through Handoff.

## Task Coverage and Fallback Authorization

- Use the original problem as the final coverage authority, the existing problem_parse as the working task list, and manifests only as execution-state records. Map each planned method or validation to original `task_id`, `source_reference`, existing `manifest_entry`, expected `result_artifacts`, and planned `paper_section` response in the Markdown code plan; mark planned evidence as expected, not produced.
- If source or parse material is missing or incomplete, report `COVERAGE_UNVERIFIABLE` and the affected task, source, manifest link, result evidence, paper response, and missing material. Do not assume existing Qx entries define all original tasks or invent a source reference. Request parser/orchestrator follow-up through Handoff without modifying their artifacts.
- A risk-probe PASS is feasibility evidence, not completion of formal validation. Transfer relevant probe conditions into the code plan without substituting them for the required validation design.
- A fallback may replace a confirmed required method only when its trigger is evidenced and an explicit human decision authorizes that specific activation or replacement, identifying the affected method and applicable plan scope.
- Before execution release, require the updated plan, matching new confirmation, and traceable supersession using existing ledger records; preserve the original method's failed attempts, Warning text, and evidence. Trigger evidence alone does not activate a replacement.
- Before plan approval, assess candidate suitability using genuine probe evidence without overriding the human's method choice. After confirmation, do not downgrade, remove, or substitute a required method or validation because of complexity, cost, runtime, or failure. An unapproved fallback remains dormant.

# Run Summary Contract

Require:

```json
{
  "schema_version": 1,
  "question": "Q1",
  "round": "round1",
  "implementation_target": "python",
  "random_seed": 2026,
  "approved_decision_id": "q1_method_choice",
  "methods": [
    {
      "method_id": "M1",
      "role": "usable_baseline",
      "script": "code/Q1/q1_baseline.py",
      "status": "success",
      "execution_time_seconds": 0,
      "input_files": [],
      "output_files": [],
      "figure_files": [],
      "metrics_summary": {},
      "warnings": [],
      "errors": []
    }
  ],
  "comparison": {},
  "fallback_trigger": {
    "fallback_id": null,
    "condition": null,
    "observed": false,
    "evidence": null
  },
  "environment": {}
}
```

## Method-Level Execution and Identity Contract

- Keep the existing JSON field hierarchy, the example above and integer `schema_version: 1`; do not add JSON fields, a Schema, a state file or top-level aggregation fields. New method-level `role` is exactly one of `main`, `usable_baseline`, `validation`, `exploratory`; `status` is exactly lowercase `success` or `failed`. These are run-summary meanings, not Method Card roles or Reviewer check enums; do not accept aliases such as `OK` from the packager's `GOOD` set.
- Bind each confirmed plan's `method_id` or `validation_id`, unchanged, to the existing `methods[].method_id`. Use a single unique ID namespace within that complete plan; a validation record has role `validation`, not a disguised baseline. Verify each record against the current confirmed inventory in both directions. A missing required validation remains missing even when all recorded items show success. Shared scripts do not merge independent validation identities or prove their execution.
- Obtain requiredness only from the actual complete human-confirmed Markdown plan. Do not derive it from the run role, complexity, runtime, cost or failure. Retain authorized exploratory records and failures; an exploratory failure is not automatically required-work or G6 failure.
- `success` means the identified target computation actually executed and completed successfully, not that validation acceptance criteria passed. `failed` requires that the target computation actually began and failed, with attributable real execution evidence and a compatible nonempty `errors` array. A launched interpreter or nonzero launcher exit alone does not prove model execution; an unrecoverable computation error is not erased by a wrapper returning zero.
- New method-level `errors` is an array of genuine error-text strings; preserve verbatim native error text, saved exception evidence or an actual recorded termination/exit message with only necessary JSON escaping. Empty `errors` is not proof of execution or success. Retain actual return-code/stderr/log/exception provenance through existing execution artifacts, plan evidence references and Handoff, without adding JSON fields. Never invent an error message, traceback, cause, exit code or evidence path. If real failure is known but compatible errors are not yet formed, preserve the native evidence and block canonical publication until the responsible producer truthfully structures it.
- Non-execution, a program that never started, unknown execution state and insufficient evidence must not be encoded as `success` or `failed`. Do not add `not_run`, `NOT RUN` or `BLOCKING_ERROR` to JSON status. Report the actual NOT RUN or evidence gap through existing Handoff and withhold incompatible canonical publication; a Warning alone does not establish executed failure.
- An executed validation can have `status: success` while failing or not conclusively satisfying its confirmed acceptance criteria. Preserve actual metrics/observable outputs and the separate review finding; required acceptance failure or missing evidence blocks a required-work success claim. Do not invent a validation-failure status or overwrite the execution fact.
- List only actual input files and actually produced output/figure files in the existing arrays, retaining failed attempts' partial outputs and relevant Warning text/associations. Planned outputs are not actual files. Do not add production `failures` fields; retain any existing historical failures/errors and report unknown or unresolved meanings without deleting them or treating falsey values as proof of correct types.
- Read historical summaries without rewriting fields, forcing a version, normalizing unknown aliases or backfilling approval. No-version methods-level historical compatibility is unproven and remains a compatibility gap, not automatically an illegal experimental state. Missing legacy top-level fields are not a contradiction; existing top-level success cannot erase method failure, and top-level failure or incompatible file lists cannot be silently dropped.

## Truthful Records and Compatible Publication

- Keep the JSON example above, `schema_version: 1`, and the existing field hierarchy. The example is a contract illustration, not evidence of an executed experiment. Do not add JSON fields, any roles or status values beyond the Method-Level Execution and Identity Contract, Schema changes, or a new state file.
- Plan real execution records for all four categories using only representations actually supported by the applicable existing contract. Retain method/validation identity, actual scripts, input selection, configuration, execution timing, output paths, metrics or observable outputs, Warning text, errors, and evidence locators through existing compatible records and references.
- Use only the defined `validation` or `exploratory` role for the corresponding confirmed work; do not invent other roles or disguise an item under an unrelated identity. If existing fields cannot truthfully represent a category, state, or evidence relationship, report the interface gap rather than silently dropping it.
- Distinguish actual execution, execution failure, work not executed, evidence availability, validation findings, and workflow blocks. `NOT RUN` and uppercase `FAILED` are report facts, not JSON status values; lowercase `failed` has only the real-execution meaning defined in the Method-Level Execution and Identity Contract. `BLOCKING_ERROR` belongs only in Handoff or the blocking report, never in a JSON status field.
- If the contract cannot legally express NOT RUN or another actual fact, do not generate or publish incompatible canonical `run_summary.json`, invent SUCCESS or FAILED, add `not_run`, or omit the item. Preserve genuine evidence and report the actual state, reason, affected items, the interface gap, and `BLOCKING_ERROR` in Handoff; use NOT RUN only for work not executed. Resume formal publication only after explicit interface resolution.
- Preserve actual failures, relevant Warning wording, associated item IDs, errors, available logs, partial outputs, and evidence paths for required and non-required work. A Warning alone does not prove failure; assess actual state, errors, and impact. Never delete failed exploration, failed attempts, or rerun history to manufacture success.
- Empty `errors` does not establish execution or success. A top-level success, if present in a historical summary, cannot erase method-level failure; a method-level success cannot establish all required work succeeded. Unknown, illegal, or irreconcilable statuses require an affected blocking report, not a successful default.
- Keep execution success separate from satisfying validation criteria. Preserve unexecuted work and inconclusive or failed validation without fabricating metrics, thresholds, outputs, or theoretical conclusions.
- Preserve historical fields and structure when reading old summaries; do not silently discard information, force upgrades, repurpose the method-choice decision field as plan confirmation, or rewrite original experiment results. Missing and conflicting evidence must remain explicit.
- Keep plan-confirmation provenance and content identity in existing Markdown plan/Handoff and ledger references, not new run-summary fields. The deployed restricted packager reads Legacy summaries and supported schema_version: 1 methods[] file views, maps method_id/validation_id to current-plan records, and checks output_files together with figure_files. This does not establish genuine authorization, execution, per-item scientific acceptance, or C2 qualification; existing evidence/compatibility blocks remain, and C2_UNQUALIFIED disables all assembly, publication, and replacement. Do not modify package_submission.py or add top-level aggregation fields here.

# Code Plan Contents

- target language and round purpose;
- approved decision ID;
- main and baseline IDs and roles;
- input fields and units;
- per-method computation steps;
- comparable outputs and metrics;
- risk-probe conditions that implementation must monitor;
- fallback trigger evaluation;
- paths, seed, dependencies, and expected runtime;
- named review checks expected downstream.

## Four-Category Inventory and Acceptance

The following are Markdown code-plan content definitions, not additions to JSON Schema, ledger structure, summary roles, or status enums.

| Plan category | Required designation and scope |
| --- | --- |
| Required Main Model | Required; the human-selected main method, with its scientific meaning unchanged. |
| Required Baseline | Required; a usable, directly comparable baseline, never diagnostic_reference. |
| Required Validation Experiments | Required when explicitly confirmed; each has its own design and acceptance criteria. |
| Non-required Exploratory Methods | Non-required; only explicitly authorized exploration, with failures retained. An empty category is valid. |

- For every method or experiment record in the Markdown plan, provide `method_id` or `validation_id`, `role` as a plan category, `task_id` or task IDs, required/non-required designation, `objective`, `input_files`, `data_requirements`, `output_files`, `expected_outputs`, `success_criteria`, `execution_conditions`, `failure_impact`, and `evidence_artifacts`.
- For each validation experiment, additionally provide `validation_id`, `task_id`, `validation_target`, `applicability` and its reason, independent `design`, `data_requirements`, `metrics` or observable outputs, `success_criteria` including failure or inconclusive findings, `execution_conditions`, `failure_impact`, and `evidence_artifacts`.
- Identify the plan's `plan_revision` or reliable revision reference, actual `decision_id` references when available, and `confirmation_status` in Markdown. Before confirmation, say pending_confirmation and do not invent a decision ID; retain the distinct G2.5 method-choice reference.
- Specify shared input fields, units, data selection, script or function entry, seed, dependencies, runtime limits, paths, comparisons, execution order, and named downstream review checks. Keep the smallest clear arrangement; independent validation design need not mean a separate script per experiment.
- Define reproducible data splits, missingness masks, time windows, perturbations, or generated-input procedures when applicable. Synthetic input is permitted only within the confirmed plan's explicit purpose and conditions, never as a substitute for missing real results.
- Distinguish plan prepared, human confirmed, code generated, actually executed, traceable valid evidence obtained, and validation criteria satisfied. None of these facts substitutes for another. Required failure, NOT RUN, or unverifiable validation prevents an overall required-work success claim.
- Validation completion requires actual execution records, actual metrics or substantive outputs, traceable input data and executed scripts, and a finding against confirmed criteria. A plan, existing code, anticipated result, or successful main-model run is not proof of validation completion; unexecuted validation is NOT RUN in the report.
- Transfer every authorized exploratory failure and its effects on selection, comparison, conclusions, and credibility to result-report-generator for material-package and paper disclosure. Material effects require body experiment-analysis or limitations disclosure; immaterial exploration may be disclosed in appendix or experiment records. Do not portray failed exploration as successful.

## Deterministic Markdown Plan Representation

Use this fixed representation in newly prepared code plans, retaining all original Code Plan Contents, mathematical meaning, task/source/manifest/result/paper mapping, comparisons, probe risks, fallback, dependencies and review instructions. It is Markdown content, not a JSON plan file, new JSON enum or general Markdown AST. Never reformat an already approved plan to make it parseable; report an unsupported representation and submit any revised complete candidate for genuine confirmation.

1. Use exactly one plan title `# Code Plan Contents`, one `## Plan Identity` table, one `## Four-Category Inventory and Acceptance` category table with one `### Work Items` table, and one `## Required Validation Experiments` table. These authoritative tables must be outside code fences, with exact case-sensitive headings, column order and a standard `| --- |` separator cell per column. Preserve non-table scientific explanation; conflicts between it, source scope and the tables require clarification, not a count-based override.
2. Plan Identity has headers `key | value` and exactly one row each for `question`, `implementation_target`, `round`, `round_purpose`, `plan_revision`, `decision_id`, `confirmation_status`, `random_seed`, `dependencies`, `expected_runtime`, `review_checks`. Keys are JSON strings. Values are nonempty strings except `random_seed` (an actual integer, not bool) and `dependencies`/`review_checks` (unique nonempty-string arrays). `decision_id` preserves G2.5 method choice, not a future confirmation ID. Do not fabricate unavailable scope or version evidence.
3. The category table headers are `category | applicability | item_ids | reason`. Provide the four categories in the order Required Main Model, Required Baseline, Required Validation Experiments, Non-required Exploratory Methods. Category/applicability/reason are nonempty JSON strings; item_ids is an array of unique nonempty strings. Main and baseline are `applicable` with nonempty ID lists. Required validation is `applicable` with IDs or genuinely `not_applicable` with `[]` and a reason confirmed with the whole plan. Exploration is `applicable` with IDs or `none_authorized` with `[]` and a reason. Non-execution is not inapplicability; an unknown required validation list is not an empty list.
4. Work Items headers are `method_id | validation_id | role | requiredness | task_ids | objective | script | input_files | data_requirements | output_files | expected_outputs | success_criteria | execution_conditions | failure_impact | evidence_artifacts`. Method rows have nonempty method_id and null validation_id; validation rows have null method_id and nonempty validation_id. The non-null original string is the unified execution ID. IDs are unique across both namespaces, without renaming, prefix guessing or case folding. `role` is the full plan-category name; `requiredness` is explicitly `required` for the three required categories and `non-required` for authorized exploration. Verify both explicit values and approval rather than deriving requiredness from role.
5. The validation table headers are `validation_id | validation_target | applicability | applicability_reason | design | data_requirements | metrics | success_criteria | execution_conditions | failure_impact | evidence_artifacts`. Each included validation has `applicability: applicable`, its independent design/metrics, and exactly one Work Items match. Category item_ids and Work Items must match in both directions; required-validation IDs must also match the validation table. Duplicated information must agree exactly. Reject missing or additional IDs, fields, tables, columns, rows or keys, duplicate IDs, unknown applicability and ambiguous parsing; do not deduplicate or silently repair.
6. Each physical data cell is exactly one single-line JSON literal, split on raw `|` before one JSON decode; headers and separators are literal Markdown. Every row starts/ends with `|` and has the exact column count. Multiple task IDs and paths use arrays, never comma/semicolon splitting. In work/validation tables, task_ids/input_files/data_requirements/output_files/expected_outputs/execution_conditions/evidence_artifacts and validation design/metrics are unique nonempty-string arrays; the other non-identity cells are nonempty strings. Preserve array order. task_ids, required validation design/metrics, acceptance criteria and evidence cannot be omitted or disguised as empty values. Empty input_files requires a real no-external-file design with explicit data/generation conditions; an empty output_files requires a documented absence of separate file outputs and nonempty traceable evidence_artifacts. Work-item evidence_artifacts cannot be empty.
7. `[]` means explicitly zero items, not missing/unknown. Only the mutually exclusive identity slot may be null. Reject blank cells, empty strings, textual N/A or "null" as null substitutes, objects, trailing commas, NaN/Infinity, comments and multiple encoding layers. Encode an internal pipe as JSON `\u007C`, backslash as `\\`, quote as `\"`, and descriptive newlines as `\n`; do not use a bare internal pipe, Markdown `\|` or physical multi-line rows. Do not apply a second JSON, Markdown, HTML or URL decode. Paths/IDs cannot contain control characters; paths are workspace-relative POSIX with no drive, absolute root, backslash, empty segment, `.`/`..` or resolved escape. Treat ordinary descriptive special characters as text, never commands.
8. Candidate outputs may be expected paths that do not yet exist; label them planned and do not claim execution. At actual execution/review, require real scripts, inputs, metrics/outputs and acceptance evidence for every required item. Shared scripts still need independent validation ID/design and traceable execution evidence; no forced separate-script quota.
9. Preserve the full approved file's exact bytes, including prose, line endings and final newline, for content identity. Do not put a self-hash into the plan. Initial `pending_confirmation` describes preparation and may remain in the exact approved text; effective permission comes only from a genuine Ledger confirmation linked to that content. Never edit a confirmed plan just to backfill an approval state/ID. Substantive revisions need fresh confirmation and traceable supersession; first-plan drafting does not require nonexistent prior confirmation.

## Task-Appropriate Validation Design

Choose validation according to original requirements, method assumptions, available data, and the claims the paper would support. Record applicability and reasons; do not mechanically require every test for every task, invent acceptance thresholds, or add experiments to meet a quota. Proposed requiredness still requires human confirmation.

| Validation layer | Plan content |
| --- | --- |
| Mathematical theory | Formulas, derivations, assumptions, theorem conditions, and limits of any claimed proof. |
| Numerical and implementation | Numerical stability, boundary conditions, invariants, implementation correctness, and comparison with checkable references when applicable. |
| Experimental | Backtests, controls, independent tests, and generalization supporting the actual claim. |
| Uncertainty | Applicable parameter intervals, resampling, confidence intervals, and propagation into conclusions. |

- Interpolation: consider backtests using contiguous missing blocks and random missingness, matching the real missingness pattern and avoiding hidden use of held-out values.
- Prediction: distinguish in-sample fit, rolling validation, and independent testing; specify temporal cutoffs and leakage controls. Training fit metrics are not independent predictive validation.
- Optimization: check constraint feasibility, objective evaluation, boundary conditions, and applicable optimality or comparison evidence; an optimizer exit flag alone is insufficient.
- Evaluation or ranking: assess indicator definitions, weight sensitivity, and ranking stability where they support the claims.
- Dynamics and differential equations: plan applicable equilibria, stability, initial/boundary conditions, numerical checks, and parameter sensitivity.
- Machine learning: specify data splits, leakage prevention, usable baseline, and generalization evaluation consistent with the actual data structure.
- Parameter estimation: assess identifiability and whether uncertainty analysis is needed; one parameter perturbation is not a complete uncertainty analysis.
- AI self-derivation or self-review is not independent mathematical proof. Distinguish derivation checks, numerical agreement, experimental support, and independent proof; do not fabricate any of them.

# Rules

- Do not write executable model code.
- Do not add candidates or change model meaning.
- Do not plan a diagnostic reference as the official baseline.
- Do not implement a fallback before activation.
- Do not require success logs.
- Do not create a README when the code plan already provides the same instructions.
- Stop if a human choice, required parameter, input field, or comparable baseline output is missing.

# Verification

- Plan scope retains the selected main and usable baseline and explicitly accounts for required validation and authorized exploration in the four-category list. Fallback implementation planning requires the evidenced trigger and specific human activation; execution release also requires matching plan confirmation.
- Outputs are directly comparable.
- Probe risks and fallback trigger are represented in `run_summary.json`.
- Paths follow the experiment contract.
- Handoff targets the correct language generator.

- First-plan drafting is not blocked solely by the absence of confirmation for a not-yet-approved plan; pending_confirmation is explicit and execution release remains prohibited.
- Historical approval is linked to actual plan content, revision, tasks, requiredness, and applicable supersession; a newly computed hash alone is insufficient.
- Every validation has an applicable design, data conditions, observable criteria, failure impact, and planned evidence path, without implying it already ran or passed.
- Existing summary fields, hierarchy, JSON example and schema_version: 1 remain unchanged; use only the defined method-level role/status meanings. Unsupported facts lead to truthful Handoff and blocked publication rather than fabricated compatibility.
- Verify preserved failures, Warning associations, original outputs, disclosure needs, and the distinction between probe evidence, actual execution, and validation findings.

# Handoff

- For human review, provide the full candidate plan, its actual revision/content identity, task mapping, four-category list, validation design, existing method-choice evidence, unresolved questions, and pending_confirmation. Request an explicit decision about that exact plan; do not imply Generator execution is authorized.
- For confirmed execution, provide the actual plan path and content identity, verified confirmation references, relevant historical content and supersession, confirmed four-category list, data contracts, output paths, validation criteria, and execution prerequisites for the matching Python/MATLAB generator.
- Preserve code-reviewer as the next technical-review responsibility after generation and execution. Provide named review checks through the plan; do not replace technical review with result reporting.
- For result-report-generator, require the Generator handoff to retain actual success, failure, NOT RUN, exploratory effects, Warning/error evidence, partial outputs, and artifact provenance; do not invent results or draft unsupported final claims.
- For BLOCKING_ERROR, identify the blocked operation, affected task/method/validation IDs, actual missing or conflicting evidence, impact, suggested responsible party, and corrective evidence required. Distinguish a plan-drafting block, an execution-release block, and a future summary-publication interface gap.
- Report all handoffs for workflow-orchestrator scheduling. Do not directly invoke other Skills, change their state, modify manifest or Gate status, write a decision ledger, execute model code, or resolve the packaging interface here.
