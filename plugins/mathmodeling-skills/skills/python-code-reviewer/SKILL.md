---
name: python-code-reviewer
description: Review, run, debug, and verify approved Python modeling code against its code plan, data contract, method decision, risk conditions, and experiment outputs, saving one compact JSON review.
---

# Preconditions

- Python code and `code/Qx/qx_code_plan.md` exist.
- Approved method decision, method card, data profile, and relevant run summary are available.
- Required inputs are accessible.

## V2.0 Dependency Boundary — NEW

The local model-code-analyzer Skill may still be the old version. Read it only to establish actual paths, existing fields, JSON examples, and legacy constraints. Do not treat its main-plus-baseline scope or immediate generator handoff as the V2.0 authority.

Record VERSION_GAP when the local Analyzer lacks the V2.0 four-category list, explicit current-plan confirmation, required-validation, specific fallback authorization, or evidence requirements defined here. VERSION_GAP is a dependency finding, not a JSON status or permission to waive a requirement.

Do not modify the Analyzer, assume its reviewed-but-unwritten revision is active, or invent V2.0-specific fields, enum values, or implementation details. This Skill's explicit V2.0 requirements remain applicable.

## Current Plan and Real Human Confirmation — NEW

- Read the actual code/Qx/qx_code_plan.md and relevant existing methods/Qx/qx_decisions.jsonl. Qx and qx are path templates; substitute the real question and filename.
- Read planning/framing_decisions.jsonl only if it exists and is relevant to an actual global or pre-Qx authorization. An unrelated absent global ledger is not an error.
- Verify the current plan's task IDs, four-category item identities, requiredness, objectives, inputs, outputs, acceptance criteria, and execution conditions against the user's actual choice and authorization evidence.
- Inspect the actual decision_type, status, decided_by, choice, evidence references, and applicable supersession or revocation without inventing missing fields or a standardized decision type.
- Link the current plan's exact content to the historical human confirmation using a recorded SHA-256 or a reliable revision reference and genuine approval evidence. A newly computed digest or version label alone does not establish approval.
- G2.5 method selection, a generic instruction to continue, or an old confirmation for substantively different content does not confirm the current complete code plan.
- If actual confirmation is missing, unreadable, contradictory, or not linked to current content, report BLOCKING_ERROR in Handoff and stop affected execution, repairs, and final review approval. Safe static inspection may continue only within available authorized scope and must not be labeled a passing execution review.
- Do not assume either approval or its absence from a missing or unreadable referenced record. Report the unverifiable evidence and needed correction.
- This Skill must not create or modify either designated ledger, search for an undesignated authorization ledger, change a manifest or Gate, or modify another Skill. The decision logger records genuine user decisions; workflow-orchestrator schedules subsequent actions.

# Workflow

1. Resolve the approved main and usable baseline from the actual confirmed current plan. Flag scripts for unapproved candidates; a fallback activation claim is not sufficient without its specific human authorization.
   - Reconcile Required Main Model, Required Baseline, Required Validation Experiments, and Non-required Exploratory Methods with actual scripts and execution records.
   - Do not infer requiredness from performance, complexity, runtime, cost, or failure; do not remove validation or expand exploration.
   - A fallback may replace a confirmed required method only when its trigger is evidenced and an explicit human decision authorizes that specific activation or replacement, identifying the affected method and applicable plan scope.
   - Require an updated confirmed plan revision and traceable supersession for a substantive replacement. Preserve the original failure, Warning, and execution evidence.
   - A diagnostic reference or exploratory method cannot substitute for the usable baseline.
2. Inspect and run the code in the intended order.
   - Separate static inspection from actual execution. Static syntax inspection cannot establish that imports, execution, reproducibility, or outputs passed at runtime.
   - Execute or rerun only the confirmed plan under the actual authorized runtime, dependency, data, and side-effect conditions. Do not install dependencies or switch required methods to make a review pass.
   - Missing authorization or execution prerequisites are blocks, not proof that a model executed and failed. Use the Execution Facts and Evidence rules below.
