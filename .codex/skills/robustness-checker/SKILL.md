---
name: robustness-checker
description: Design and run risk-targeted robustness, sensitivity, error, and baseline checks for an approved mathematical model, emitting compact machine evidence in lean mode and a final report in submission mode.
---

# Purpose

Test the claims most likely to fail. Choose checks from the model's assumptions and decision risks rather than filling a generic checklist.

# Preconditions

The existing prerequisites below apply before experimental execution and execution-supported robustness conclusions. Missing prior runs or a lawful run summary does not prevent safe authorized static inspection or drafting recommendations; report the actual missing evidence and do not claim an unexecuted experiment passed.

- Approved main and usable baseline executed.
- Run summary, method card, probe summary, and relevant outputs exist.
- Claim or decision to be tested is known.

## Plan, Scope, and Authorization

- Read the original problem, available problem_parse task mapping, actual current `code/Qx/qx_code_plan.md` or `code/matlab/Qx/qx_code_plan.md`, method card, probe evidence, relevant decisions, and genuine execution artifacts. Use original requirements as the coverage authority; missing source material is COVERAGE_UNVERIFIABLE, not evidence that existing Qx entries cover everything or that a task is exempt.
- Read relevant `methods/Qx/qx_decisions.jsonl`, replacing Qx and the qx filename component with the real question. Read `planning/framing_decisions.jsonl` only when it exists and is relevant to a global or pre-Qx decision. An irrelevant absent ledger is not an error; a relied-on unreadable record makes authorization unverifiable, without proving either approval or that approval never happened.
- Distinguish G2.5 method choice from explicit confirmation of the current full plan and robustness scope. Verify task and item identities, requiredness, execution conditions, actual choice, human ownership, approval evidence, and applicable supersession/revocation. Link exact current content to historical confirmation with genuine recorded digest or reliable immutable content evidence; a freshly computed SHA-256, version label, or mutable path alone does not prove prior approval.
- Reconcile Required Main Model, Required Baseline, Required Validation Experiments, and Non-required Exploratory Methods against the confirmed plan. Audit every confirmed required validation's actual completion; exploration cannot replace required validation or be silently promoted to required work.
- Execute only approved applicable robustness checks under authorized inputs, runtime, and side-effect conditions. Suggest out-of-scope experiments through Handoff for human confirmation; do not add required experiments, alter designs or requiredness, delete baseline/validation, switch models, or activate fallback yourself.
- Candidate designs and safe static advice may be prepared before a first code plan exists; do not demand confirmation of a nonexistent plan or treat normal pending confirmation as an authorization error. Such advice is not an approved executable plan. Analyzer prepares the plan; user confirmation precedes affected execution.
- A required check that is unexecuted, failed, or unsupported by necessary evidence remains explicitly unmet; strong unrelated metrics cannot compensate. If a missing original requirement is absent from the plan, report the mismatch for Analyzer/user consideration without editing the plan.
- An unperformed non-required suggestion alone does not establish overall incompleteness or a workflow blocker. Record its potential value or limitation; do not turn optional experiments into mandatory work or Gate conditions. All proposed validation techniques remain conditional on task relevance and confirmed scope.

# Workflow

1. Identify load-bearing assumptions and claims.
2. Select applicable checks:
   - parameter or weight perturbation;
   - alternate split or resampling;
   - seed stability;
   - outlier/missing-data treatment;
   - constraint/capacity perturbation;
   - baseline comparison;
   - output concentration/rank stability;
   - error and uncertainty analysis.
3. State perturbation ranges and why they are meaningful before interpreting results.
4. Run checks with fixed seeds where stochastic.
   - Use the evidence and applicability rules below for R2, R3, and R4 as relevant to the confirmed plan. A probe PASS, implemented code, actual execution, available artifacts, traceable evidence, and satisfaction of acceptance criteria are different facts.
5. Save compact metrics to:

`robustness/Qx/qx_robustness_summary.json`

6. In `submission`, also save:

`robustness/Qx/qx_robustness_report.md`

7. If the stability verdict affects method continuation or claim scope, prepare one evidence-linked choice card in Handoff for workflow-orchestrator scheduling and request faithful recording of the genuine human answer by modeler-decision-logger in the existing methods/Qx/qx_decisions.jsonl. Do not directly invoke another Skill or write the ledger.

## R2: Contiguous and Random Missingness

