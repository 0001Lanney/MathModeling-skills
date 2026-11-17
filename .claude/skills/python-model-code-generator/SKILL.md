---
name: python-model-code-generator
description: Generate and execute reproducible Python code for human-confirmed main models, usable baselines, required validation experiments, and authorized non-required exploratory methods, preserving truthful execution evidence and experiment artifacts.
---

# Preconditions

- G2.5 human method choice is recorded in `methods/Qx/qx_decisions.jsonl`.
- `code/Qx/qx_code_plan.md` exists.
- Required cleaned data and profile exist.
- The plan targets Python.

Legacy method pools and `code/model-code-analyzer.md` may be read during migration, but they do not override the human choice.

Read the actual current code plan produced by `model-code-analyzer` and the relevant existing human-confirmation record before generating code.

- A recorded method choice does not establish code-plan confirmation.
- G2.5 does not automatically confirm the required-method list.
- Permission to continue does not confirm every method or experiment unless the user explicitly approved the referenced plan and list.
- Do not reconstruct the plan from memory, the method card, or an earlier version.
- Do not create or repair a human authorization record.

- For Qx-specific confirmation, use the actual `methods/Qx/qx_decisions.jsonl` path, replacing `Qx` and the corresponding `qx` filename component with the real question ID and ledger filename. During actual Skill execution, read the existing relevant record before relying on its authorization. Text drafting or review does not require a physical ledger file to exist.

- Treat `planning/framing_decisions.jsonl` as a conditional reading path for relevant global or pre-Qx decisions. During actual Skill execution, read it if it exists and is relevant. If authorization relies on either the Qx ledger or the global ledger but the required file or record is missing, unreadable, or untraceable, report that authorization evidence cannot be verified, output `BLOCKING_ERROR` through the Handoff, and stop affected generation. If no relevant authorization depends on a ledger, its absence alone is not an error.

- This Skill must not create or modify either designated ledger, or search for or use an undesignated alternative authorization ledger. Do not assume that a missing or unreadable ledger contains confirmation. Do not infer from its absence that authorization was never given, and do not treat an unverified authorization as valid.

## Plan Content and Human-Confirmation Match

Verify all of the following before affected code generation:

- the actual code-plan path and current contents;
- `plan_revision` or another real, traceable revision identifier;
- the plan's task IDs;
- the four-category method and experiment list;
- requiredness, objectives, inputs, expected outputs, execution conditions, and acceptance criteria;
- the actual decision record's `decision_type`, `status`, `decided_by`, and `choice`;
- genuine authorization wording, references, and evidence linking the decision to that plan;
- applicable supersession or revocation records.

The confirmation must explicitly cover the current plan and its four-category list:

- Required Main Model;
- Required Baseline;
- Required Validation Experiments;
- Non-required Exploratory Methods.

Do not assume historical records contain a particular optional field. Read real fields and traceable referenced evidence without inventing missing keys, decision types, authorization text, or references.

The applicable record must establish an explicit human decision. A pending record, AI suggestion, unrelated method choice, or confirmation of a substantively different plan is insufficient.

## Reliable Revision Evidence

Verify plan content identity, not only a version label or filename.

- Compute SHA-256 for the actual current plan contents, or use a reliable revision reference that resolves to the exact historical content.
- Trace the human confirmation to that content through an existing recorded digest, an immutable version reference, or other genuine evidence identifying exactly what was approved.
- A newly computed digest alone does not prove that the user previously approved those contents.
- Do not backfill a historical digest, fabricate a confirmation, or add ledger fields to manufacture the association.
- Do not treat the same version string or mutable path as proof that the plan has not changed.
- Compare the actual task scope, four-category list, requiredness, and substantive execution contract with the confirmed content.
- If a current digest differs from the confirmed digest, do not independently dismiss the difference as harmless. Require reliable evidence identifying the approved content or an explicit updated confirmation.
- A substantive change requires a new human decision covering the updated plan revision and preserving the relationship to the previous decision.

This check does not modify the plan, ledger, manifest, or another Skill's state.

If confirmation is missing, unreadable, untraceable, inconsistent with the current plan, superseded, or otherwise insufficient to establish approval, report `BLOCKING_ERROR` in this skill's Handoff and stop affected code generation.

Identify the affected tasks, conflicting or missing evidence, and the corrective evidence needed. Do not infer either approval or its absence from an unreadable referenced record.

