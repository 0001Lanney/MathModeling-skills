---
name: completeness-auditor
description: Audit whether the semantic evidence required by the active lean or submission profile exists and is current, without requiring one verbose artifact per skill or an arbitrary number of pass bullets.
---

# Purpose

Check deliverable evidence, not whether every invoked skill left a ceremonial report.

Audit original-task coverage and the semantic evidence actually delivered. Do not solve models, design or execute missing experiments, generate results, rewrite the paper, or replace independent code, robustness, consistency, or QA review. Report concrete gaps to workflow-orchestrator; do not directly invoke repair Skills or change their state.

# Lean Checks

Per active Qx, require as applicable:

- manifest;
- method card;
- human decision ledger;
- risk-probe summary;
- latest run summary.

Lean completeness does not require final reports, freeze, paper, or G6 artifacts.

Apply requirements only when due for the requested stage. Check the current code plan, genuine confirmation, language review, and required execution evidence when that stage depends on them; lean does not waive required validation or approval. A first candidate plan awaiting confirmation may be prepared and reviewed without treating its ordinary pending_confirmation as failed historical authorization. Do not require a nonexistent approved plan, successful run summary, or final paper before safe early-stage evidence inspection.

# Submission Checks

Per Qx require:

- final method explanation;
- current language review JSON with all required named checks passing;
- final result analysis;
- robustness report;
- solution package;
- current frozen numbers;
- paper section and referenced figures.

Globally require symbol table, assumptions, references, consistency audit, completeness audit, and QA report.

This is the final-submission inventory, not a circular prerequisite for producing this audit. Check applicable symbols, assumptions, references, and deliverable completeness within this Skill's remit. Record other final-audit presence/currentness and the outstanding G6 dependency separately: do not require a prior copy of this audit or a future QA verdict to audit completeness. QA follows consistency/completeness; Orchestrator still requires all three independent valid audits before G6/final assembly. Producing a peer audit is not a reason to invent its passage or repeatedly rerun this audit when its materially cited evidence has not changed.

# Workflow

1. Read `rigor_profile`.
2. Establish independently verifiable original-task scope, then reconcile problem_parse, expected Qx manifests including missing entries, and actual artifacts; manifests describe execution, not the universe of required tasks.
3. Check required artifacts and semantic fields.
4. Check staleness only against materially cited evidence.
5. Accept documented legacy equivalents during migration.
6. Save `paper/audits/completeness_audit.md` only in submission/final mode.
7. Return the actual scope, item findings, unresolved evidence, completion facts, and repair owners through Handoff. In lean or scoped work, use a compact digest rather than a ceremonial new report.

## Original-Task Coverage and Mapping

- Read the actual original problem, relevant attachments and their identity/version, genuine user clarifications, problem_parse, manifests, the approved current plan, and canonical code/results/paper appropriate to the stage. The original problem is the final scope authority; problem_parse is the working list and manifests are execution records. Independently compare every verifiable original requirement against the existing task list, including requirements that have no manifest or artifact.
- Trace task_id, source_reference or actual source locator, original requirement/excerpt, parse entry, manifest_entry, approved required method/validation, code/execution evidence, result_artifacts, paper_section, completion fact, and missing requirement/impact. These are logical audit links in existing supported artifacts or the report, not new JSON keys. A fine-grained task such as Q1.R1 may link to its parent Q1 manifest; do not demand a separate manifest per requirement.
- Reuse equivalent evidence in original sources, supported parse fields, plans, and existing artifacts. Require supplementary mapping only when those cannot unambiguously express the task/output/evidence relationship; do not require duplicate Markdown or a fixed extra file because an ID is fine-grained or an excerpt is long. If numbering or source meaning is uncertain, name the actual source excerpt and unresolved identifier, and hand the mapping issue to problem-parser through Orchestrator; do not invent IDs or rewrite scope to remove gaps.
- For each gap report the actual or unresolved task_id, source path/version/locator and requirement, expected versus actual parse/manifest/plan/code/result/paper link, missing evidence, affected conclusion or Gate, and repair owner. An absent original source, incomplete material, or unreliable extraction is COVERAGE_UNVERIFIABLE: identify exactly what is unavailable and request Parser/user clarification. It is neither proof of full coverage nor Exempt. Withhold only coverage-dependent conclusions while safe independent work continues.
- Before final completeness approval, locate a substantive paper response and genuine result evidence for every required original delivery. A filename, copied question heading, plan entry, or manifest PASS cannot stand in for an actual answer. Unbuilt manifests and omitted tasks remain gaps rather than disappearing from the audit.

