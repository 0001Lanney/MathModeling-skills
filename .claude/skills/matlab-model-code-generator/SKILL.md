---
name: matlab-model-code-generator
description: Generate and run minimal reproducible MATLAB or Beita Tianyuan compatible code for the human-approved main method and usable baseline, with compact experiment artifacts and a canonical run summary.
---

# Preconditions

- G2.5 human method choice is recorded.
- `code/matlab/Qx/qx_code_plan.md` exists.
- Required cleaned data and profile exist.
- The plan targets MATLAB or 北太天元.

Legacy artifacts may be read during migration but do not override the human decision.

## Confirmed Plan and Authorization — NEW Shared Governance

Before generating code, read the actual current MATLAB code plan, relevant method-choice evidence, and the real human-confirmation record.

- G2.5 method selection is not code-plan or required-list confirmation.
- Verify the actual task IDs, method and validation identities, roles, requiredness, objectives, inputs, outputs, execution conditions, and acceptance criteria.
- The confirmed list must distinguish Required Main Model, Required Baseline, Required Validation Experiments, and Non-required Exploratory Methods.
- An empty exploratory category is valid; do not add methods or experiments to fill a category.
- Check the record's actual decision_type, status, decided_by, choice, and genuine authorization evidence without assuming undefined historical fields exist.
- Establish content identity using SHA-256 or a reliable revision that resolves to the exact approved plan content, and link that content to the historical human confirmation.
- A current digest alone, mutable filename, version label, G2.5 choice, or general instruction to continue does not establish current-plan approval.
- Do not invent approval, backfill a historical digest, or dismiss a content mismatch without verifiable evidence or new explicit confirmation.
- Check applicable supersession and revocation. A substantive plan change requires a new explicit decision covering the revision and preserving the prior-decision relationship.
- If the plan-confirmation association is missing, unreadable, inconsistent, or untraceable, report BLOCKING_ERROR through Handoff and stop affected code generation.

Use methods/Qx/qx_decisions.jsonl for relevant Qx decisions, substituting the real question and filename. Read planning/framing_decisions.jsonl only when it exists and is relevant to a global or pre-Qx decision. The path references do not require ledger files to exist during text drafting.

If actual authorization relies on a designated ledger or record that is unavailable, report authorization evidence as unverifiable; do not assume approval or conclude that authorization never occurred. An irrelevant absent global ledger is not an error.

This Skill must not create or modify either designated ledger, or search for or use an undesignated alternative authorization ledger. The decision logger retains its own role in recording actual user decisions.

Do not modify manifests, Gate permissions, schemas, another Skill, or the packaging script. Report subsequent actions for workflow-orchestrator scheduling; do not directly invoke another Skill or change its state.

# Workflow

1. Read the code plan, decision ledger, method card, probe conditions, and data profile.
2. Confirm scope: approved main plus usable baseline, all confirmed required validation experiments, and only explicitly authorized non-required exploratory methods.
   - A fallback may replace a confirmed required method only when its trigger is evidenced and an explicit human decision authorizes that specific activation or replacement, identifying the affected method and applicable plan scope.
   - Keep the fallback dormant until these conditions and an updated, traceably confirmed plan are satisfied.
   - Do not add a candidate, remove validation, expand exploration, or change requiredness because of complexity, cost, runtime, or failure.
   - Do not substitute a diagnostic reference or exploratory method for the usable baseline.
   - Preserve the original method's failure, Warning, and execution evidence after an authorized replacement.
   - Stop affected implementation when a substantive plan change has not yet been confirmed.
3. Generate conservative `.m` files under `code/matlab/Qx/`.
   - Implement every required validation experiment as well as the main method and baseline; script existence alone is not completion.
   - Resolve each validation_id, task_id, target, applicability, design, data requirements, metrics or observable outputs, success criteria, execution conditions, failure impact, and evidence artifacts from the confirmed plan.
   - Preserve mathematical meaning and keep plan, code, input selection, execution, and result identities traceable.
   - Distinguish plan preparation, human confirmation, code generation, actual execution, available evidence, and satisfaction of validation criteria.
   - Do not invent thresholds, data, or validation conclusions. A numerical run or AI self-review is not an independent mathematical proof.