## Confirmed Scope and Execution Readiness

Every confirmed item must be traceable to:

- `method_id` or `validation_id`;
- original `task_id` or task IDs;
- category and required or non-required designation;
- objective;
- input data and data requirements;
- expected outputs;
- success or acceptance criteria;
- execution conditions;
- evidence locations.

For each required validation experiment, also resolve its:

- validation target;
- applicability;
- independent experimental design;
- metrics or substantive observable outputs;
- failure impact.

An empty authorized exploratory category is valid. Do not add methods to fill it.

Do not infer requiredness from method names, apparent performance, execution cost, complexity, runtime, or success and failure outcomes.

Check required runtime, dependencies, cleaned data, and plan prerequisites without installing dependencies or changing the plan unless separately authorized.

If a prerequisite is unavailable, report the affected scope and reason. Do not represent a pre-execution block as a model that actually ran and failed.

# Workflow

1. Read the code plan, decision ledger, method card, probe conditions, and data profile.
   - Perform the plan-content and human-confirmation checks in Preconditions before affected code generation.
   - Verify the actual plan revision and its association with the historical user confirmation.
   - Read genuine method-choice evidence separately from code-plan confirmation.
   - If the required association cannot be established, report `BLOCKING_ERROR`, identify the missing or conflicting evidence, and stop affected code generation.
   - Do not modify the ledger, manifest, or Gate state to clear the block.

2. Confirm scope:
   - one approved main method;
   - one usable baseline;
   - all required validation experiments in the confirmed plan;
   - only explicitly authorized non-required exploratory methods;
   - A fallback may replace a confirmed required method only when its trigger is evidenced and an explicit human decision authorizes that specific activation or replacement, identifying the affected method and applicable plan scope.

   Keep required main models, required baselines, required validation experiments, and non-required exploratory methods distinct.

   - Do not add a candidate or exploratory method on your own.
   - Do not delete an approved validation experiment.
   - Do not downgrade required work because of complexity, runtime, cost, or failure.
   - Do not use an exploratory method or `diagnostic_reference` as the official usable baseline.
   - A fallback trigger alone does not authorize replacement of a required main model.
   - A replacement requires an updated code plan, a new explicit human decision covering its revision, and a traceable supersession relationship.
   - Preserve the original method's execution and failure evidence after any authorized replacement.
   - If the scope changes substantively, stop affected implementation and wait for the new confirmed plan.

3. Generate clear runnable `.py` files under `code/Qx/`.
   - Implement the confirmed main method, usable baseline, required validation experiments, and authorized exploratory scope.
   - Do not consider code generation complete merely because main-model and baseline scripts exist.
   - Implement each required validation's confirmed target, applicability, design, data selection, metrics or observable outputs, acceptance criteria, execution conditions, and evidence production.
   - Keep validation identity traceable between the plan, implementation, actual execution, and results.
   - Reuse helpers and the smallest clear script arrangement where appropriate; an independent validation design does not require a separate file for every experiment.
   - Do not change the approved mathematical meaning, requiredness, or scope.

4. Use project-root-safe paths, fixed seeds, explicit inputs, and minimal justified dependencies.
   - Record the actual seed, relevant runtime and dependency versions, input selection, and configuration.
   - Keep data windows, splits, masks, perturbations, and generated-input procedures traceable when applicable.
   - Do not silently change a confirmed validation design to fit the environment.
   - Respect the original-data protection and other restrictions in Rules.

5. Save:
   - tables to `results/Qx/experiments/roundN/tables/`;
   - metrics to `results/Qx/experiments/roundN/metrics/`;
   - useful diagnostic/comparison figures to `results/Qx/experiments/roundN/figures/`;
   - canonical `run_summary.json`, only when the actual records can be expressed under the existing compatible contract.

   - Preserve actual input and output paths and usable metric or artifact locators.
   - Distinguish expected paths from files actually produced.
   - Do not invent metrics, output files, or successful execution records.
   - Apply the complete Run Summary contract below, including Actual Records and Evidence, Failure and Warning Preservation, Unexecuted Work and Legal Summary Publication, and Historical Compatibility.
   - If canonical publication is blocked under that contract, preserve genuine evidence and report the affected items, actual state, reason, and `BLOCKING_ERROR` through Handoff; do not publish an incompatible summary.