## Confirmed Plan and Required Validation

- Read the actual Python code/Qx/qx_code_plan.md or MATLAB code/matlab/Qx/qx_code_plan.md when due, its actual revision/content, and the relevant effective human record. Verify real decision_id, decision_type, status, decided_by, choice, rationale, evidence_refs, and applicable supersedes/revocation, with task scope and exact approved plan content traceable through supported references. A genuine recorded digest, immutable revision, or other verifiable historical linkage is needed; a newly computed SHA-256, version label, mutable path, G2.5 method choice, or generic permission to continue alone is not full-plan confirmation.
- Distinguish Required Main Model, Required Baseline, Required Validation Experiments, and Non-required Exploratory Methods from the confirmed plan. Verify IDs, task linkage, requiredness, objectives, inputs, outputs, execution conditions, acceptance criteria, and evidence locations. The baseline must complete the real task comparably; diagnostic_reference is not a usable baseline. Do not define requiredness yourself, add experiments to reach a count, or downgrade approved requirements because of cost, time, complexity, missing environment, or failure.
- For each confirmed required validation, check task_id/validation_id, original/plan requirement, applicable target and design, data requirements, implementation, actual execution record, input data and executed script, logs, real metrics or observable outputs and units, acceptance finding, evidence paths, and impact on the original answer. No plan, existing code, expected result, risk-probe PASS, training fit, main-model success, unrelated favorable metric, or optional exploration substitutes for this evidence.
- Distinguish generated code, actual execution, valid evidence, and criteria satisfied. Report unexecuted work as NOT RUN with its reason; executed failure with real errors and retained artifacts; completed execution that misses criteria as validation failure, not a fabricated runtime error; insufficient evidence as INCONCLUSIVE or an existing compatible factual description. These are audit facts, not new JSON enum values.
- Cross-check summary/review claims against real inputs, scripts, outputs, metrics, tables, figures, and approved conditions. Keep failures, earlier attempts, reruns, native errors, original Warning text, method/validation association, and evidence locations. Empty errors is not success; a Warning alone is not failure. Assess its actual risk and disclose unresolved material effects rather than silently dropping it.
- Non-required authorized exploration that fails or is not run does not alone make an original required task incomplete or veto a satisfied submission. Preserve its record and effects; material impacts on method selection, comparisons, main conclusions, or credibility need disclosure in experiment analysis/limitations, while immaterial exploration may remain in appendix or experiment records. Do not describe failed exploration as successful or let a better exploration result automatically replace a required main method.
- A confirmed required-method replacement needs actual trigger evidence, an explicit human decision authorizing the specific activation/replacement and plan scope, an updated confirmed plan, and traceable supersession with original failure evidence retained. Prelisting a fallback or firing its trigger alone is not authorization. Report missing authorization; do not activate alternatives or amend the ledger yourself.

## R2–R4 Evidence Completeness

- R2: when original requirements or the approved applicable plan require contiguous-missing and random-missing backtests, inspect each design, actual mask/data, execution, result, and paper response separately. Random masking cannot satisfy a required contiguous-gap check. Do not require these experiments for an inapplicable task.
- R3: distinguish in-sample fit, rolling validation, and independent test evidence. Check that the particular test required by the problem/confirmed plan was actually performed and represented truthfully in the report/paper; fit is not prediction testing, and rolling validation is not automatically an independent test. Do not impose an independent test set on every problem.
- R4: distinguish point estimates, sensitivity perturbations, and uncertainty evidence required by the original task. Inspect the genuine source for applicable intervals, resampling, scenarios, or justified uncertainty boundaries, and any disclosed inability to quantify. Sensitivity alone or one perturbation is not required uncertainty quantification; do not mandate Bootstrap, Monte Carlo, or another uniform design.
- Inspect coverage and delivered evidence; do not take over Analyzer's plan design, Generator's implementation/execution, Reviewer's technical validation, or Robustness Checker's experiment/evidence assessment. Escalate missing design or unclear applicability to the responsible owner rather than inventing thresholds, data, proof, or findings. AI self-derivation alone is not independent mathematical proof.

## Exempt Authorization

