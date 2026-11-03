# What needs to be done

The Stage 2 readiness-report corrections task is a small documentation-only cleanup. Most of the original corrections have already been made in the revised report. There are two remaining items to address.

## 1. Correct the cross-computer portability wording

The report currently overstates what Subtask 2.1 has implemented by referring to “cross-computer data reference preservation.”

The tests verify that external data-reference metadata survives saving and reopening a project. They do not verify that file paths work across different computers.

Replace the wording in both the Executive Summary and Section 5 with:

> External data-reference metadata is preserved across project save and reopen operations. Cross-computer path portability has not been implemented or verified.

## 2. Remove redundant wording in Section 4.7

Section 4.7 repeats information already established elsewhere about:

- Storing external data references.
- Checking whether referenced files are available.

Remove the redundant opening sentence that repeats those points. Keep the section focused on what is not implemented yet: the full scientific-data provenance and metadata workflow.

## 3. Verify the finished report

After those edits, the AI should:

- Re-read the complete report.
- Confirm both portability corrections were made.
- Confirm the Section 4.7 redundancy was removed without deleting necessary information.
- Check that the report consistently distinguishes project-metadata persistence from scientific-data import, preservation, and provenance.
- Confirm that the readiness conclusion remains Conditionally ready to begin planning Subtask 2.2.
- Report exactly what it changed.

## Scope boundaries

This task should not involve:

| Area                   | Expected action                  |
| ---------------------- | -------------------------------- |
| Source code            | No changes                       |
| Tests                  | No changes or reruns required    |
| Foundation documents   | Read-only                        |
| Architecture decisions | No new decisions                 |
| Roadmap                | No changes expected              |
| Readiness report       | Minimal wording corrections only |

One practical detail: We have not established that the readiness report is actually stored in the repository. It may exist only in your locally saved `.md` document. The AI should locate the actual report before editing anything rather than assuming a file path.

## Completion criteria

Once those two corrections are applied and verified, this task is complete. We can move directly to Subtask 2.2 — Light-curve import, beginning with a fresh Plan-mode review of the current repository and Foundation requirements.



# Prompt

# Build Task — Stage 2 Readiness Report Corrections

## Mode: BUILD

Implement only the documentation corrections explicitly authorized below.

Do not expand the scope, modify source code, or make unrelated improvements.

---

## 1. Project Context

Repository: `C:\Code\New_Project`

GitHub: https://github.com/brettadin/New_Project

The project is currently completing Stage 2.1 (Project Lifecycle) and preparing to begin Stage 2.2 (Light-Curve Import).

The Stage 2 Readiness Review was previously conducted in Plan mode. Its revised report already incorporates the primary scientific-data preservation and project-ownership wording corrections.

This task addresses the remaining issues identified during review.

## 2. Required Preparation

Before editing:

1. Read the root `AGENTS.md` and follow its instructions.
2. Identify and locate the actual Stage 2 Readiness Review report.
   - Do not assume it is stored in a particular repository path.
   - It may be a locally saved Markdown document outside the repository.
   - If the report cannot be located or accessed, stop and report that. Do not recreate it or edit a different document as a substitute.
3. Read the complete report before making changes.
4. Confirm that the two outstanding issues described below are present.
5. Do not modify Foundation documents. They are read-only.

## 3. Required Corrections

### Correction 1 — Cross-computer data-reference portability wording

The report currently overstates the implementation by referring to "cross-computer data reference preservation."

Subtask 2.1 verifies that external data-reference metadata survives project save and reopen operations. It does not implement or verify cross-computer path portability.

Locate the wording in both:

- Executive Summary
- Section 5

Replace the inaccurate wording in both locations with this exact statement:

"External data-reference metadata is preserved across project save and reopen operations. Cross-computer path portability has not been implemented or verified."

Preserve the surrounding section structure and formatting.

Do not imply that external scientific data files themselves are copied, preserved, or made portable by Subtask 2.1.

### Correction 2 — Section 4.7 redundancy

Section 4.7 redundantly repeats information already covered elsewhere concerning:

- Storage of external data references.
- Dynamic checking of referenced-file availability.

Remove the redundant opening sentence that repeats this information.

Preserve the section's substantive discussion of the scientific-data provenance and metadata workflow that remains unimplemented.

Do not remove information necessary to understand the current implementation limitations.

## 4. Scope Restrictions

This is a documentation-only task.

**Authorized:**
- Edit the identified Stage 2 Readiness Review report.
- Make the two specified corrections.
- Make minimal formatting adjustments if required by the edits.

**Not authorized:**
- Modify Python source code.
- Modify tests or test expectations.
- Modify Foundation documents.
- Modify architecture decisions or decision records.
- Modify the development roadmap or development log.
- Perform additional readiness-review work.
- Rewrite or reorganize the report.
- Introduce new requirements or architectural decisions.
- Begin Subtask 2.2.
- Commit, push, reset, clean, or otherwise alter Git history or repository state beyond the authorized document edit.

If you discover another possible issue, report it separately. Do not fix it as part of this task.

## 5. Verification

After editing:

1. Re-read the complete report.
2. Confirm the corrected portability statement appears in both the Executive Summary and Section 5.
3. Confirm Section 4.7 no longer contains the redundant opening sentence.
4. Confirm the report still accurately distinguishes:
   - Project metadata persistence.
   - External data-reference metadata.
   - Scientific-data import and preservation.
   - Scientific-data provenance and processing history.
5. Confirm the readiness conclusion remains **Conditionally ready** to begin planning Subtask 2.2, unless the actual report contains evidence that makes this conclusion inaccurate. Do not change the conclusion without explaining the evidence.
6. Review the final document for accidental deletions, formatting problems, or unrelated changes.

No source-code tests or full test-suite execution are required because no code is being changed.

## 6. Final Report

When finished, provide:

1. The exact report file edited and its location.
2. The two corrections made.
3. Confirmation that the complete report was re-read.
4. Confirmation that the scope restrictions were respected.
5. Any issues discovered but intentionally left unchanged.
6. Whether the readiness conclusion remains unchanged.

Do not claim completion if the report could not be located, edited, or verified.

**Stop after completing this task. Do not begin Subtask 2.2 or prepare its implementation.**