# Project Instructions

## Governing specification

`docs/Foundation/` is the authoritative specification for this application's intended requirements, goals, constraints, and development philosophy. It is the governing document, not optional background reading.

- The **Foundation** defines what the application is intended to be and what it must satisfy.
- The **codebase** determines what has actually been implemented. Never assume a capability exists because the Foundation describes it, and never assume a requirement is optional because it is not yet implemented.
- Foundation documents are **read-only**. Do not modify, reorganize, rename, replace, or delete them without explicit user authorization. Do not substitute summaries for the originals.

## Before substantive work

Before planning, designing, implementing, or reviewing anything meaningful:

1. Identify which Foundation sections are likely relevant, using the section map below.
2. Open `docs/Foundation/0_index.md` for the overall structure and navigation.
3. Consult the relevant section overview (`x.0`) to orient yourself, then read the relevant detailed documents (`x.y`) directly.
4. Cite the original relative path (and section/heading) when relying on a requirement in plans, reports, or implementation notes.

Retrieve proportionately to the task. Do not bulk-read the entire Foundation, and do not treat the index, a section overview, or a summary as a substitute for the detailed source document.

Consult the Foundation for work involving:

- application vision, scope, requirements, or priorities;
- scientific methods, data, analysis, or validation;
- architecture, platform, storage, dependencies, or external services;
- workspaces, projects, UI/UX, or user-facing behavior;
- AI responsibilities, approvals, testing, documentation, or continuity;
- any change to an established requirement or a consequential decision.

For purely mechanical changes with no behavioral effect, targeted retrieval may not be necessary — but do not assume requirements from memory. The absence of a remembered requirement is not proof that none exists; check the index and relevant section overviews.

## Truth, authority, and uncertainty

- Distinguish clearly between **verified facts**, **assumptions**, **recommendations**, and **approved decisions**.
- Never present a recommendation as though the user has approved it. Approval must come explicitly from the user.
- The user retains final authority over direction, priorities, requirements, and consequential decisions.
- Never claim work is complete, tested, or verified without evidence.
- If Foundation documents conflict with each other, or with the codebase, report the conflict with exact sources. Do not silently pick an interpretation when it materially affects the work, and do not edit the Foundation to resolve it.
- If information is missing or ambiguous, say so. Do not invent requirements, project status, decisions, or approvals. Absence of a record is itself something to report.

## Session continuity

At the beginning of a new session, and before resuming work:

1. Inspect the actual repository state rather than assuming what exists.
2. Check for and read the project's development records, including any Master Development Roadmap and development log, if present.
3. Identify the most recent work, decisions, and outstanding items from those records.
4. Consult the relevant Foundation sections for the current task.

If a required record is missing, report that it is missing rather than reconstructing project status from memory. Persistent project knowledge belongs in project documentation and records, not in conversational memory.

## Foundation map

| Section | Topic |
|---|---|
| 0 | Master index — `docs/Foundation/0_index.md` |
| 1 | Overall Vision, Identity and Purpose |
| 2 | Scientific Scope and Subject Areas |
| 3 | Core Scientific Capabilities and Research Workflows |
| 4 | Data Discovery, Databases and External Resources |
| 5 | Scientific Integrity, Automation and Analysis Control |
| 6 | Application Structure, Workspaces and User Experience |
| 7 | Education, Documentation and Learning Resources |
| 8 | Community, Collaboration and Research Sharing |
| 9 | Platform, Architecture, Portability and Offline Use |
| 10 | AI Development Partner: Responsibilities and Autonomy |
| 11 | Knowledge Management, Project Records and Continuity |
| 12 | Initial Research Phase, Planning and Implementation Boundaries |
| 13 | Outstanding Questions, Flexibility and Future Possibilities |

Section overviews (`x.0`) provide orientation and overall principles. Detailed subsection documents (`x.y`) are authoritative for their specific requirements. Use `0_index.md` for subsection-level detail.

## Project Documentation Index

Project documentation is maintained under `docs/` with a central index at `docs/README.md`. The Master Development Roadmap is maintained at `docs/MASTER_DEVELOPMENT_ROADMAP.md` (§10.3.4) and is the single authoritative source for development planning and progress.