6. Evaluate and record output-degeneracy and fallback-trigger metrics required by the plan.
   - Execute the required validation experiments under their confirmed conditions.
   - Save actual metrics or substantive outputs and the evidence connecting them to inputs and executed scripts.
   - Record observations that fail or do not conclusively meet acceptance criteria without relabeling them as validation success.
   - Do not treat a successful probe, a main-model run, code existence, or expected output as completion of a separate validation experiment.
   - Keep these distinctions explicit: plan prepared, user confirmed, code generated, experiment actually executed, traceable evidence obtained, and validation criteria satisfied.
   - A completed execution can yield a failed or inconclusive validation outcome.
   - A failed or unexecuted required item prevents an overall required-work success claim.
   - Do not derive overall success from one successful method or an empty error list.

7. Persist full logs only on failure or when a warning needs reproduction.
   - Preserve real execution logs and available traceback for an actual Python execution failure.
   - If a process did not start, preserve the actual launch or prerequisite error rather than inventing a Python traceback.
   - Keep valid outputs produced before a failure, together with their actual provenance.
   - Retain each relevant Warning's original text, associated method or validation item, and evidence location.
   - A Warning alone does not establish experimental failure. Assess it with actual status, errors, and effects.
   - Do not silently discard Warnings or errors.
   - Do not require meaningless full success logs; compact execution records and actual artifacts remain acceptable when sufficient.
   - Keep intermediate evidence needed for review, reproduction, robustness, or explaining anomalies.

8. Run the code. Do not claim success from code generation alone.
   - Execute only the confirmed scope and only when authorization and execution prerequisites are satisfied.
   - For work not executed, report `NOT RUN` and its specific reason.
   - For work actually executed but failed, report the failure fact as `FAILED` with genuine errors, available traceback or process output, and existing evidence.
   - Report authorization or plan-confirmation blocks as `BLOCKING_ERROR`, not as a model execution failure.
   - Treat `NOT RUN` and `FAILED` here as execution-report labels, not approval to insert new JSON enum values.
   - Use a JSON status value only when the existing contract supports it and it accurately describes the execution.
   - If no compatible representation exists, follow the canonical-summary publication block in step 5.
   - Do not fabricate metrics or outputs when the runtime, dependencies, data, or execution is unavailable.
   - Do not delete failed tasks, lower requiredness, or automatically switch the main model.
   - Preserve execution and failure records for authorized exploratory methods as well as required work.
   - Identify how exploratory failures may affect selection, comparisons, conclusions, or credibility without writing final paper claims.
   - Report blocked scope and required corrective evidence for `workflow-orchestrator` to schedule.

9. Hand off to `code-reviewer`.
   - Apply all evidence, recipient, and blocking-report requirements in Handoff, including For Code Review, For Result Reporting, and Blocking Findings.
   - Preserve `code-reviewer` as the next technical-review owner; do not substitute result reporting for code review.
   - These are reported handoffs only; do not directly invoke another Skill or change its state. `workflow-orchestrator` manages subsequent scheduling and Gate decisions.

# Script Layout

Prefer the smallest clear layout:

```text
code/Qx/
├── qx_code_plan.md
├── qx_baseline.py
├── qx_main.py
└── run_all.py        # only when coordination is useful
```

Do not create one script per unapproved candidate. Do not create a README that duplicates the code plan.

Implement the confirmed validation experiments and authorized exploratory methods within this existing structure using the smallest clear arrangement.

- Reuse shared helpers and existing scripts where appropriate.
- Add a separate validation or exploratory script only when the confirmed plan and clear execution or evidence needs justify it.
- An independent validation design does not require a separate file for every experiment.
- Keep method and validation identities traceable between the plan, implementation, execution record, and actual outputs.
- Do not omit required validation because the example layout shows only main and baseline scripts.
- Do not add an unapproved candidate to fill a layout or increase the apparent breadth of experiments.
- Keep `run_all.py` optional and use it only when coordination is useful.
- Do not create an alternative state file, duplicate plan, or independent audit framework.
- A script's existence does not establish that it ran or that its validation criteria were met.

# Run Summary

Follow the schema in `model-code-analyzer`. Include:

- approved decision ID;
- method IDs and roles;
- inputs and outputs;
- seed and environment;
- execution status and timing;
- compact metric summaries;
- output-degeneracy evidence;
- warnings/errors;
- fallback-trigger state.

Preserve the existing summary structure and `schema_version: 1`. Do not force upgrades of historical summaries or modify a JSON schema.