3. Evaluate required checks:
   - `syntax`: imports, execution, exceptions, and obvious runtime faults.
   - `input_contract`: paths, fields, units, shapes, missing-data handling, and raw-data protection.
   - `method_alignment`: formulas, objectives, constraints, assumptions, main/baseline roles, and fallback scope match the approved plan.
   - `reproducibility`: seed, deterministic setup, dependency/runtime record, and rerun consistency.
   - `output_contract`: saved tables/metrics/figures, valid run summary, comparable main/baseline metrics, degeneracy evidence, and fallback-trigger state.
   - Cover confirmed required validation within the existing five named checks rather than adding mandatory review keys or a new audit framework.
   - For each required validation_id, verify the actual implementation, task and target, applicability, independent design, input selection, metrics or observable outputs, success criteria, execution conditions, and evidence artifacts against the confirmed plan.
   - Verify actual execution records, input data, executed scripts, configuration, and result locators. A plan, code file, expected result, or main-model success does not prove that separate validation ran or passed.
   - Keep code generation, execution completion, traceable evidence, and satisfaction of validation criteria separate; an executed validation can fail or remain inconclusive.
   - Compare authoritative run-summary claims with actual on-disk metrics, tables, figures, units, data splits, method roles, and input/output provenance. Missing or stale outputs do not become current evidence because a summary says success.
   - For numerical or theoretical checks, distinguish formula alignment, independent numerical checks, actual experimental evidence, and proof. AI self-review or successful execution alone is not an independent mathematical proof.
4. Add risk-specific checks only when relevant, such as leakage, constraint feasibility, numerical stability, or scale.
5. If asked to fix findings, make minimal changes, rerun affected checks, and record the repair. Otherwise report findings without changing code.
   - Repair authorization does not permit changing scientific meaning, requiredness, task scope, human decisions, schemas, another Skill, or original data.
   - If the correction changes the confirmed substantive plan, stop that repair and request an explicit updated decision through Handoff.
   - Retain pre-repair failure evidence and distinguish actual reruns from a proposed rerun.
6. Save `code/Qx/reviews/qx_python_review.json`.
   - Publish only a truthful review that the existing Review Schema can represent. The example below is a structural example, not a pre-filled successful result.
   - If unexecuted or unrepresentable checks cannot be encoded without inventing statuses or misusing NOT_APPLICABLE, do not publish an incompatible or falsely passing review JSON. Preserve evidence and report BLOCKING_ERROR through Handoff.

# Review Schema

```json
{
  "schema_version": 1,
  "question_id": "Q1",
  "language": "python",
  "reviewed_files": [],
  "decision_id": "q1_method_choice",
  "checks": {
    "syntax": {"status": "PASS", "evidence": []},
    "input_contract": {"status": "PASS", "evidence": []},
    "method_alignment": {"status": "PASS", "evidence": []},
    "reproducibility": {"status": "PASS", "evidence": []},
    "output_contract": {"status": "PASS", "evidence": []}
  },
  "findings": [],
  "verdict": "PASSED",
  "reviewed_at": "ISO-8601"
}
```

Statuses are `PASS`, `FAIL`, or `NOT_APPLICABLE` with a reason. Any required `FAIL` blocks G3.

## Execution Facts and Evidence — NEW

- Use NOT RUN in this Skill's report for checks or experiments not executed, with the actual reason and affected scope.
- Use FAILED in the report only for an actual executed failure, with real errors, available Python traceback or process output, logs, and produced artifacts.
- If a process did not start, retain its actual launch or prerequisite error; do not fabricate a Python traceback or describe non-execution as executed failure.
- BLOCKING_ERROR is a workflow finding in this Skill's Handoff, never an invented run-summary or review-check status. Do not modify Gate state to enforce it; report its effect for orchestrator scheduling.
- Preserve relevant Warning wording, method or validation association, and evidence location. A Warning alone does not prove experimental failure; assess actual statuses, errors, and effects, and report an unresolved major risk at its supported blocking severity.
- Do not delete failed, unexecuted, exploratory, or pre-repair records to manufacture success. Preserve failures of non-required methods and their effect on comparisons, selection, conclusions, or credibility for result reporting.
- A top-level success label cannot erase method-level failures. Empty errors, a successful method, or an existing script alone cannot establish overall required-work or validation success.
- Treat unresolved status conflicts, unknown states, illegal types, or missing authoritative evidence as BLOCKING_ERROR when they prevent a supported result or review conclusion. Report actual fields, values, locations, and affected claims; do not normalize by guessing.

## JSON and Historical Compatibility — NEW

