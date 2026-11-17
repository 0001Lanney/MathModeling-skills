---
name: modeler-decision-logger
description: Faithfully append a human modeler's choice and rationale to one canonical per-subquestion JSONL decision ledger. Use after a choice card is answered or when migrating legacy decision artifacts; never originate or improve the decision.
---

# Purpose

Make human judgment traceable without multiplying decision files.

# Canonical Output

`methods/Qx/qx_decisions.jsonl`

One JSON object per line. Records are append-only.

Use `planning/framing_decisions.jsonl` for global/pre-Qx framing decisions.

# Required Fields

```json
{
  "schema_version": 1,
  "decision_id": "q1_method_choice",
  "decision_type": "method_choice",
  "status": "DECIDED",
  "decided_by": "human",
  "captured_in_mode": "learning",
  "choice": "M2",
  "rationale": "Human-authored reason tied to evidence.",
  "evidence_refs": ["methods/Q1/probes/risk_probe_summary.json"],
  "decided_at": "ISO-8601",
  "supersedes": null
}
```

Optional structured fields may include confidence, rejected alternatives, round action, claim scope, assumption labels, or fallback activation.

# Workflow

1. Receive the human's answer, the choice-card ID, and evidence paths.
2. Preserve the user's meaning and wording. Normalize only structure, identifiers, and whitespace.
3. Verify:
   - the choice is one of the presented options or explicitly records a user-supplied alternative;
   - evidence paths exist;
   - rationale is non-empty and contains no placeholder;
   - the record does not falsely label AI-authored prose as human-authored.
4. Append one JSON line.
5. If revising a decision, append a new record with `supersedes`; never overwrite history.
6. Update the compact history in `qx_method_card.md` only when the decision changes method state.
7. Update the manifest gate/status fields when present.

# Decision Types

Typical values:

- `framing`
- `method_choice`
- `code_plan_confirmation`
- `fallback_activation`
- `result_verdict`
- `stability_verdict`
- `assumption_necessity`
- `claim_scope`
- `package_signoff`
- `submission_authorization`

# Scope and Confirmation Evidence

- Capture only an actual explicit human answer, with real source/message reference and the decision's exact scope. Method selection, current full-plan confirmation, Exempt, fallback activation/replacement, sign-off, and submission authorization are distinct decisions; generic permission to continue is not approval of all four method/experiment categories.
- Keep the existing JSONL shape, schema_version: 1, required/optional fields, canonical paths, and append-only rules. Use only a decision_type genuinely supported by the actual caller/ledger contract; the typical list is not proof that arbitrary new types are accepted. If no supported representation truthfully expresses a decision, preserve the actual answer/evidence in Handoff and report the interface gap rather than inventing a type or mislabeling plan approval as method choice.
- Represent task IDs, plan path/revision, exact scope/requiredness, and actual human wording through existing choice, human rationale, and evidence_refs where they truthfully support it. Do not invent mandatory task_ids/authorization_text/authorization_ref fields, fabricated rationale, or historical approval evidence.
- For current full-plan confirmation, identify the actual complete plan content, four-category inventory, applicable conditions, and the exact human answer. At the time of genuine confirmation, preserve a verifiable linkage to the content actually presented and approved, using a contemporaneous digest, immutable revision, preserved snapshot, or other genuinely supported evidence reference. A digest computed after the event or an unchanged version label alone cannot establish historical approval. Do not require a prior approval record before the first genuine confirmation can be captured. If the approved content cannot be reliably identified, report the evidence gap instead of claiming confirmation. First candidate plans may remain pending_confirmation in ordinary Markdown/Handoff; do not create pending ledger records or invent new JSON fields.
- For Exempt, retain the specific original requirement/task IDs, genuine reason/authorization, scope, impact, disclosure and G6 consequences using real existing supported references. Do not infer exemption from failure, missing data/runtime, cost, silence, or similar results. Exempt is not Completed and not automatic G6 approval.
- For a required-method fallback/replacement, distinguish recording the genuine human change decision from authorizing execution of the replacement. A specific human activation/replacement decision may be appended when its actual scope, affected method, genuine trigger evidence, and applicable supersedes relation are established, even if the revised code plan has not yet been drafted or confirmed. This record alone must not release Generator execution. Replacement execution requires the applicable updated complete plan and explicit human confirmation of its current content, together with all other required Gate evidence. Keep original failed attempts and history; do not silently alter requiredness, infer human activation from a trigger, or invent a confirmation.
- decided_at remains ISO-8601 and records formal append time for new records. Do not claim it is actual authorization time unless independently evidenced. Preserve evidenced authorization-time provenance using existing supported representation; otherwise disclose uncertainty through Handoff without inventing timestamps, adding fields, imposing a fixed marker, or rewriting human rationale. Preserve genuine historical timestamps/source provenance on migration rather than manufacturing precision.
- Verify applicable supersession/revocation in real records. A new decision appends a reference to what it supersedes; do not overwrite, delete, silently reactivate revoked choices, or invent a revocation enum/state. A referenced unreadable record makes authority unverifiable, not never-given or valid.
- Use Qx ledgers for actual Qx decisions and the existing framing ledger for genuine global/pre-Qx scope; these scopes are not interchangeable. An irrelevant uncreated ledger is not an error. Do not create an alternative authorization ledger or use a nonexistent ledger as confirmation.
- Preserve existing method-history and manifest update duties only when a genuine recorded decision changes the supported state. Do not move G2.5/plan/G6 or allowed flags beyond what that decision and current evidence authorize; Orchestrator coordinates overall Gate evaluation. Report missing human reason/evidence rather than completing the user's required rationale yourself.