The code plan, its confirmed content identity, and the corresponding human-confirmation record must remain traceable in the Handoff and existing plan and ledger references.

Do not silently repurpose an existing method-choice decision field as a code-plan confirmation field. Do not introduce a new JSON field solely to resolve that distinction.

## Actual Records and Evidence

Retain actual execution records for:

- required main models;
- required baselines;
- required validation experiments;
- authorized non-required exploratory methods.

Use only roles, fields, and status values supported by the applicable existing contract.

- Preserve each item's real identity and its relationship to the confirmed plan.
- Keep validation IDs traceable to the relevant method or experiment record through existing compatible records and references.
- Do not invent role values or hide a validation experiment under an unrelated method identity.
- If the existing contract cannot represent a required category accurately, report the interface gap and do not publish an incompatible or misleading summary.
- Record actual input paths, data selections, execution scripts, configurations, and output paths.
- Identify actual metrics and substantive outputs with usable artifact locators.
- Do not list a planned output as an existing result.
- Record genuine execution timing, seed, environment, warnings, and errors.
- Do not invent an execution duration, dependency version, input file, metric, or result path.
- Keep evidence needed to reproduce or explain an anomaly without requiring meaningless full success logs.

For each validation experiment, preserve the relationship among:

- the confirmed validation design;
- actual input data or generated-input procedure;
- the executed script or entry point;
- the actual execution record;
- observed metrics or substantive outputs;
- the applicable acceptance criteria;
- the resulting validation finding.

Code generation, actual execution, production of traceable evidence, and satisfaction of validation criteria are different facts.

An experiment can execute successfully while failing or not conclusively satisfying a validation criterion. Do not collapse these findings into a single unsupported success statement.

## Failure and Warning Preservation

Preserve failures of required and non-required work.

- Keep the failed item's identity, role, actual execution state, error information, and available outputs.
- Preserve genuine failure logs and available traceback for Python execution errors.
- Preserve actual launch or system errors when the process did not start.
- Do not fabricate a Python traceback for a pre-execution problem.
- Retain each relevant Warning's original wording, method or validation association, and evidence location.
- A Warning alone does not establish experimental failure. Evaluate it with actual status, errors, and observed effects.
- Do not silently delete or ignore relevant Warnings.
- An empty `errors` array does not establish that execution occurred or succeeded.
- A top-level success value, when present in an existing summary, cannot erase a method-level failure.
- A method-level success does not establish that all confirmed required work ran or passed.
- An exploratory failure remains a failure even when it does not invalidate the required-work result.
- Do not delete unsuccessful or unexecuted items to manufacture overall success.
- Do not remove the original failure when an authorized fallback is later executed.
- Keep rerun and replacement evidence distinguishable from the original attempt.

If existing status records conflict or cannot be interpreted under the documented contract, do not invent a normalization or successful interpretation. Report `BLOCKING_ERROR` through the Handoff with actual fields, values, evidence, and affected scope.

## Unexecuted Work and Legal Summary Publication

Use `NOT RUN` in this skill's execution report or Handoff for work that did not execute, with the specific reason.

Use `FAILED` in the execution report for work that actually executed and failed, with genuine error evidence.

These report labels do not authorize new JSON status values.

- Do not assume that `not_run`, `NOT RUN`, `FAILED`, or another spelling is a supported JSON enum.
- Use a JSON status value only when the applicable existing contract supports it and it accurately represents the facts.
- Do not write `BLOCKING_ERROR` into a run-summary `status` field.
- Do not represent non-execution as success.
- Do not represent non-execution as an actual model execution failure.
- Do not put a value into canonical `run_summary.json` that violates the existing schema or contract.

If the existing JSON contract cannot accurately express `NOT RUN`:

1. Do not generate or publish the incompatible canonical summary.
2. Do not add an unapproved status enum.
3. Do not substitute success or failure for non-execution.
4. Do not omit the unexecuted item to produce an apparently complete summary.
5. Preserve genuine logs, prerequisite errors, existing outputs, and evidence paths.
6. Record `NOT RUN`, its reason, affected items, and available evidence in the existing Handoff mechanism.
7. Report `BLOCKING_ERROR` and identify the exact contract gap.
8. Wait for the interface issue to be explicitly resolved before producing a compatible formal summary.

If a different actual execution state or category also lacks a supported representation, apply the same prohibition on incompatible or misleading publication and report the specific gap.