- Documentation index: `docs/README.md`
- Master Development Roadmap: `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- Development log: `docs/development/DEVELOPMENT_LOG.md`
- Decision records: `docs/development/decisions/`
- Templates: `docs/templates/`

At the beginning of each development session, consult `docs/README.md` and `docs/MASTER_DEVELOPMENT_ROADMAP.md` before planning or starting implementation work (§10.3.4).

## Task Continuity

When you are instructed to "continue working," "keep going," or similar:

1. Inspect the Master Development Roadmap (`docs/MASTER_DEVELOPMENT_ROADMAP.md`), Development Log (`docs/development/DEVELOPMENT_LOG.md`), unresolved-questions register (`docs/development/UNRESOLVED_QUESTIONS.md`), and relevant project records to determine the next appropriate unfinished task.

2. Continue working on that task without requiring the user to restate project goals or manually select the next step.

3. Respect the current operating mode:
   - **Plan mode:** Continue investigation, research, analysis, and planning. Do not modify files or implement anything.
   - **Build mode:** Continue implementing approved work, testing, documenting, and verifying results.

4. Respect all approval gates. Do not make decisions reserved for the user's approval, expand approved scope, or proceed past a blocked decision. Stop and explain when the user's input or approval is genuinely required.

5. Work incrementally. Avoid unnecessary repetition, rereading the entire Foundation, duplicating completed work, or creating documentation without a clear purpose.

6. Maintain project continuity:
   - Update the Development Log as meaningful work is completed.
   - Update the Roadmap when task statuses or dependencies change.
   - Maintain the Unresolved Questions register.
   - Create handoff records when useful or when a session ends with unfinished work.
   - Record important findings, decisions, and implementation details so future agents can resume without relying on conversation history.

7. After completing a task, identify the next appropriate task and continue if it is within the approved scope and current mode. Do not stop merely to ask whether the user wants you to continue.

8. Stop when the next task requires the user's approval, a new scope decision, unavailable information, or a change of operating mode.

## Documentation Maintenance During Implementation

Documentation updates are a required part of every Build-mode implementation task, not a separate documentation-only activity.

### Before implementation

1. Read the relevant roadmap and development records before implementation work begins:
   - Master Development Roadmap (`docs/MASTER_DEVELOPMENT_ROADMAP.md`) — confirm current task status and dependencies.
   - Development Log (`docs/development/DEVELOPMENT_LOG.md`) — understand recent work and context.
2. Identify which documentation may need updating based on the authorized task (application behavior, module interfaces, architecture, data structures, persistence behavior, testing, or progress status).
3. Respect existing architectural decisions and approval boundaries.

### During implementation

Update relevant documentation as part of the implementation task whenever the work changes or establishes:

- Application functionality or behavior.
- Module responsibilities or interfaces.
- Architecture or data flow.
- Data structures or persistence behavior.
- Validation, testing, or quality-control behavior.
- Development progress or task completion status.

Update the appropriate existing documents rather than postponing these changes:

- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — reflect verified progress and current status when task statuses, milestones, or dependencies change.
- `docs/development/DEVELOPMENT_LOG.md` — record completed work and important implementation details.
- Architecture and module documentation — when actual architecture or responsibilities change.
- Decision records — when an approved decision is implemented (do not change approved decisions without approval).
- Testing and validation documentation — when testing strategy or verified behavior changes.

Do not update documents merely for the sake of making changes. Avoid duplication and preserve accurate existing material. Documents not affected by the implementation do not need artificial edits.

### Before reporting completion

1. Compare documentation against the actual implementation. Confirm descriptions match the code and verified test results.
2. Identify which documentation files were changed.
3. Explain why relevant documents were intentionally left unchanged.
4. Report any remaining documentation gaps rather than silently deferring them.
5. Distinguish implemented, planned, deferred, and unresolved work in all status reports.

### Scope and authority

- Documentation updates must remain within the authorized implementation scope.
- Do not change approved architectural decisions without approval.
- Do not turn planned functionality into documented implemented functionality.
- Foundation documents remain read-only unless explicitly authorized.
- Do not commit or push documentation changes.
