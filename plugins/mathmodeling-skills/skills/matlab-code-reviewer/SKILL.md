---
name: matlab-code-reviewer
description: Review, run, debug, and verify approved MATLAB or Beita Tianyuan modeling code against its plan, data contract, method decision, compatibility constraints, and experiment outputs, saving one compact JSON review.
---

# Preconditions

- MATLAB code and `code/matlab/Qx/qx_code_plan.md` exist.
- Approved method decision, method card, and data profile are available when applicable; inspect the relevant run summary when one has truthfully been produced. An absent run summary must be reported with its actual reason and must not prevent authorized static inspection or truthful NOT_RUN reporting.
- MATLAB or 北太天元 runtime availability is known.

## Confirmed Plan and Authorization

- Read the actual `code/matlab/Qx/qx_code_plan.md`, relevant `methods/Qx/qx_decisions.jsonl`, method card, probe evidence, data profile, and current run summary. Replace Qx and the qx filename component with the real question and filename.
- Read `planning/framing_decisions.jsonl` only if it exists and is relevant to a genuine global or pre-Qx decision. An irrelevant absent ledger is not an error; if relied-on authorization cannot be read or verified, report the missing evidence without assuming either approval or that authorization never occurred.
- Link the current plan's exact content and revision to the actual historical human confirmation using a genuinely recorded digest, immutable revision reference, or other traceable evidence. A newly computed SHA-256, version label, or mutable path alone does not prove past approval.
- Verify actual task IDs, four-category identities, requiredness, scope, execution conditions, and the real decision's choice, decision_type, status, decided_by, evidence references, and supersession or revocation. Do not invent optional fields, decision types, approval wording, or retrospective digests.
- G2.5 method choice is not confirmation of the current complete code plan; permission to continue or approval of a substantively different plan is insufficient. Code generation, actual execution, and validation success are separate facts.
- If current-plan approval is missing, unverifiable, conflicting, or revoked, report BLOCKING_ERROR in Handoff and stop affected execution, repairs, and final approval. Safe authorized static inspection may continue, but cannot be reported as a passing execution review.
- This Skill must not create or modify either designated ledger, use an undesignated authorization ledger, change manifests or Gates, modify another Skill, or approve a plan on the user's behalf. The decision logger records genuine human decisions; workflow-orchestrator schedules subsequent work.
- Read actual current upstream contracts rather than assuming an old Analyzer is present. Resolve any observed contract mismatch through Handoff without editing upstream Skills; Python Reviewer is a shared-review reference, not evidence of MATLAB's original capabilities or runtime behavior.

# Workflow

1. Resolve approved main/baseline scope and any activated fallback.
   - Reconcile Required Main Model, Required Baseline, Required Validation Experiments, and Non-required Exploratory Methods with the confirmed plan, .m code, actual execution records, and result evidence.
   - Preserve each method_id or validation_id, original task_id, requiredness, objective, input selection, expected output, execution conditions, acceptance criteria, and artifact provenance through existing compatible records.
   - Do not infer or change requiredness, method identity, task scope, or experiment design because of performance, complexity, runtime, cost, or failure. Do not count unauthorized exploration as required work or substitute diagnostic_reference for the usable baseline.
   - A fallback may replace a confirmed required method only when its trigger is evidenced and an explicit human decision authorizes that specific activation or replacement, identifying the affected method and applicable plan scope.
   - Require the updated plan confirmation and traceable supersession for a substantive replacement; trigger evidence alone is insufficient. Preserve the original method's failed attempts, Warning text, and execution evidence.
2. Inspect and run the code when a compatible runtime is available.
   - Apply the authorization checks in Preconditions before execution or repair. A compatible executable alone does not authorize a run.
   - Separate static inspection from real runtime checks; a syntactically plausible .m file or static inspection does not prove execution, reproducibility, or output correctness.
   - Run or rerun only the confirmed scope with actual authorized data, runtime, dependencies, licenses, and side effects. Do not install dependencies or switch models to make a review pass.
3. Evaluate:
   - `syntax`
   - `input_contract`
   - `method_alignment`
   - `reproducibility`
   - `output_contract`
   - Apply the existing five named checks to the full confirmed four-category scope; do not add mandatory review keys or a separate audit framework.
   - For every required validation_id, verify task_id, validation target, applicability, independent design, data requirements and selection, execution conditions, metrics or observable outputs, success/failure criteria, failure impact, and evidence artifacts against the confirmed plan.
   - Inspect actual implementation, execution records, executed scripts or functions, input provenance, configuration, and substantive results. Code existence or an expected result is not proof that validation ran or passed.
   - Distinguish validation implemented, actually executed, supported by traceable evidence, and meeting its acceptance criteria. In-sample fit is not automatically independent testing; a risk-probe PASS is not formal validation.
   - Use task-appropriate checks and disclosed criteria; do not force all problems into one experiment design or invent acceptance thresholds. Numerical agreement and AI self-review are not independent mathematical proof.
   - Cross-check run-summary claims against actual .m entries, inputs, splits or missingness masks, metrics, tables, saved figures, units, output directories, and timestamps or round identity. A file's existence does not prove successful execution; execution success does not prove validation success.