Do not overwrite a historical valid summary with an incompatible current record. Do not publish a previous summary as evidence for a new attempt.

Do not create an alternative JSON state file to bypass the canonical contract.

The obligation to produce canonical `run_summary.json` does not override truthfulness or schema compatibility. If formal publication is blocked, report the missing current summary and its consequences explicitly.

## Historical Compatibility

Read historical records without rewriting their original structure or fields.

- Do not assume that historical records contain new optional confirmation, task, hash, role, or status fields.
- Use only actual fields and genuine referenced evidence.
- Preserve original recorded values when reporting a supported interpretation.
- Distinguish a missing field from a null, empty, invalid, or conflicting value.
- Do not infer missing execution or confirmation facts.
- Do not treat an old successful method record as proof that the current plan and all required validations succeeded.
- Do not force a schema-version change or batch migration.

The known difference between method-level summary fields and downstream top-level packaging fields is outside this file's repair scope.

Do not modify `package_submission.py`, add top-level aggregation fields, or claim that the packaging interface mismatch has been resolved.

# Rules

- Do not change the approved model or baseline.
- Do not read or overwrite raw data.
- Do not hide assumptions in code.
- Do not emit placeholder metrics, figures, or successful statuses.
- Prefer portable `.py` scripts over notebook-only workflows.
- Keep intermediate files only when needed for explanation, review, robustness, or debugging.
- Use Type 1 diagnostic figures internally; do not present them as paper figures.
- Apply the complete authorization, plan-content, revision-evidence, and ledger restrictions in Preconditions, including Plan Content and Human-Confirmation Match, Reliable Revision Evidence, and Confirmed Scope and Execution Readiness.
- Do not change requiredness because of complexity, runtime, cost, inconvenience, or failure.
- Apply all scope, required-validation, baseline, fallback, replacement-authorization, and supersession restrictions in Workflow step 2.
- Preserve original failures, Warnings, and evidence after an authorized replacement or rerun.
- Apply the complete evidence, failure-preservation, execution/validation distinction, JSON-contract, and blocked-publication requirements in Run Summary and its subsections.
- Do not modify a manifest, decision ledger, JSON schema, another Skill, or the packaging script.
- Do not change Gate state, final-assembly permission, or another Skill's state.
- Do not directly invoke another Skill; identify the required handoff and let `workflow-orchestrator` schedule subsequent work.
- Do not install dependencies or change execution conditions beyond the confirmed plan and separately granted authorization.
- Do not write final paper claims or decide their scientific interpretation.
- Do not add a Skill, Gate, or independent state system.

## Conditional Global-Ledger Reading

Treat `planning/framing_decisions.jsonl` as a conditional reading path for relevant global or pre-Qx decisions.

- During text drafting or review, the path reference does not require verifying that a physical ledger file already exists.
- During actual Skill execution, read the file if it exists and contains relevant decisions.
- If authorization depends on that file and it is missing or unreadable, report that the authorization evidence cannot be verified and stop the affected generation through `BLOCKING_ERROR`.
- Do not assume that a missing or unreadable file contains confirmation.
- Do not assume that its absence proves no authorization was ever given.
- If no relevant authorization depends on the global ledger, its absence alone is not an error.
- Do not create the file, search for an alternative authorization ledger, or invent a confirmation record.

Apply this condition to the global-ledger reference in Preconditions. It does not remove the requirement to verify every authorization actually relied upon.

# Verification

Evaluate these checks against actual evidence. They are acceptance conditions, not statements that execution already succeeded.

- Main and baseline both ran and are directly comparable.
- Fallback code is absent unless activated.
- Formal outputs and run summary exist.
- Seed, inputs, versions, warnings, and errors are recorded.
- Required concentration/degeneracy checks are saved.
- Next handoff is `code-reviewer`.

For the original checks above:

- An authorized activation or replacement must satisfy the human-confirmation boundaries in Preconditions and Workflow.
- Existing output files alone do not prove that the current attempt ran successfully.
- If a compatible formal summary cannot be published, the summary-existence check is not satisfied. Report the block instead of creating an illegal file.
- A failed or unexecuted required item must not be hidden to make an acceptance check appear satisfied.

Also verify:

