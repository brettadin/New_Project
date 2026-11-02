# Problem Record Template

**Location:** `docs/templates/PROBLEM_RECORD_TEMPLATE.md`
**Governed by:** §11.4.3, §10.7, §10.9.8

## Purpose

Standardized format for recording problems, investigations, and obstacles encountered during development (§11.4.3).

## Instructions

- Classify severity per §10.9.8: Temporary obstacle / Significant problem / Fundamental blocker.
- Record investigation findings and unsuccessful approaches where useful (§13.1.5).
- Update status when the problem is resolved, deferred, or escalated.

## Template

```
# PROB-XXX — [Problem Title]

**Record ID:** PROB-XXX
**Date identified:** YYYY-MM-DD
**Status:** Open | Resolved | Deferred | Escalated
**Severity:** Temporary obstacle | Significant problem | Fundamental blocker

## Problem Description

What is the problem? Describe the issue, its symptoms, and where it occurs.

## Impact

How does this affect functionality, scientific reliability, development progress, or existing work?

## Investigation

What has been investigated? What approaches were tried? What were the results?

## Recommended Resolution

What is the recommended solution? What are the alternatives?

## Blocking Relationships

Does this problem block any development task, decision, or stage? If so, which ones?

## Related Records

- Related decisions: [DEC-XXX references]
- Related research reviews: [REVIEW-XXX references]
- Related test reports: [TEST-XXX references]

## Resolution

- **Resolution:** [How the problem was resolved, or N/A]
- **Date resolved:** YYYY-MM-DD
- **Resolution verified by:** [Name or role]
- **Follow-up actions:** [Any actions needed after resolution]
```