- For applicable interpolation or missing-data risks, distinguish contiguous gaps from random masking. For a contiguous gap, record actual length and location, affected trend/cycle/event, train/validation/test placement, imputation assumptions, performance under the window, and effects of other approved locations.
- For random masking, record the missing proportion, mechanism and assumptions, seed, actual repetitions, pre/post metrics, and conditions comparable to the contiguous-gap experiment. A random-mask experiment does not establish contiguous-gap robustness; when the plan requires both, verify separate execution evidence.
- Prevent leakage into held-out observations and fit imputation only with permitted information. Use genuine known observations for backtest error; do not fabricate unknown ground truth or metrics for naturally missing values. Record actual masks/windows and metric units through the evidence contract.
- A five-day gap is only a possible later R2 fixture, not a universal requirement. If data are not temporal and no contiguous-gap risk applies, explain inapplicability rather than imposing that experiment. Recommend additional designs without executing unapproved scope.

## R3: Fit, Rolling Validation, and Independent Testing

- Identify actual in-sample fitting, rolling/time-ordered validation, independent testing, and other appropriate external or holdout evidence. Trace true split boundaries, training, preprocessing, tuning, model selection, final evaluation, executed scripts, inputs, metrics, and artifacts; check leakage and reuse of evaluation information.
- Training MAE, RMSE, or R-squared is not automatically predictive test evidence. Rolling validation is not automatically independent testing; a repeatedly reused model-selection set is not untouched, and a file named test is not proof of independence.
- If the confirmed plan requires independent testing but only fitting and rolling-validation evidence exists, report the required independent test as unmet. Do not relabel either result as independent testing or claim required validation is complete.
- Do not require independent test data for every mathematical problem. When genuinely unavailable or inapplicable, disclose the limitation and assess its effect against original requirements and the confirmed plan; do not fabricate a split or treat AI self-review as independent mathematical evidence.

## R4: Sensitivity and Uncertainty

- Sensitivity describes response to parameter, input, weight, feature, or justified assumption changes. Record the actual perturbation range and its scientific/data/domain or confirmed-plan basis before interpretation; an arbitrary percentage is not automatically justified.
- Uncertainty concerns how input, parameter, model-structure, or stochastic uncertainty affects conclusions. Where applicable and approved, evidence may use confidence/prediction intervals, bootstrap, Monte Carlo, parameter posteriors, distribution changes, scenarios, or defensible bounds; these are choices, not a mandatory list.
- Distinguish point estimates, sensitivity magnitude, output ranges, quantified uncertainty, and supported claim boundaries. Sensitivity alone, one perturbation, or one point prediction does not establish uncertainty quantification or an evidenced uncertainty statement.
- If the task requires uncertainty reporting but materials contain only point estimates without intervals or uncertainty explanation, report the missing requirement and its impact. If the approved plan omits that original requirement, request plan review through Handoff rather than adding required work yourself.
- If uncertainty cannot be quantified or is inapplicable, state the reason and limitations without automatically declaring model failure; separately report any explicitly required criterion that remains unmet. The later R4 point-only fixture does not prescribe a particular statistical technique.

## Evidence and Actual Outcomes

- For each actual check, trace original task_id, method_id or validation_id, current plan and authorization scope, input data/version, perturbation object/design/range, applicable seed and repetitions, executed code, runtime, real outputs, metrics/units, comparable baseline, acceptance or interpretation basis, completion/failure reason, and effect on conclusions. These are provenance requirements, not new JSON fields.
- Distinguish designed, implemented, actually executed, artifacts available, evidence traceable, and confirmed criteria satisfied. File existence does not prove execution; successful execution does not prove robustness. Preserve contradictory results and the full approved range, not only the best-performing parameter.
- For applicable analytic arguments, identify the actual derivation, assumptions, and checkable evidence without claiming a numerical experiment ran. AI self-derivation or self-review is not independent mathematical proof.
- Use NOT RUN as the factual description of unexecuted work with its actual reason. Use FAILED only for genuine executed failure or a validation criterion actually not met, explicitly distinguishing those two meanings and retaining native errors or criterion evidence. INCONCLUSIVE describes insufficient evidence; none of these labels grants a new JSON enum.
- Preserve relevant Warning text, associated item and evidence location, errors, original failures, partial outputs, pre/post-repair evidence, rerun history, unexecuted work, and non-required exploration failures. A Warning alone is not failure, and an anomaly does not authorize deleting a method.
- Report the actual effect of failures and limitations on each affected claim. Do not fabricate data, metrics, runs, predeclared acceptance thresholds, or successful results to fill evidence gaps; disclose any genuinely exploratory post-hoc threshold as exploratory under the existing Rules.

# Summary Contract

Record:

- tested claim/assumption;
- input and result source paths;
- perturbation;
- metric and threshold if predeclared;
- observed value;
- status `PASS`, `CONDITIONAL`, or `FAIL`;
- limitation;
- fallback-trigger relevance.

## Existing Output and State Boundaries

