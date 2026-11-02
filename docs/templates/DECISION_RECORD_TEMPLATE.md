# Decision Record Template

**Location:** `docs/templates/DECISION_RECORD_TEMPLATE.md`
**Governed by:** §10.9.5, §10.4.5, §11.4.2

## Purpose

Standardized format for recording consequential decisions and approvals. Each decision record must distinguish approved decisions from recommendations and assumptions (§10.4.5).

## Instructions

- Complete all sections. Mark "Not applicable" where a section does not apply.
- Decision status must be one of: Approved, Rejected, Deferred, Modified Approval, Pending (§10.9.5).
- Record the user's response and any conditions attached to approval.
- Link to affected requirements, roadmap items, or architectural decisions.

## Template

```
# DEC-XXX — [Decision Title]

**Record ID:** DEC-XXX
**Date:** YYYY-MM-DD
**Status:** Approved | Rejected | Deferred | Modified Approval | Pending
**Decision Maker:** User | AI Development Partner (within scope)

## 1. Decision Required

What needs approval? State the decision clearly and concisely.

## 2. Context

Why has this decision arisen? What requirement, problem, or opportunity motivates it?

## 3. Options

What reasonable alternatives exist? For each option:
- Option A: [description]
- Option B: [description]
- Option C: [description]

## 4. Recommendation

Which option does the AI recommend, and why?

## 5. Consequences

What are the benefits, drawbacks, risks, and dependencies of the selected approach?

## 6. Scope

Does this change existing requirements, architecture, or development plans? If so, which ones and how?

## 7. Confirmation

What exactly is the user being asked to approve?

## Approval Record

- **User response:** [Approved / Rejected / Deferred / Modified]
- **Conditions or limitations:** [Any conditions attached to approval]
- **Date of response:** YYYY-MM-DD
- **Affected requirements:** [List Foundation sections or project documents affected]
- **Affected roadmap items:** [List roadmap stages or items affected]
- **Required follow-up actions:** [List actions resulting from this decision]

## Related Records

- Preceding decisions: [DEC-XXX references]
- Follow-up decisions: [DEC-XXX references]
- Related problem records: [PROB-XXX references]
- Related research reviews: [REVIEW-XXX references]
```
