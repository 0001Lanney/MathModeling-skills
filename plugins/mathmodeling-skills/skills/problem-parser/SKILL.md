---
name: problem-parser
description: Parse a mathematical-modeling problem into goals, objects, data, constraints, outputs, subquestions, dependencies, variables, relationships, and human-confirmed success criteria before any method selection.
---

# Purpose

Produce a model-neutral problem contract. Do not start from favorite algorithms or infer missing attachments.

# Inputs

- complete problem statement and attachments list;
- contest rules and required deliverables;
- user clarifications;
- existing parse when revising.

# Workflow

1. Record source files and missing referenced material.
2. Extract the global objective and each Qx verbatim enough to preserve intent.
3. For each Qx identify:
   - goal;
   - objects/entities;
   - inputs and data;
   - decisions or unknowns;
   - hard and soft constraints;
   - required output and format;
   - evaluation/success criteria;
   - dependencies on other Qx;
   - uncertainty and ambiguity.
4. Separate:
   - statement facts;
   - observations from supplied data;
   - proposed relationships;
   - assumptions requiring human judgment.
5. If output form or success criteria are materially ambiguous, invoke one choice card. Do not choose the framing silently.
6. Save:
   - `planning/parse/problem_parse.json`
   - an optional concise `planning/parse/problem_parse.md` only when a human-readable view is useful.
7. Compare the parsed task set with manifest Qx entries and report missing or mismatched links. Do not modify execution status, current_gate, allowed flags, or final_assembly; workflow-orchestrator owns execution-state reconciliation.

# JSON Contract

```json
{
  "schema_version": 1,
  "problem_source": [],
  "global_goal": "",
  "objects": [],
  "data_inventory": [],
  "global_constraints": [],
  "subquestions": [
    {
      "id": "Q1",
      "statement": "",
      "goal": "",
      "inputs": [],
      "unknowns_or_decisions": [],
      "constraints": [],
      "required_outputs": [],
      "success_criteria": [],
      "dependencies": [],
      "proposed_relationships": [],
      "ambiguities": []
    }
  ],
  "missing_material": [],
  "human_decisions_needed": []
}
```

# Original-Task Coverage and Scope

- The actual original problem and genuine clarifications determine task scope. Record every independently verifiable original-problem output and any explicitly required validation objective before method choice, without designing method-specific experiments or assigning their requiredness. Existing manifests cannot define or shorten the original task set. Do not infer original requirements from old Qx files; leave method-specific validation design and requiredness to the Analyzer's plan and genuine human confirmation.
- At initial parsing, establish the original source/version/locator and excerpt, actual task_id where supported, and parse entry using evidence currently available. Preserve links to a parent manifest_entry when one already exists. Later approved-plan, code, result_artifacts, and paper_section links are checked and completed by their responsible downstream Skills as those artifacts become available; their absence during initial parsing is not by itself a Parser failure. Keep the eventual traceability chain auditable through actual supported fields and artifacts. A fine-grained ID such as Q1.R1 may map to parent Q1; do not create extra manifests or new JSON fields merely for granularity.
- The existing planning/parse/problem_parse.json contract and example remain unchanged. Use its statement/required_outputs/success_criteria/dependencies where sufficient; use an existing Markdown mapping when useful. Supplement planning/parse/problem_parse.md only when sources, supported parse fields, and existing artifacts cannot unambiguously represent fine-grained IDs, multiple independently required outputs, source excerpts, or evidence links. Long source text or a fine-grained ID alone does not require redundant Markdown.
- Compare all original requirements with parsed tasks and manifest entries, including requirements without manifests. Report source/requirement, actual or unresolved task_id, expected versus actual mapping, missing material, impact, and responsible owner. Resolve material ambiguity through the existing human-framing mechanism; do not silently invent IDs, delete tasks, or rewrite scope.
- Missing/incomplete/unreliable source material is COVERAGE_UNVERIFIABLE in the report/Handoff, not proof of full coverage or a new JSON status. Request actual missing material; preserve independently established facts and allow unrelated safe work, while withholding a complete-coverage claim.
- Read relevant existing methods/Qx/qx_decisions.jsonl, substituting the real Qx and qx filename. Read planning/framing_decisions.jsonl only when present and relevant to a global/pre-Qx decision. An irrelevant uncreated ledger is not an error; claimed or relied-on authorization requires verification. Missing/unreadable evidence proves neither valid authorization nor that the user never authorized. Do not create/search an alternative exemption ledger.
- Scope changes or Exempt require specific genuine human authority, actual task IDs, reason, scope, effects, disclosure, and effective supersession. Trace real existing decision fields/references; do not add mandatory task_ids/authorization_text fields or write the ledger. Keep original exempted requirements visible; Exempt is not Completed or automatic G6 approval.
- Respect decided_at's existing ISO-8601 ledger-append-time meaning. Do not substitute it for actual authorization time. Preserve genuinely evidenced authorization-time provenance only using existing supported representations; otherwise state uncertainty in Handoff, without rewriting human rationale, inventing fields/timestamps, or requiring a fixed marker.
- Parser establishes model-neutral requirements, not required-method choices, verification results, or plan approval. Classification, method selection, Analyzer's four-category plan, human confirmation, and execution remain separate responsibilities. Handoff concrete source/mapping gaps to Orchestrator; report-only labels do not extend JSON enums.

# Rules

- Parse before classifying.
- Do not name or recommend methods.
- Do not fabricate data, fields, equations, causal relationships, or evaluation criteria.
- Preserve units, time ranges, populations, and output formats.
- A proposed relationship must be labeled as proposed until human-confirmed or evidence-supported.
- Ask only about ambiguities that change the downstream problem.

# Verification

- Every subquestion maps to a required output.
- Constraints and dependencies are explicit.
- Missing attachments and ambiguities are visible.
- Facts, proposals, assumptions, and decisions are separated.
- Human-owned success criteria are confirmed or remain a blocker.