4. Prefer basic matrix/table operations and avoid optional toolboxes unless the plan approves them.
   - Apply the retained Compatibility Rules and the explicitly marked NEW MATLAB-specific requirements below; do not substitute another language's runtime or package mechanisms.
5. Save tables, metrics, useful figures, and `run_summary.json` under `results/Qx/experiments/roundN/`.
   - Keep formal tables, metrics, and figures in the existing tables/, metrics/, and figures/ subdirectories as specified by the confirmed output contract.
   - Use actual output locations and evidence locators; planned files are not existing artifacts.
   - Publish canonical run_summary.json only when the actual facts can be represented under the existing contract; apply Run Summary below without adding unapproved fields, roles, or status enums.
6. Evaluate output-degeneracy and fallback-trigger metrics required by the plan.
   - Execute and retain the confirmed validation evidence when runtime and prerequisites permit. A successful main-model run does not prove that separate validation ran or passed.
7. Use `diary` or another full log only for a failure or reproducibility warning.
   - Keep real MATLAB or target-runtime error evidence, available exception stack information, relevant Warning text, associated item IDs, existing outputs, and evidence paths.
   - Do not suppress or delete failures or Warnings to make a run appear successful. A Warning alone is not an execution-failure verdict.
   - Do not require meaningless full success logs; compact authoritative records and necessary evidence remain sufficient.
8. Run in the available compatible runtime. If unavailable, report the unexecuted state explicitly.
   - Execute only the confirmed scope with the required runtime, dependencies, data, and authorization.
   - Work not executed is NOT RUN in the report, with its actual reason. Actual executed failure is FAILED in the report, with genuine runtime evidence.
   - A missing executable, license, toolbox, data input, or authorization is not proof that the mathematical model executed and failed.
   - Do not fabricate runtime logs, numerical outputs, status, or MATLAB exception stacks when execution did not occur.
   - Do not automatically generate synthetic data to stand in for missing real experimental inputs. Synthetic data is permitted only when the confirmed plan explicitly allows it and records its functional-check purpose, generation procedure, configuration, and seed.
   - Do not describe a synthetic functional check as a real-data experiment.
   - A required failure, NOT RUN item, or unverifiable validation blocks an overall required-work success claim.
   - Do not automatically lower requiredness, switch the main method, install dependencies, or change the confirmed experiment to bypass a block.
   - Report BLOCKING_ERROR and the affected scope, existing evidence, and necessary correction for workflow-orchestrator scheduling. Apply the JSON status restrictions below.
9. Hand off to `code-reviewer`.
   - Preserve code-reviewer as the next technical-review owner. Supply the Handoff evidence below through this Skill's report; do not directly invoke another Skill.

# Script Layout

```text
code/matlab/Qx/
├── qx_code_plan.md
├── qx_baseline.m
├── qx_main.m
└── run_all.m        % only when useful
```

Do not create scripts for unapproved candidates or a duplicate README.

## Entry Points and Path Scope — NEW MATLAB-Specific Requirements

- Keep the .m script and function arrangement minimal and consistent with the confirmed plan. An independent validation design need not require a separate file.
- Identify the actual script entry or function name, filename, arguments, and dependencies; do not assume a script and a function have interchangeable invocation semantics.
- Use project-root-safe fullfile paths and explicit cleaned-data inputs. Prefer explicit paths over relying on the caller's current directory.
- If cd or addpath is necessary, limit it to documented approved locations, record the prior working directory and path, and restore them after success or failure.
- Use onCleanup for restoration only where supported by the selected runtime, or a verified equivalent restoration procedure. Do not assume MATLAB utilities work unchanged in 北太天元.
- Do not use savepath or persist global search-path changes to make a local experiment run.
- Keep run_all.m optional and do not create GUI or alternative-language wrappers outside the confirmed scope.