## Complete Code-Plan Confirmation

- `code_plan_confirmation` records only an actual human confirmation of the current complete code plan, not G2.5 method selection, generic permission to continue, fallback activation, package sign-off or submission authorization. Do not use synthetic answers as real authority. A first genuine confirmation can be captured without a prior confirmation record; do not create pending Ledger records.
- Preserve the existing JSONL object and fields: `schema_version`, `decision_id`, `decision_type`, `status`, `decided_by`, `captured_in_mode`, `choice`, `rationale`, `evidence_refs`, `decided_at`, `supersedes`. Use schema_version 1, the defined confirmation type, actual `DECIDED` human ownership, a unique decision_id and the actual captured mode. Keep genuine choice/rationale and evidence; never fill a missing human reason yourself. For this type, retain supersedes as null on the first record or the genuine superseded decision reference on revision. Do not add task_ids, authorization text/ref, plan hash or other Ledger fields.
- Before appending, verify that the human actually saw and approved the exact complete plan, revision/content identity, four-category inventory, explicit requiredness, original task scope, execution conditions and acceptance criteria. Link that answer to contemporaneously preserved full content, an immutable revision, a genuinely recorded digest or other reliable existing evidence. A mutable plan path, unchanged revision label, new post-event SHA-256 or human/DECIDED strings alone cannot establish historical approval. Do not rewrite choice/rationale or backfill historical evidence to make the link appear valid.
- Use existing choice/rationale/evidence_refs to preserve the actual plan scope, IDs and approval provenance; referenced evidence must be real, readable and attributable. Verify the actual current bytes against what was approved, without reformatting or updating the plan to claim approval. Keep method-choice decision IDs distinct from full-plan confirmation and from the packager's separate inclusion-list digest confirmation.
- Substantive plan changes require a new explicit human confirmation and applicable supersedes; retain prior records and failed attempts. A genuine fallback_activation/replacement record may precede the revised plan, but cannot authorize replacement execution before that updated complete content is confirmed. Do not downgrade requiredness or infer activation from a trigger.
- Check actual supersession, revocation, staleness, conflicts, duplicate identities and source scope. Do not choose the last line automatically, revive a revoked record, invent a revocation enum or substitute a global decision for a Qx-specific one. If a relied-on source is unreadable, untraceable, stale or conflicting, report affected `BLOCKING_ERROR` through existing Handoff for orchestrator scheduling; authority is unverifiable, not proven never given or valid.
- Preserve ISO-8601 decided_at as the real formal append time. Establish any actual authorization time only from genuine evidence in existing verified representations; when precise authorization time is unknown, disclose uncertainty through Handoff without inventing a timestamp, new field or forced rationale marker. Unknown exact authorization time alone does not invalidate otherwise genuine, explicit, traceable approval.
- Record genuine current-Qx decisions only in its designated Ledger and read relevant global/pre-Qx evidence only for its actual scope. Do not create an alternative authorization Ledger. Keep all other decision types, existing field meanings, append-only/history duties and limited supported manifest updates unchanged; no plan confirmation automatically authorizes G3/G6 or final assembly. Only this Logger faithfully appends the user's real decision, scheduled through the existing workflow; other Skills and the packaging script must not manufacture or append it.

# Staleness

Mark a decision stale only when its cited evidence materially changed:

- append a `decision_stale` record naming the old decision and changed evidence;
- ask the human to reconfirm through one choice card;
- do not mark decisions stale because unrelated files or formatting changed.

# Legacy Migration

Read legacy:

- `methods/Qx/qx_decision_log.md`
- `methods/Qx/decisions/*_modeler_decision.md`

Migrate only completed human decisions. Preserve original timestamps and source paths when available. Do not convert PENDING placeholders into decisions.

# Rules

- Never choose, rationalize, strengthen, or complete the user's decision.
- Never create a separate pending decision artifact.
- Never copy `ai_suggestion` into the human rationale.
- One evidence-linked sentence is enough; do not impose arbitrary prose length.
- Preserve an honest AI-use provenance distinction.

# Verification

- JSONL is valid one-object-per-line.
- Record is append-only and uniquely identified.
- Human ownership and evidence are accurate.
- Supersession and staleness preserve history.
