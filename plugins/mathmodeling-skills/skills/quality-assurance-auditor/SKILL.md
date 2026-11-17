---
name: quality-assurance-auditor
description: Perform the final submission-level audit of mathematical-modeling workflow integrity, evidence quality, anti-fabrication, paper coherence, figures, references, and contest readiness after consistency and completeness audits pass.
---

# Preconditions

- `rigor_profile` is `submission`.
- All Qx reached G5.
- Final consistency and completeness audits exist.

# Audit Dimensions

1. **Workflow integrity**
   - G1–G5 passed per Qx.
   - Human judgments trace to the decision ledger.
   - Main/baseline/fallback execution respected approved scope.

2. **Evidence integrity**
   - No fabricated data, references, experiments, metrics, or figures.
   - Main claims trace to frozen numbers and robustness evidence.
   - Limitations and uncertainty are visible.

3. **Method quality**
   - Baseline is usable.
   - Assumptions, units, objectives, constraints, and solution steps are coherent.
   - Output concentration/degeneracy and failure triggers were addressed.

4. **Paper quality**
   - Problem, method, results, and conclusions align.
   - Claims are proportional to tested comparisons.
   - Human-owned physical meaning and contribution are present.

5. **Presentation**
   - Required figures/tables exist and passed render checks.
   - Figure types are used correctly.
   - References are real, complete, and consistently cited.
   - AI-use disclosure follows the current contest profile and verified rules.

# Independent Final Evidence

- Start from the actual original problem and attachments/version, not only manifests or passing earlier audits. Reconcile original requirements/task IDs, supported parse/parent manifests, confirmed current plan, real execution/results and substantive paper answers. Missing original tasks or unresolved sources are concrete gaps/COVERAGE_UNVERIFIABLE, not automatic coverage.
- Verify current complete-plan confirmation and exact historical content linkage using actual effective human decisions. G2.5, a version label, new digest or generic continuation is insufficient. Review four-category requiredness and check that all required validation has actual implementation/execution/input/script/log/output/metric/criteria evidence; fit/Probe PASS/code existence is insufficient.
- Check applicable R2 contiguous/random missingness evidence separately; R3 fit/rolling/independent evaluation honestly distinguished; R4 sensitivity versus required uncertainty and limitations. Do not impose universal designs or repeat experiments yourself. Technical reviewers and Robustness Checker retain their own responsibilities.
- Verify Exempt's actual specific human authority, original task, scope, impact, disclosure and supersession. Keep it distinct from Completed and unresolved key requirements; it never automatically passes G6. Conditional means an agreed objective actually met with disclosed allowed limits, not hidden incompleteness. Unauthorized scope reductions cannot be accepted.
- R5 checks must use actual full text and deliverables: required sections/answers, placeholders/fragments/template residue, abstract/body numbers/parameters/conclusions, formula/table/figure/reference completeness, and necessary actual DOCX/PDF post-export evidence. R6 requires real figure/result origin, values/units/axes/captions/references and render evidence, not just filenames.
- Distinguish real success, executed failure, unexecuted NOT RUN, insufficient evidence and workflow BLOCKING_ERROR without adding JSON enums. Preserve native failures, original Warnings and provenance, partial artifacts/reruns and exploratory effects; Warning or optional exploration failure alone does not automatically invalidate fulfilled requirements, but unresolved material effects must be assessed and disclosed.
- Inspect currentness and unresolved findings in actual Consistency and Completeness reports, then inspect canonical sources independently. Do not trust a PASS alone or certify their full remit by substitution. QA begins after those audits; its own absence must not be required as a prerequisite for producing them.
- Keep actual PASSED/FAILED/NOT_RUN QA verdicts and paper/qa_report.md path. A passing report must have the actual explicit Verdict: PASSED line required by the packager; a nonpassing report must have its truthful existing verdict and no stale/quoted passing verdict line. Preserve actual QA Schema version/fields when one is used; do not apply it to Completeness or create new states.
- Only Orchestrator evaluates G6/manifest flags. Preserve existing QA reporting/recommendation authority, not an ability to edit Gates, ledgers, schemas, summaries, other Skill outputs or frozen results. Report affected task/claim/Gate, actual evidence, repair owner, safe independent work and re-entry conditions; do not repair issues within QA or loop unrelated tasks.

# Workflow

1. Read the two earlier audits and unresolved blockers.
2. Sample canonical sources directly; do not trust summaries alone.
3. Record blocking and nonblocking findings with artifact paths and repair owners.
4. Save `paper/qa_report.md`.
5. Set verdict:
   - `PASSED`
   - `FAILED`
   - `NOT_RUN`

# Rules

- Do not approve on partial audits.
- Do not use artifact count or bullet count as a proxy for quality.
- Do not repair issues inside QA.
- Do not hide uncertainty or downgrade a blocker silently.
- Do not claim compliance with time-varying contest rules without verification.

# Verification

- All five audit dimensions were evaluated.
- Blocking findings are explicit and actionable.
- QA verdict agrees with consistency/completeness verdicts and sampled evidence.
- Final assembly is recommended only when all three audits pass.