4. Include compatibility evidence for toolbox usage, `jsonencode`, file I/O, plotting/export, and 北太天元 constraints.
   - Apply MATLAB Runtime and Numerical Review below using genuine evidence from the selected runtime; do not infer compatibility from keywords or Python behavior.
5. Add only relevant numerical, feasibility, leakage, or scale checks.
6. If runtime is unavailable, use `NOT_RUN` rather than claiming execution success.
   - Preserve this existing MATLAB-review NOT_RUN provision as qualified in Review Schema. Do not copy Python's narrower status vocabulary over it or insert that value into an unrelated run-summary contract.
   - Missing runtime, Toolbox, license, inputs, or authorization is not evidence that a mathematical model actually executed and failed. Record the actual prerequisite problem and unexecuted scope.
7. If asked to fix findings, patch minimally and rerun affected checks.
   - Without an explicit repair request, report findings without changing code. Repair permission does not authorize changes to scientific meaning, data, requiredness, method scope, human decisions, schemas, upstream Skills, or the approved experiment design.
   - If a repair requires a substantive plan change, stop the affected repair and request new human confirmation through Handoff.
   - Preserve pre-repair failures, native errors, Warnings, and actual outputs; distinguish a real rerun from a proposed or blocked rerun. Do not mark an unexecuted repair verification PASS.
8. Save `code/matlab/Qx/reviews/qx_matlab_review.json`.
   - Publish only a truthful review representable by the existing MATLAB Review Schema. If lawful representation or required evidence is unavailable, retain evidence, withhold incompatible or falsely passing publication, and report the actual limitation and BLOCKING_ERROR through Handoff.

## MATLAB Runtime and Numerical Review

- For .m scripts and functions, verify actual filenames, function names, entry points, arguments, dependencies, execution order, and working directory. A script and a function are not interchangeable entry points; do not substitute a Python .py launcher.
- Record the real MATLAB or 北太天元 runtime and version, supported functions, approved Toolbox dependencies, and actual license evidence where applicable. Installed-product or license checks alone do not prove model execution; do not assume MATLAB license behavior applies to 北太天元.
- Inspect the confirmed rng call or equivalent, recorded seed, and any required random stream configuration. For 北太天元, verify support for that mechanism; use only a confirmed equivalent or report the reproducibility limitation without claiming a reproducible run.
- Verify project-root-safe fullfile paths, explicit approved cleaned-data inputs, field names, units, shapes, and actual outputs. Inspect any cd or addpath scope and restoration after success or failure; do not persist a global search path or use unapproved locations to bypass input failures.
- Check readtable, readmatrix, writetable, writematrix, save, load, and related operations against actual runtime support and the approved data contract; neither an I/O call nor a reported path proves a valid saved file.
- Verify actual jsonencode support or the approved deterministic compatible serializer, correct escaping and types, and preservation of the existing summary/review contract. Do not infer compatibility from the presence of a jsonencode token or emit malformed JSON.
- Check plan-approved saveas, print, exportgraphics, or other actual export operations only where supported by the selected runtime and version. Verify saved table and figure files and report native export errors; a plot window is not a delivered image or proof of rendering quality.
- Add applicable numerical precision, tolerance, stability, boundary-condition, constraint-feasibility, objective-value, and perturbation checks according to the confirmed plan. Record evidence and limitations; do not invent tolerances or equate a solver exit flag with feasibility or validation.
- Preserve genuine MATLAB MException identifiers, messages, and available stacks, or the actual native error mechanism of 北太天元. Do not fabricate a MATLAB stack, use Python traceback as a substitute, or describe a launch failure as an executed-model exception.
- Preserve original Warning text, available identifiers or locations, associated methods or validations, and observed effects. A Warning alone is not failure; unresolved major risks require evidence-based findings and BLOCKING_ERROR when they prevent a supported conclusion.
- Use diary or another full log only for failure, relevant Warnings, or a reproducibility need; compact genuine evidence remains sufficient for ordinary success. Do not require meaningless success logs, globally suppress Warnings to obtain a clean review, or discard partial outputs and failed attempts.
- Do not execute code that reads or overwrites protected raw data, alters unapproved paths, or silently changes runtime state. Inspect and repair only within explicit authorization and approved cleaned-input contracts.


# Review Schema

Use the same schema as `python-code-reviewer`, with:

- `"language": "matlab"`
- `runtime`
- `compatibility_target`
- optional `compatibility` check

Required named checks use `PASS`, `FAIL`, or justified `NOT_APPLICABLE`. Runtime-dependent checks use `NOT_RUN` when execution was impossible; this blocks G3 until executed.

## Existing JSON Contract and Execution Facts