- Keep the existing schema_version: 1, five named checks, review path, example structure, and documented check statuses. Do not add status or role enums, mandatory fields, schema files, or a separate state system.
- The existing decision_id example identifies method choice; do not silently repurpose it as plan confirmation. Keep distinct plan-revision and confirmation provenance in genuine existing evidence references and Handoff.
- NOT RUN, FAILED, BLOCKING_ERROR, and VERSION_GAP here are report labels or findings, not newly authorized JSON values.
- NOT_APPLICABLE requires genuine inapplicability. Missing runtime, missing execution, missing authorization, and unavailable evidence do not make an applicable required check inapplicable.
- PASS requires actual evidence for every applicable component of the named check, including execution where required. Do not mark the combined syntax check PASS based only on static syntax inspection.
- Do not use FAIL merely to disguise an experiment that never ran. Report the actual missing-execution or evidence condition without inventing an execution history.
- Use FAIL when a required review check actually fails under its defined criteria and evidence. A missing required artifact may fail output-contract review without implying that the model itself executed and failed.
- If a truthful check or overall verdict cannot be represented under the established contract, withhold incompatible formal publication and report BLOCKING_ERROR through Handoff; do not invent NOT_RUN or other enums, force an unsupported verdict, or emit a falsely passing review.
- Review historical summaries and reviews using actual fields and documented compatible meanings. Preserve unknown or conflicting evidence rather than rewriting records or assuming a new confirmation field exists.
- Do not modify run summaries, JSON schemas, packaging interfaces, or historical experimental results to reconcile a mismatch.

# Rules

- Do not pad evidence to reach a count.
- Do not fabricate execution or outputs.
- Do not approve a toy diagnostic reference as the official baseline.
- Do not silently change mathematical meaning.
- Do not create success logs beyond the review JSON.
- Treat code newer than its review as requiring the affected checks to rerun, not necessarily the entire pipeline.
- Apply the current-plan confirmation, four-category scope, validation, execution-evidence, and compatible-publication requirements above without weakening them to match the old local Analyzer.
- Do not replace a required method or activate a fallback without the specific human decision and applicable confirmed plan revision.
- Do not modify manifests, decision ledgers, Gate permissions, another Skill, a schema, or the packaging script.
- Do not directly invoke another Skill; provide the next actions and evidence through Handoff for workflow-orchestrator scheduling.
- Do not substitute synthetic data for real experimental inputs unless explicitly authorized for the stated purpose in the confirmed plan; identify a functional fixture as such, not as real-data validation.

# Verification

- Every required named check has concrete evidence.
- Main and baseline are approved and comparable.
- Run summary and on-disk outputs agree.
- Review verdict follows check statuses.

The original acceptance conditions above require genuine current evidence, not a count of files or a copied PASS template.

- Verify all four categories against the actual confirmed plan and implementation; identify unauthorized, missing, failed, or unexecuted items.
- Verify historical confirmation linkage to exact current plan content, including the user's choice, applicable decision type and status, human ownership, task scope, and supersession.
- Verify that G2.5 method choice has not replaced code-plan confirmation and that a VERSION_GAP has not waived a V2.0 requirement.
- Verify required-validation implementation, actual execution, input/script provenance, independent design, metrics or outputs, and acceptance findings.
- Verify specific human fallback authorization, affected-method scope, updated plan confirmation, and preserved original failures.
- Verify that static review, runtime checks, validation outcomes, NOT RUN, actual FAILED execution, and BLOCKING_ERROR findings remain distinct.
- Verify actual Warning and error evidence, review-to-artifact consistency, JSON compatibility, and lawful publication or explicit blocking.
- Report each unperformed check as NOT RUN rather than claiming it passed. A checklist's existence is not completed verification.

# Handoff — NEW

The original delivery remains code/Qx/reviews/qx_python_review.json when a truthful compatible review can be published. This section adds explicit downstream reporting; it does not claim an original Handoff section existed.

- Provide workflow-orchestrator with the actual review artifact or the reason publication is blocked, affected files and task IDs, current plan revision, genuine authorization references, findings, and required next actions.
- Provide factual review, run-summary, metric, output, Warning, error, and exploratory-failure references for subsequent result-report-generator use. Do not replace result analysis or write final paper claims.
- For VERSION_GAP, identify the local Analyzer path, actual missing or older contract, affected V2.0 requirement, and evidence needed; do not edit the Analyzer or invent its unwritten implementation.
- For BLOCKING_ERROR, identify the blocked operation, actual missing or conflicting fields and files, evidence, affected required work and claims, proposed responsible owner, and corrective authorization, execution, data, or interface evidence.
- Retain genuine failed-attempt and pre-repair evidence. Clear only this Skill's finding after inspecting real corrective evidence; do not update another Skill's status, manifest, ledger, or Gate.
- Report separately the static checks performed, executions actually performed, results or validations satisfied, and NOT RUN items. Do not report a rule-definition check as model execution.
- Do not directly invoke downstream Skills. workflow-orchestrator owns scheduling and Gate decisions.
