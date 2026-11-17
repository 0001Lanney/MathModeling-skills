---
name: problem-classifier
description: Classify each parsed mathematical-modeling subquestion by required output and structure, surface ambiguous framing trade-offs for human choice, and record primary/secondary task types without selecting algorithms.
---

# Preconditions

- `planning/parse/problem_parse.json` exists and maps every Qx to an output.
- Material framing ambiguities are visible.

Read legacy parse paths only during migration.

# Task Types

- evaluation/ranking;
- prediction/estimation;
- optimization/decision;
- mechanism/dynamics;
- classification/clustering;
- graph/routing/network;
- simulation/scenario;
- descriptive/inference;
- mixed.

Detailed cues are in `references/task-type-guide.md`.

# Workflow

1. Classify from the required output, decision structure, constraints, and relationships—not keywords alone.
2. Assign:
   - primary type;
   - optional secondary type;
   - confidence;
   - evidence from the parse;
   - consequences for validation and deliverables.
3. Identify mixed or ambiguous framings that would change what the team can claim.
4. For a load-bearing ambiguity, invoke one choice card explaining consequences. Do not silently settle it.
5. Save `planning/classification/problem_classification.json`.
6. After a genuine human framing answer, hand the exact answer and evidence to workflow-orchestrator for modeler-decision-logger capture in the existing methods/Qx/qx_decisions.jsonl or relevant global/pre-Qx planning/framing_decisions.jsonl. Distinguish the human answer, the actual append-only Logger record, and its currently effective authorization. Set or cite framing_decision_id only after verifying a genuine matching effective decision_id in the supported ledger; otherwise leave its existing nullable representation unfilled and report the pending or unverifiable record through Handoff. Do not fabricate or directly append an authorization record, or invent a decision type to make the framing appear approved.

# Output Contract

```json
{
  "schema_version": 1,
  "subquestions": [
    {
      "id": "Q1",
      "primary_type": "evaluation",
      "secondary_type": null,
      "confidence": "high",
      "evidence": [],
      "required_validation": [],
      "framing_decision_id": null,
      "risks": []
    }
  ]
}
```

# Coverage and Validation Advice

- Check original-task/source identity against the actual parse, required outputs, constraints, data characteristics, and success criteria. Do not classify only existing manifests and thereby omit an original requirement. Report missing or ambiguous mappings as COVERAGE_UNVERIFIABLE with source location and repair owner; Parser resolves extraction and IDs.
- Preserve the existing task types, primary/secondary prioritization, JSON example/schema_version: 1, fields, and classification output path. Use evidence/risks/required_validation only with their existing meanings; no new taxonomy, IDs, fields, enums, or manifest updates.
- Explain data needs and applicable validation consequences from the required output: interpolation may need distinct contiguous/random missingness checks; prediction separates fit/rolling/independent evaluation; optimization needs feasibility; ranking may need weight/rank stability; dynamics may need equilibrium/stability/boundary checks; learning requires leakage/generalization checks; estimation may need uncertainty. State applicability and missing data rather than imposing all checks or invented thresholds.
- Treat required_validation as an existing classification-level field, not as an approved Required Validation Experiments list or proof of execution. Distinguish validation obligations explicitly stated by the original problem from classification-derived applicability recommendations, using actual source evidence and only representations supported by the existing contract. Do not silently promote a recommendation to requiredness; when the legal field representation cannot distinguish the two reliably, disclose the distinction and unresolved scope in Handoff rather than inventing JSON fields or claiming approval. Analyzer designs the four-category code plan and acceptance criteria; the human confirms its current complete content before Generator execution. G2.5 or classification approval cannot substitute for that confirmation.
- Do not choose main/baseline/fallback, downgrade original requirements, grant Exempt, declare validation successful, or interpret a probe PASS as formal validation. Read real human framing evidence without assuming optional fields or undocumented decisions; refer unverified scope/authorization through Handoff to Orchestrator.
- Include source task/output links, chosen type/evidence, data limitations, validation applicability, unresolved human trade-offs, and missing information in a compact Handoff. Safe independent classification can continue where facts are reliable; no unsupported full-coverage or Gate approval.

# Rules

- Do not propose or choose methods.
- Do not classify only from nouns such as “forecast” or “optimal”; verify the required output.
- A subquestion may be mixed, but avoid listing many types without prioritization.
- Human framing is required when alternative classifications lead to materially different outputs or claims.
- Do not create a long taxonomy report when the JSON record is sufficient.

# Verification

- Every Qx has one primary type.
- Mixed/secondary types are justified.
- Classification evidence resolves to the parse.
- Ambiguous framing is human-confirmed or remains a blocker.
- No algorithm selection leaked into classification.

# Reference

- `references/task-type-guide.md`