- Read actual methods/Qx/qx_decisions.jsonl for Qx decisions, substituting the real question and filename. Read planning/framing_decisions.jsonl only when present and relevant to global/pre-Qx authorization; global and Qx scopes are not interchangeable. An uncreated irrelevant ledger is not an error. If a claimed or relied-on decision cannot be read/verified, report authorization unverifiable, neither valid approval nor proof that approval never occurred. Do not search for/create an alternative ledger.
- Verify Exempt against a genuine explicit human decision: original task ID/requirement, actual decision content/type/status/person, reason, specific scope, impact on results/paper, disclosure requirements, Gate/G6 consequences, and relevant decision_id/evidence/supersedes or revocation. Use real existing choice/rationale/evidence_refs and supported references; do not require undeclared task_ids, authorization_text, authorization_ref, or a new decision type/Schema field.
- Do not grant Exempt because data or a runtime is missing, work is difficult/expensive, time is short, code failed, the user is silent, or another model has similar output. Only the specific genuine authorization applies; do not enlarge it or fabricate human wording, approval evidence, timestamps, or retrospective approval hashes. Do not create or modify any ledger; Logger records genuine human decisions through Orchestrator.
- Keep decided_at's existing ISO-8601 and formal ledger-append-time meaning. Do not misrepresent it as the actual human authorization time. Preserve independently evidenced authorization-time provenance only through an existing supported representation; otherwise disclose uncertainty in Handoff without inventing or rewriting human rationale, adding fields, or imposing a fixed marker. Unknown precise authorization time alone does not invalidate otherwise explicit traceable authorization.
- Retain every Exempt original requirement in the final coverage table with its genuine authorization and disclosed limitations in final paper/materials. Exempt is not Completed and does not automatically permit G6. Authorized continuation or a reduced delivery scope must be reported as such, never as completion of unmet original requirements; no passing final original-task completeness verdict while such required deliveries remain unmet.

## Paper, Results, and R5–R6

- In submission/final scope, check each original requirement's substantive body response, methods within approved scope, genuine executed results, traceable metrics/units/parameters/tables/figures, and disclosed important limits. Results without a paper answer and paper claims without real evidence remain gaps.
- R5: identify missing required sections, unanswered original tasks, missing key conclusions/figures/attachments, unfilled placeholders, fragments/template text, undisclosed material defects, and major abstract/body contradictions. Check that numbering, references/citations, and required export deliverables are present; when final DOCX/PDF checks are required, inspect actual post-export evidence rather than assuming the source file proves export quality.
- R6: check that needed and cited image files are actually delivered, have genuine result-source links, and have complete captions/numbering/references. File presence alone does not establish a correct figure. Record known caption/unit/axis/result conflicts; hand detailed numerical and visual consistency to the appropriate figure producer, Consistency Auditor, or QA.
- This Skill reports completeness gaps and provenance. Writer/Polisher handle authorized writing/format/language repair, Consistency Auditor checks cross-media agreement, and QA independently assesses final quality. Do not rewrite claims, manufacture missing data/results/figures/references, perform their repairs, or count an upstream PASS as their independent evidence.

# Status

- `PRESENT`: required evidence exists and is current.
- `MISSING`: required evidence absent.
- `INSUFFICIENT`: artifact exists but required semantic fields/checks are missing.
- `STALE`: cited material evidence changed after approval/review.
- `NOT_APPLICABLE`: justified by task/profile.

Keep these five evidence-item statuses and their meanings; the original Skill declares no JSON Schema, schema_version, or dedicated machine verdict format. Do not import QA's JSON Schema or add enum values, required keys, or a state file. NOT_APPLICABLE is for genuinely inapplicable requirements, not a substitute for failure, missing evidence, or a human exemption.

In audit narrative or another already-supported representation, separately describe task completion:

- Completed: all relevant original delivery requirements have complete, credible actual evidence, including the paper response when due.
- Partial: some necessary requirements are met, with identifiable remaining gaps.
- Incomplete: major delivery requirements are absent or not met.
- Exempt: a specific genuine human exemption is verified; the original requirement remains visibly unfulfilled rather than Completed.
- Conditional: the agreed delivery objective has actually been met and permitted limitations are explicitly disclosed. An unmet key original requirement stays Partial or Incomplete; Conditional must not hide it.

These are task facts, not additions to the five evidence-item statuses or any JSON enum. Report unavailable/insufficient evidence with the existing lawful item status plus narrative. Do not infer completion from a file, generated code, a successful process, artifact count, or absent source material. A stage-limited evidence check is a scoped finding, not a Completed claim for original deliveries that remain unmet.

# Rules