- The actual current code plan and relevant real decision records were read.
- The plan's content identity is linked to the user's confirmed content through SHA-256 or a reliable traceable revision.
- A new digest was not used as a substitute for historical confirmation evidence.
- Task IDs, method and validation identities, four-category scope, requiredness, and substantive acceptance conditions match the confirmation.
- Applicable supersession or revocation records were considered.
- No unconfirmed substantive plan change was implemented.
- Required main models, required baselines, required validation experiments, and authorized exploratory methods remain distinct.
- Required validation code implements the confirmed target, applicability, design, data needs, metrics or outputs, criteria, execution conditions, and evidence production.
- Planned paths are distinguished from actual output files.
- Validation execution is traceable to real inputs, scripts, configuration, and observed results.
- Actual execution, evidence availability, and validation outcome are reported separately.
- Work not executed is reported `NOT RUN` with its reason.
- Actual failed execution retains genuine errors and available traceback or process output.
- Pre-execution authorization or prerequisite blocks are not misrepresented as model execution failures.
- Relevant Warning text, item association, and evidence locations remain available.
- Non-required exploratory failures and their effects remain recorded for result reporting.
- No unsupported JSON enum, role, field, or schema change was introduced.
- No `BLOCKING_ERROR` was written into a summary status field.
- An incompatible canonical summary was not generated or published.
- Unresolved contract gaps and the missing current summary are explicit in the Handoff.
- Historical outputs and execution records were not rewritten to conceal failure.
- Raw-data protection, explicit inputs, fixed seeds, minimal dependencies, portable scripts, and the existing output directories remain respected.
- Type 1 diagnostic figures were not presented as paper figures.
- No manifest, ledger, Gate permission, other Skill, or packaging script was modified.
- Subsequent technical review remains assigned to `code-reviewer`, with result evidence and blocks identified for orchestrator scheduling.

If a check is unsupported, failed, or not executed, report that condition rather than marking it passed. Do not interpret a checklist's existence as completed verification.

# Handoff

Provide the handoff through this skill's existing report or conversation output. Do not create another persistent state file, modify another Skill's status, or directly invoke its execution.

`workflow-orchestrator` manages subsequent scheduling and Gate decisions.

## For Code Review

Identify `code-reviewer` as the next technical-review owner and provide:

- actual generated script paths;
- the current confirmed code-plan path;
- the applicable revision and genuine content-identity evidence;
- method-choice and code-plan confirmation references, kept distinct;
- task IDs and the confirmed four-category list;
- actual input and output paths;
- available compatible run summary;
- validation design and execution evidence;
- metrics and substantive output locators;
- failed or unexecuted items;
- relevant Warnings, logs, errors, and traceback or process evidence;
- unresolved implementation, execution, or contract limitations.

If an output or canonical summary does not exist, state that explicitly. Do not list a planned path as a produced artifact.

## For Result Reporting

Provide the following for subsequent use by `result-report-generator`:

- actual successes, failures, and unexecuted work;
- required and non-required item identities;
- relevant original Warning content and evidence locations;
- failure reasons and available execution evidence;
- outputs preserved before failure;
- effects of exploratory failures on method choice, comparisons, main conclusions, or credibility;
- authorized replacement and rerun provenance;
- unresolved validation outcomes and limitations.

Do not erase a failed exploratory attempt or describe it as a successful experiment.

The generator supplies factual records. It does not replace result analysis, package assembly, or final paper disclosure.

## Blocking Findings

For each `BLOCKING_ERROR`, report:

- the affected task, method, or validation IDs;
- the operation that is blocked;
- the code-plan and authorization references involved;
- the actual missing, unreadable, conflicting, or unsupported evidence;
- actual field values and types when relevant;
- the execution fact, including `NOT RUN` where applicable;
- the specific reason;
- genuine logs, errors, existing outputs, and evidence locations;
- effects on required work and dependent results;
- the recommended responsible owner;
- the correction, authorization, environment, data, or interface evidence needed before continuation;
- whether the current canonical summary could not be generated or published;
- any unaffected authorized work that can safely continue.

Do not use `BLOCKING_ERROR` as a JSON execution-status value.

Do not independently resolve an authorization or interface gap by changing the plan, ledger, schema, method requiredness, or Gate state.

For a blocked summary, wait until the interface issue is explicitly resolved before producing a compatible formal record. For a plan-confirmation block, wait for verifiable authorization covering the actual current plan. For an execution or data prerequisite, wait for the required genuine corrective evidence.

Preserve original failure and non-execution facts when work later resumes. A repaired environment, authorized method replacement, or successful rerun does not erase the earlier record.