- Keep the existing lean summary path and submission-only final-report path, formats, eight Summary Contract content items, and PASS/CONDITIONAL/FAIL status vocabulary. The original Skill declares no schema_version or concrete JSON key/type schema; do not invent one or add required keys, enum values, schema files, or a new result/state system.
- Use only actual supported representations for the existing content items and evidence references. Additional provenance and R2/R3/R4 findings belong in compatible existing records, the existing submission report when applicable, or Handoff text; they do not authorize expanding JSON.
- Assess PASS, CONDITIONAL, or FAIL only from genuine checks under stated criteria and disclosed limits. CONDITIONAL is not a substitute for missing execution evidence, and FAIL must not falsely imply a model ran when it did not.
- NOT RUN, FAILED, Warning, INCONCLUSIVE, BLOCKING_ERROR, COVERAGE_UNVERIFIABLE, and Exempt in this document are report facts or findings, not newly authorized summary status values. Do not import MATLAB Reviewer's runtime-dependent NOT_RUN exception into robustness JSON or copy the other Skills' schema_version.
- If the existing summary cannot legally express an actual finding or unexecuted item, retain genuine facts and report the specific interface gap through Handoff instead of fabricating PASS, relabeling it as CONDITIONAL/FAIL, dropping the item, or emitting incompatible JSON. For affected required work or execution authorization, explicitly report BLOCKING_ERROR; a non-required recommendation alone is not a blocker.
- Preserve historical records and real fields/types; do not rewrite run summaries, original results, another Skill, or the packager to force compatibility. If a lawful summary cannot be produced, state its absence and cause; do not claim a complete deliverable or invent summary numbers.

# Rules

- Do not run irrelevant checks merely to reach a count.
- Do not invent a threshold after seeing the result without labeling it exploratory.
- Do not convert stability metrics into the human confidence verdict.
- Do not create `robustness-checker_modeler_decision.md`.
- A failed robustness check is evidence for adjust/fallback/claim downgrade, not permission for AI to decide.

- Do not change the required main model, remove the required baseline, downgrade validation, add unapproved required work, alter the code plan, or act as a general code-syntax reviewer or paper writer.
- Do not directly invoke other Skills or change G1-G6, manifest, ledger, schema, or another Skill's state. Human continuation, replacement, confidence, and claim-scope decisions remain human decisions; workflow-orchestrator owns scheduling.
- A fallback recommendation needs genuine trigger evidence and a specific new human decision covering the affected method and updated plan scope, with traceable supersession, before any authorized replacement; preserve original failure evidence.
- Do not create a new Skill, Python audit framework, test platform, dependency, uniform mathematical-validation template, or alternative exemption ledger. Do not modify protected raw data or install dependencies to make checks pass.

# Verification

- Every major final claim has a supporting check or explicit limitation.
- Perturbations are justified and reproducible.
- Baseline and main comparisons remain metric-compatible.
- Concentration/degeneracy risks are revisited when relevant.
- Submission report sources its numbers from the summary and experiment artifacts.

- The existing supporting-check-or-limitation condition qualifies claims honestly; it does not complete an explicitly required but unperformed validation. Review required and optional scope separately.
- For requested Exempt handling, verify the existing genuine human decision, affected tasks, reason, authorization evidence, scope, and disclosures through designated ledger references. This Skill cannot grant Exempt; it is not Completed, not a passing check, and not automatic G6 approval. Missing coverage or authorization is not an exemption.
- Verify R2 missingness pattern and actual mask/window evidence, R3 split/selection independence, and R4 uncertainty versus sensitivity only where relevant and confirmed.
- Any unperformed execution or validation remains NOT RUN with its reason. This Skill reports evidence and gaps; it does not modify Gate status or paper claims.

# Handoff

The existing summary and submission report remain the deliverables under their original mode conditions; Handoff is this Skill's plain report, not a new JSON state file or compulsory duplicate artifact.

- Provide workflow-orchestrator with reviewed scope, original tasks, actual current plan and confirmation references, four-category requiredness, approved versus suggested checks, implemented/executed/unexecuted work, masks or windows, validation type, sensitivity versus uncertainty findings, genuine artifact paths, limitations, and affected methods/claims.
- For required missing/failed evidence or an execution-authorization block, identify the blocked operation, exact finding and failure nature, actual source fields/files, impact, proposed responsible party, corrective evidence, and any human decision needed. Do not infer whole-model failure merely from an unperformed optional suggestion.
- Request one evidence-linked choice card when method continuation or claim scope needs human judgment, and faithful decision recording by modeler-decision-logger through orchestrator scheduling; do not write, strengthen, or fabricate the human answer.
- Supply preserved failures, Warnings, NOT RUN work, contradictory results, and exploratory effects for downstream result-report-generator use; do not rewrite final claims or silently suppress an inconvenient experiment.
- Report unavailable or unverifiable original task coverage as COVERAGE_UNVERIFIABLE and request source material; do not presume completion or Exempt. Any work continuation under a genuine exemption remains for the existing authorized workflow to decide.