# Compatibility Rules

- Prefer `readtable`, `readmatrix`, `writetable`, `writematrix`, `save`, `load`, and `fullfile`.
- Use `rng(2026)` or the recorded seed.
- For 北太天元, verify that the selected runtime supports the required random-seed mechanism; if not, use only a confirmed equivalent consistent with the approved plan, or report the reproducibility limitation without claiming a reproducible run.
- Use `jsonencode` when supported; otherwise write the required JSON fields deterministically.
- Avoid Live Scripts, App Designer, GUI code, Simulink, and toolbox-only functions unless explicitly approved.
- Note any 北太天元 compatibility risk in the run summary.

## Runtime, License, and Export Checks — NEW MATLAB-Specific Requirements

- Record the selected runtime, its actual version, required functions, and approved optional toolbox dependencies before claiming compatible execution.
- In MATLAB, use applicable installed-product and license evidence, such as ver or supported license checks, without equating product installation or a license check with successful model execution.
- For 北太天元, use that runtime's genuine compatibility evidence; do not assert MATLAB license or toolbox behavior without verification.
- Do not replace missing toolboxes with an unapproved method, install software, or fabricate an available license.
- Preserve the existing rng rule. Record the actual seed and any plan-required generator or stream configuration; do not substitute another language's seeding mechanism.
- For actual MATLAB exceptions, retain the genuine MException identifier, message, and stack when available. For another compatible runtime, retain its actual native error information rather than inventing MException data.
- Record actual Warning text and available identifiers or locations. Do not globally disable warnings to produce a clean-looking run; restore any explicitly approved temporary warning-state changes.
- Keep the original table, matrix, MAT-file, and fullfile I/O preferences. Verify actual field names, shapes, units, and outputs rather than assuming an I/O call proves correctness.
- Use plan-approved figure exports supported by the actual runtime, such as applicable print or saveas operations; use version-dependent export functions only after verifying support.
- Record actual exported figure files and any native export errors. A generated plot window is not proof that a saved figure exists or passed rendering inspection.
- Preserve the original jsonencode preference and deterministic fallback. Any fallback serializer must preserve the existing contract, correct JSON escaping, types, and reproducible field content; if this cannot be established, block canonical-summary publication rather than emitting malformed JSON.

# Run Summary

When canonical run_summary.json cannot legally be published, record the actual 北太天元 compatibility risks in the Handoff instead; do not create an incompatible summary merely to satisfy the original reporting requirement.

Follow the `model-code-analyzer` contract, including approved decision ID, roles, paths, metrics, output-degeneracy evidence, fallback state, timing, seed, environment, warnings, and errors.

## Truthful Execution and Contract Compatibility — NEW Shared Governance

- Preserve the existing summary structure and schema_version: 1; do not force historical upgrades or add a state file.
- Keep method-choice provenance distinct from code-plan confirmation. Reference the actual confirmed plan revision and decision through existing plan and Handoff evidence rather than silently repurposing a summary field.
- Retain actual records for main, baseline, required validation, and authorized exploration, linked to their plan IDs.
- Record actual input data or synthetic-input generation when authorized, scripts or function entries, configuration, seed, runtime, timing, actual outputs, and metric locators.
- Keep success, failure, NOT RUN facts, evidence availability, and validation outcomes distinct. An empty errors array, existing .m file, expected result, or method-level success does not establish overall success.
- Preserve failed and unexecuted work, original Warning content, errors, logs, outputs, and rerun history. A top-level success label cannot erase method-level failures.
- Optional status does not permit deleting an exploratory failure; pass its actual effects on selection, comparisons, and credibility to result reporting.
- Use only existing supported JSON roles, fields, and status values. NOT RUN and FAILED in this document describe report facts, not newly approved JSON enums.
- BLOCKING_ERROR belongs only in this Skill's Handoff or blocking report, never in a run-summary status field.
- If the existing JSON contract cannot accurately represent a real state or category, do not generate or publish an incompatible canonical summary, add an enum such as not_run, invent success or failure, or omit the item.
- Preserve genuine evidence and report the actual state, reason, affected items, contract gap, and BLOCKING_ERROR through the existing Handoff. Resume formal-summary publication only after the interface is explicitly resolved.
- Do not create a substitute JSON file, rewrite historical results, or publish an old summary as evidence for a new run.
- Read historical records without inventing missing authorization, version, role, status, or execution fields. Report missing, malformed, unknown, or contradictory evidence without a successful default.
- Do not alter the packaging script or add top-level aggregation fields to resolve downstream compatibility in this Skill.

