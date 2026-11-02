# DEC-003 — Initial Deployment: Single-User, Private-by-Default, Permission-Aware Architecture

**Record ID:** DEC-003
**Date:** 2026-11-02
**Status:** Approved
**Decision Maker:** User

## 1. Decision Required

Establish the initial deployment model, project ownership and privacy model, and authorization/permission architecture for the first implementation.

## 2. Context

§8.11 establishes privacy and access control as fundamental application-wide requirements, not isolated features. The initial implementation priorities in §8.11 require: private-by-default research projects, explicit authorization before sharing, understandable visibility settings, basic permissions for individuals and groups, distinct viewing/contributing/management roles, protection of profile information, secure credential handling, access review and revocation, clear privacy settings, and basic records of permission changes (§8.11 "Initial Implementation Priorities"). However, the Foundation does not require multi-user accounts, authentication, or collaboration in the first release — these are addressed as future possibilities in §8.11 and §9.8.2 ("where applicable"). D4 must reconcile these requirements: establish foundations without building speculative multi-user infrastructure.

## 3. Options

- **Option A: Single-user local deployment with permission-aware data model.** Projects private by default; single local user implicitly owns all projects; data model stores owner and permission-relevant fields; code enforces single-owner access; roles (view/contribute/manage) present in schema even if UI exposes only owner view; no accounts, authentication, groups, or invitations. Multi-user capability preserved via architectural seams (§9.1.2).
- **Option B: Full multi-user with accounts, authentication, groups, invitations.** Implements §8.11.3–8.11.5 in full. Higher complexity; speculative for first release; risks violating §9.8.1 (avoid infrastructure not yet needed).
- **Option C: Single-user with no permission foundation.** Simplest initial implementation but violates §8.11 initial implementation priorities (private-by-default, basic permissions, access review).

## 4. Recommendation

Option A. Satisfies §8.11 initial implementation priorities while deferring actual multi-user functionality (accounts, authentication, groups, invitations, collaboration). Establishes permission seams in the data layer so adding users later is not a rewrite (§9.1.2, §9.8.2).

## 5. Consequences

**Benefits:** §8.11 compliance from the start; single-user simplicity reduces technical risk; architectural seams preserve future multi-user option without restructuring (§9.1.2).
**Drawbacks:** No actual multi-user functionality; permission UI is trivial (single owner only) until accounts are added.
**Risks:** Permission-aware data model must be designed correctly from the start to avoid costly retrofitting (§9.1.2).
**Dependencies:** D2 (photometry first) — analysis records must be associable with projects; D6 (storage) — project file structure must support ownership fields.

## 6. Scope

**Must exist in initial implementation:**
- Single-user local deployment (no accounts, no authentication, no server)
- Projects private by default (§8.11.2)
- Project ownership: single local user implicitly owns all projects
- Permission-aware data model: owner field and permission-relevant fields stored; single-owner access enforced in code
- Roles in schema: view/contribute/manage (present architecturally, exposed as owner-only in UI)
- Understanding visibility settings (trivially satisfied with one user)
- Basic records of permission changes (single-user trivial)

**Architectural foundation (no user-facing multi-user features):**
- Data layer seams for future user/group grant UI
- Access revocation mechanism (single-user trivial)

**Deferred user-facing features:**
- Accounts, authentication
- Group management
- Invitations
- Collaboration
- Public sharing

## 7. Confirmation

User approved single-user local deployment with private-by-default projects and a permission-aware data model; multi-user functionality deferred.

## Approval Record

- **User response:** Approved
- **Conditions or limitations:** Do not implement unnecessary authentication, group-management, or multi-user infrastructure before it is needed; establish foundations without building speculative functionality
- **Date of response:** 2026-11-02
- **Affected requirements:** §8.11, §9.1.2, §9.8.2, §10.4.2
- **Affected roadmap items:** Stage 0 through Stage 2
- **Required follow-up actions:** Record permission model in architecture documentation when created (Stage 3)

## Related Records

- Preceding decisions: DEC-001 (D2), DEC-002 (D3)
- Follow-up decisions: None at this stage
- Related problem records: None
- Related research reviews: None