- The original MATLAB Skill contains no inline JSON example; its Review Schema explicitly inherits the Python Reviewer base structure with the MATLAB differences listed above. Read that actual current base example rather than copying unverified Python fields or inventing a standalone MATLAB schema.
- Preserve inherited schema_version: 1 and the five original named checks, plus the original MATLAB language, runtime, compatibility_target, optional compatibility check, documented statuses, verdict contract, and code/matlab/Qx/reviews/qx_matlab_review.json path.
- The existing MATLAB exception permits NOT_RUN for runtime-dependent review checks when execution was impossible, and such required work blocks G3 until executed. Do not broaden NOT_RUN to unrelated fields, add it to run_summary.json without existing support, or replace it with fabricated PASS or executed failure.
- Use NOT RUN in factual reporting for unexecuted work with its actual reason, and FAILED only for real executed failures with native errors and evidence. BLOCKING_ERROR belongs to Handoff or the blocking report, not a new review-check status, run-summary status, or verdict.
- PASS requires concrete current evidence for each applicable component of the named check, including runtime evidence where required. A static result must not become a passing runtime review; a combined check with unexecuted runtime work uses the existing applicable NOT_RUN provision or a truthful publication block.
- Use FAIL for an actual failed review criterion supported by evidence; a missing required artifact can fail output-contract review without implying executed-model failure. NOT_APPLICABLE requires genuine inapplicability, not missing runtime, authorization, or evidence.
- A completed run may fail validation or be inconclusive. Do not collapse execution status, validation outcome, evidence availability, and workflow permission into one successful claim.
- Preserve original failures, unexecuted work, authorized exploration, rerun history, pre-repair evidence, Warning wording, native errors, logs when needed, and partial outputs. An empty errors list or top-level success cannot erase a method-level failure or establish overall required-work success.
- Report actual field names, values, files, evidence, and affected claims for unknown, illegal, or contradictory statuses; do not normalize by guessing. If the conflict prevents a defensible conclusion, output BLOCKING_ERROR through Handoff.
- Do not add mandatory JSON fields, check names, role/status/verdict enums, schema files, or a state system. The original schema reference does not authorize blindly copying Python-only runtime semantics or removing MATLAB's documented NOT_RUN provision.
- Do not repurpose the method-choice decision_id as proof of current-plan confirmation. Preserve actual revision and confirmation provenance using genuine existing evidence references and Handoff without inventing ledger or review fields.
- If existing legal fields or verdicts cannot express an actual finding, preserve evidence and report the contract gap and BLOCKING_ERROR through Handoff instead of publishing an incompatible or falsely passing review. Do not modify run summaries, schemas, historical results, or packaging code to force compatibility.

# Rules

- Do not pad pass items.
- Do not fabricate MATLAB/北太天元 execution.
- Do not approve unavailable toolbox dependencies without an explicit target exception.
- Do not change the mathematical model silently.
- Do not require a duplicate Markdown review.

# Verification

- Approved main and baseline scope is enforced.
- Compatibility constraints are checked.
- Run summary and outputs agree.
- Verdict follows required check statuses and runtime evidence.

- Preserve the confirmed four-category scope, actual plan-confirmation linkage, required-validation evidence, and specific fallback authorization defined above.
- Do not downgrade required work, invent execution evidence, or delete failed or unexecuted exploration to manufacture a passing review.
- Do not modify other Skills, manifests, decision ledgers, Gate permissions, schemas, or the packaging script; report next actions for orchestrator scheduling.
- Do not directly invoke another Skill or install dependencies as a repair shortcut. Do not replace MATLAB execution semantics with Python entry points, package installation, exception, or export mechanisms.
- Do not substitute synthetic data for real experimental inputs unless the confirmed plan explicitly authorizes its purpose and generation conditions; label functional checks honestly.

# Handoff

The existing primary output remains code/matlab/Qx/reviews/qx_matlab_review.json when truthful compatible publication is possible. This explicit Handoff is an added reporting boundary, not a claim that the original Skill had a Handoff section.

- Provide workflow-orchestrator with the actual review artifact or publication-block reason, affected task/method/validation IDs, current plan content and revision, genuine authorization evidence, real runtime and dependency limits, findings, and corrective evidence required.
- Provide actual code and entry points, inputs, execution records, metrics, tables, figure paths, native errors, relevant Warnings, NOT RUN work, failed exploration, and retained earlier attempts for downstream result-report-generator use. Do not replace result analysis or write unsupported paper claims.
- For BLOCKING_ERROR, identify the blocked operation, actual missing or conflicting authorization, runtime, data, status, or interface evidence, affected required work and claims, proposed responsible owner, and next repair requirements.
- Keep static checks performed, actual executions, validation findings, evidence availability, and NOT RUN items separate. A rule-definition review is not a MATLAB or 北太天元 experiment.
- Do not directly schedule or invoke downstream Skills, change another Skill's status, modify manifest or Gate state, or create or alter decision ledgers. workflow-orchestrator owns scheduling and Gate decisions.
