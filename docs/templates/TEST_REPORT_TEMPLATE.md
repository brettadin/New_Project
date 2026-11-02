# Test Report Template

**Location:** `docs/templates/TEST_REPORT_TEMPLATE.md`
**Governed by:** §11.4.4, §10.6, §12.6.5

## Purpose

Standardized format for mandatory test reports for relevant implementation and testing tasks, with exact results and separate scientific verification (§11.4.4, §10.11.9).

## Instructions

- A task must not be declared scientifically validated solely because its software tests pass (§12.6.5).
- Separate software correctness testing from scientific verification.
- Record exact results, not summaries.
- Identify known limitations and unexpected behavior.

## Template

```
# TEST-XXX — [Test Title]

**Record ID:** TEST-XXX
**Date:** YYYY-MM-DD
**Tester:** [Name or role]
**Environment:** [Hardware, OS, software versions]

## Test Objective

What functionality, behavior, or scientific property is being tested?

## Scope

What is included and explicitly excluded from this test?

## Test Procedure

Describe the steps performed, inputs used, and expected outputs.

## Exact Results

Record the actual observed results. Do not summarize; include exact values, outputs, logs, and measurements.

| Test Case | Input | Expected Output | Actual Output | Pass/Fail |
|---|---|---|---|---|
| TC-1 | | | | |
| TC-2 | | | | |

## Software Correctness

- Unit tests: [Pass/Fail/Not run]
- Integration tests: [Pass/Fail/Not run]
- Regression tests: [Pass/Fail/Not run]
- Data integrity checks: [Pass/Fail/Not run]

## Scientific Verification (separate from software execution)

- Scientific verification performed: [Yes/No]
- Reference datasets or methods used: [List]
- Scientific result: [Validated / Not validated / Inconclusive]
- Limitations identified: [List]

## Defects and Unexpected Behavior

| Defect ID | Description | Severity | Status |
|---|---|---|---|
| | | | |

## Conclusion

- Overall result: [Pass / Fail / Partial]
- Known limitations: [List]
- Recommended follow-up: [List]

## Related Records

- Related decision: [DEC-XXX references]
- Related problem: [PROB-XXX references]
- Related research review: [REVIEW-XXX references]
```