- Do not require `≥5` prose pass items.
- Do not require a report just because a skill ran.
- Do not mark a decision stale for unrelated code, formatting, or file changes.
- Do not treat legacy artifact count as proof of semantic completeness.
- Do not repair artifacts during audit.
- Do not modify manifests, Gate/allowed flags, decision ledgers, schemas, run summaries, historical results, another Skill, or the packager. Report findings for Orchestrator scheduling; this Skill cannot approve the entire workflow or substitute for either final peer auditor.
- Preserve each actual producer's JSON structure, version, roles, legal statuses, review paths, and original evidence. Four plan-category labels do not create run-summary role enums. MATLAB Reviewer's runtime NOT_RUN allowance is not a new Python-review/run-summary/robustness enum; Robustness Summary remains PASS / CONDITIONAL / FAIL with no invented schema_version.
- Unknown/illegal status types, irreconcilable top-level/method status conflicts, or missing authoritative evidence require a scoped BLOCKING_ERROR when they prevent a defensible completeness conclusion. Keep actual fields, values, paths, evidence, affected claims, owner, and repair requirement. Do not let top-level success erase method failure or fabricate a success/FAILED/NOT RUN JSON value.
- When lawful canonical run-summary/review publication is withheld for a real contract gap, record the artifact's actual absence and reason with compatible item status and Handoff facts. Do not require a fictitious summary before inspecting source/inputs or give runtime approval based on static inspection. Unsupported facts belong in report/Handoff; do not publish incompatible JSON or falsely passing audits.
- The deployed restricted packager reads Legacy summaries and supported schema_version: 1 methods[] file views, including current-plan identity and output/figure scope checks. Structural or completeness checks do not prove publication or final assembly completed: C2_UNQUALIFIED disables that operation, and it must not be reported as completed. Exempt remains distinct from Completed and does not automatically satisfy G6. Name the affected packaging operation and actual fields/evidence; do not modify package_submission.py or summaries to make this audit pass.
- Scope a block to the conclusions/operations dependent on the missing evidence. Identify safe independent collection/static diagnosis/repairs, responsible owner, and concrete re-entry evidence. Do not make every Qx repeat an audit for an unrelated local problem, require full-workspace checks because several files changed, or rerun without changed material evidence.
- Preserve lean/submission density and existing legacy equivalents without upgrading old method choices into current-plan approval. Do not invent universal experiments, mandatory per-item files, new Skills/Gates, an independent audit framework, or a global task/exemption state system.

# Verification

- Requirements match the active profile.
- Every gap names the missing evidence and producer/owner.
- Staleness links to a material changed source.
- Final verdict is `PASSED` only when all submission requirements are satisfied within this auditor's completeness remit, with original-task coverage verified and required deliveries actually met. Other final-audit availability remains separately necessary for G6 as specified in Submission Checks.
- Original-task scope is checked independently of existing manifests; each missing or unresolved link has its source, affected conclusion/Gate, and repair owner.
- Current-plan confirmation, four-category identities, required execution/validation evidence, and retained failures/Warnings match actual sources.
- Exempt authorization and disclosed scope are genuine; Exempt and Conditional do not conceal unmet original requirements.
- Report claims, actual figures/exports, and evidence-item statuses agree with the genuine deliverables. Safe static checks are not reported as execution or R1–R6 test results.

# Output and Handoff

Preserve the primary submission/final Markdown output paper/audits/completeness_audit.md; use a compact conversational digest otherwise. The actual packager and Orchestrator require an explicit Verdict: PASSED line for a passing completeness report. Emit that line only after this Skill's complete original-task/evidence checks pass; it does not authorize G6 or certify the other auditors.

The original completeness contract explicitly defines PASSED as its passing verdict but does not define a closed nonpassing verdict enum. For gaps or unverifiable evidence, use the existing lawful evidence-item statuses and clear nonpassing narrative/Handoff; do not silently import QA's FAILED/NOT_RUN or invent a machine verdict. Never include a passing verdict line as a quoted example, stale carry-over, or negated template in a nonpassing report. If an actual consumer requires an unsupported nonpassing value, identify that interface gap and withhold incompatible publication rather than force a false verdict.

Handoff to workflow-orchestrator: provide the actual original source/version, audited profile/stage, task coverage and unresolved IDs/source locators, gaps across parse/manifest/plan/code/validation/results/paper, evidence paths and contradictory values, genuine Exempt decisions/scope/disclosure/G6 impacts, required NOT RUN/failed/inconclusive work, repair owner and priority, affected Gate/conclusion, safe independent work, needed human decisions, and specific re-entry evidence. Do not directly schedule repairs, change peer states, or claim final assembly approval.

QA must still inspect actual deliverables and original coverage independently; Consistency remains responsible for cross-media agreement. An explicitly authorized early-packaging waiver is not G6 approval or a reason to label incomplete original tasks complete.