# Rules

- Do not change the selected mathematical method.
- Do not access or overwrite raw data.
- Do not fabricate successful execution when MATLAB/北太天元 is unavailable.
- Keep only evidence-bearing intermediate outputs.
- Separate Type 1 diagnostics from paper figures.
- Apply the complete confirmed-plan and authorization rules in Preconditions and the scope and fallback restrictions in Workflow step 2.
- Do not create or modify designated decision ledgers, manifests, schemas, another Skill, or Gate state.
- Do not decide method requiredness, remove required validation, expand exploration, or weaken confirmed success criteria.
- Apply Script Layout and Compatibility Rules using MATLAB or the selected compatible runtime's actual semantics; do not substitute Python entry points, pip dependencies, Python traceback, or Python-specific data and graphics interfaces.
- Apply the Run Summary evidence and compatible-publication requirements even when formal outputs cannot be completed.
- Do not treat numerical agreement, code execution, or AI self-review as an independent theoretical proof.
- Do not directly call another Skill, install dependencies, or bypass an authorization or runtime block; report subsequent actions for orchestrator scheduling.

# Verification

- Main and baseline are directly comparable and both executed when a runtime is available.
- Fallback code exists only when activated.
- Formal outputs and run summary exist.
- Compatibility, seed, inputs, warnings, and errors are recorded.
- Required concentration/degeneracy checks are saved.
- Next handoff is `code-reviewer`.

The original checks above are acceptance conditions, not declarations that work already ran. An unavailable runtime must remain NOT RUN; required work and formal-summary gaps cannot be marked passed.

- Verify actual confirmed plan content, historical authorization linkage, current four-category scope, and applicable decision supersession.
- Verify that required validation implementation, actual execution, input and script provenance, metrics or outputs, and criteria findings are separately evidenced.
- Verify the original .m layout, toolbox restrictions, rng strategy, deterministic JSON alternative, diary policy, data protection, and Type 1 figure separation.
- Verify actual runtime and version evidence, applicable license or dependency limits, path-scope restoration when changed, native errors and Warnings, and real table and figure outputs.
- Verify that no unsupported JSON status or field was emitted and no incompatible canonical summary was published.
- Verify that original failures and authorized exploratory anomalies remain available for reviewer and result-reporting handoffs.
- If a check was not performed, mark it NOT RUN and explain why. Static source review is not proof that a MATLAB model or 北太天元 program executed.

# Handoff

Provide this Skill's report for workflow-orchestrator scheduling; do not invoke another Skill or alter its state.

- For code-reviewer: provide actual .m code, script or function entry, confirmed plan and revision, authorization references, real runtime and dependency evidence, inputs, outputs, validation findings, native errors, Warnings, and applicable compatibility limits.
- For result-report-generator: provide actual success, failure, NOT RUN, exploratory effects, preserved earlier attempts, and source locations. Do not write final paper claims or hide failed exploration.
- For BLOCKING_ERROR: identify the blocked operation, task and item IDs, actual missing or conflicting authorization, runtime, data, or summary-contract evidence, available genuine outputs and logs, impact, proposed owner, and corrective evidence needed.
- State explicitly when a current canonical summary is absent because publication was blocked. Do not present a planned path as an existing artifact.
- Do not clear a block by changing requiredness or fabricating evidence. Wait for the corresponding genuine correction or explicit human decision.
- Preserve existing failed or unexecuted attempts when execution later becomes possible; a later successful rerun does not erase them.
