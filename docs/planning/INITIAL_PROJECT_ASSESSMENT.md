# Initial Project Assessment

> **STATUS: PRELIMINARY — UNAPPROVED WORKING ASSESSMENT**
>
> This document is a record of an initial project assessment produced during a planning session. It is **not** the Master Development Roadmap, it does **not** authorize implementation, and it does **not** establish approved requirements, scope, architecture, or technology choices.
>
> - No decision described in this document has been approved unless it is explicitly marked as approved by the user.
> - Recommendations remain recommendations.
> - Assumptions remain assumptions.
> - Unresolved questions remain unresolved.
> - The governing specification remains `docs/Foundation/`, which is authoritative and read-only.
>
> **Date of assessment:** 2026-11-02
> **Repository state at time of assessment:** `AGENTS.md` and `docs/Foundation/` only; no application implementation, no Master Development Roadmap, no rolling development record.
> **Mode of production:** Plan mode. No files were created or modified during the assessment itself.

---

**Status:** Plan mode. No files were created or modified. The repository is unchanged.

**Coverage note:** I verified the repository state, read the master index and all thirteen section overviews, and read in full the detailed documents governing this phase (Sections 11, 12, 13.1) plus the documents most relevant to identity, scope, capabilities, data, integrity, structure, and platform (Sections 1.1–1.6, 2.2, 2.6, 3.1, 3.4, 4.2, 4.4, 5.2, 5.5, 6.1, 6.4, 9.1–9.8, 10.3, 10.4, 10.9, 10.11). I did **not** read all 131 documents line-by-line. Requirements for areas not yet in scope (detailed discipline documents 2.3–2.5, most of Sections 3.2–3.12, 4.1/4.3/4.5–4.12, 5.1/5.3/5.4/5.6/5.7, 6.2–6.9, all of 7.x and 8.x) are known only at index/overview level and must be read before those areas enter development.

**Label key:** **[F]** verified Foundation requirement (with source) · **[R]** my recommendation · **[A]** assumption · **[?]** unresolved, needs research or your decision.

---

## 0. Verified repository state

| Item | Finding |
|---|---|
| `AGENTS.md` | Present; Foundation declared read-only and governing |
| `docs/Foundation/` | Present; 131 documents (index + 13 sections) |
| Application implementation | **Absent** |
| `docs/MASTER_DEVELOPMENT_ROADMAP.md` | **Absent** — mandatory under 10.3.4 / 10.11.2 |
| Rolling development record | **Absent** — required under 10.11.3 / 11.2.3 |
| Decision, problem, test, research, handoff, improvement records | **Absent** |
| Documentation index `docs/README.md` | **Absent** |
| Version control | Repository is **not** a git repository (10.3.4 requires the roadmap to be in version control; 11.5.5 recommends version control for document history) |

This matches your description. The Foundation describes an application that does not yet exist; no capability may be assumed present.

---

## 1. Application vision and identity

**Verified Foundation requirements**

- The application is an **entirely new, independent project** — not a successor, rebuild, continuation, or rebranding of any existing application. It must have its own codebase, architecture, documentation, and development history. (`docs/Foundation/1.1_Project Identity and Independence.md` §1.1.1–§1.1.2)
- Its **central purpose is astronomy research**: a comprehensive, scientifically credible research platform integrating data discovery, observation, analysis, modelling, visualization, and research management. Education, project management, collaboration, and community are supporting functions that must strengthen — not displace — the scientific core. (`1.2_Overall Vision and Purpose.md` §1.2.1; `1.3_Integrated Scientific Research Environment.md` §1.3)
- It is an **integrated environment**, not a collection of unrelated tools: capabilities must exchange compatible information while preserving metadata, units, provenance, and processing history. (`1.3` §1.3.1–§1.3.3)
- **Intended audience:** beginners, amateur astronomers, students, educators, experienced researchers, and interdisciplinary users. Accessibility must not reduce scientific depth or restrict advanced capability. (`1.4_Intended Audience and Accessibility.md` §1.4.1–§1.4.2)
- **Guiding philosophy:** scientific integrity first; transparency; reproducibility; evidence-based conclusions; usability; long-term adaptability; incremental development. Feature count is explicitly not the goal. (`1.5_Core Philosophy and Guiding Principles.md`; `1.6_Long-Term Ambition and Development Direction.md`)
- **Name, acronym, and branding are not selected.** No provisional name may be treated as official. (`1.1` §1.1.3–§1.1.4)
- Identity must be documented in a **central authoritative location** and used consistently. (`1.1` §1.1.6)

**[R]** The vision is coherent and unusually well specified, but it is also very broad. The main planning risk is not ambiguity about *what* the application should be — it is the gravitational pull of the full vision on the first implementation stage. Section 1.6 explicitly warns against that: the initial implementation is not the permanent limit, and the broader vision is not a mandate to build everything immediately.

---

## 2. Major scientific and functional capability areas

**Verified Foundation requirements — scientific scope**

| Area | Foundation position |
|---|---|
| Initial priority disciplines | Exoplanet science; Planetary science and Solar System research; Stellar astronomy; Observational astronomy (`2.2_Initial Priority Scientific Disciplines.md`) — priorities, not permanent restrictions |
| Cross-disciplinary research | Required where scientifically compatible (`2.9`); examples include stellar characterization supporting exoplanet work, and spectroscopy combined with photometry (`12.2` §12.2.9) |
| Future expansion | Disciplines may be added later through evaluation (`2.7`, `2.10`, `13.2`) |

**Verified Foundation requirements — scientific capability areas (Section 3)**

| Capability | Document | Relevance to a first implementation |
|---|---|---|
| Capability framework; general vs specialized tools; complete workflows | 3.1 | Defines the architecture of capabilities; explicitly requires workflows, not isolated features |
| Observational data examination and preparation | 3.2 | Enabling foundation for every other capability |
| Spectroscopy and spectral analysis | 3.3 | Cross-disciplinary; heavier calibration and reference-data requirements |
| Photometry, transits, time-series | 3.4 | Explicitly cross-disciplinary (stellar variability, exoplanet transits, eclipses, periodic phenomena); strongest candidate for a first vertical slice |
| Astronomical imaging and image analysis | 3.5 | Large subsystem: calibration, WCS, source detection, image measurement |
| Additional measurements (radial velocity, astrometry, polarimetry, occultations) | 3.6 | Later; high data/reference complexity |
| Modelling, simulation, prediction | 3.7 | Later; depends on data and analysis foundations |
| Orbital, dynamical, system analysis | 3.8 | Later; relevant to planetary and exoplanet work |
| Comparative / multi-source / integrated analysis | 3.9 | Depends on multiple capabilities existing |
| Scientific visualization and presentation | 3.10 | Cross-cutting; needed from the first scientific capability |
| Research investigations, outputs, results | 3.11 | The container that makes work coherent; depends on projects and records |
| Extensible capabilities and future methods | 3.12 | Architectural requirement, not an initial feature |

**Verified Foundation requirements — functional/supporting areas**

- **Data (Section 4):** discovery framework (4.1), archives/catalogues/databases (4.2), relevance and ranking (4.3), data types/formats/standards (4.4), retrieval and import (4.5), lineage (4.6), provenance and attribution (4.7), quality and reliability (4.8), local data/caching/offline (4.9), external software and APIs (4.10), licensing/privacy/responsible use (4.11), resource evaluation and expansion (4.12).
- **Integrity (Section 5):** integrity and reliability (5.1); **four automation levels — Manual, Guided, Balanced, Advanced** (5.2); processing safeguards (5.3); interpretation and uncertainty (5.4); reproducibility and traceability (5.5); validation and quality control (5.6). **AI-assisted scientific analysis (5.7) is explicitly recorded as speculative future possibility, not an initial requirement.**
- **Structure/UX (Section 6):** navigation principles (6.1); workspaces (6.2); shared cross-disciplinary tools (6.3); projects as persistent environments distinct from workspaces (6.4); interface/visual identity (6.5); UX/accessibility (6.6); data presentation (6.7); customization (6.8); contextual guidance (6.9).
- **Education (Section 7):** reference library (7.1), learning paths (7.2), interactive learning (7.3), contextual education (7.4), mathematical explanations (7.5), literature (7.6), user-created resources (7.7), community learning (7.8), quality/validation (7.9).
- **Community (Section 8):** participation (8.1), profiles (8.2), sharing/publication (8.3), collaborative projects (8.4), data sharing (8.5), workflow sharing (8.6), discussion (8.7), review/reproducibility (8.8), groups (8.9), attribution (8.10), privacy/permissions (8.11), discovery/networking (8.12), moderation (8.13).
- **Platform (Section 9):** hybrid web+desktop preferred long-term, **one platform first** (9.1); modular architecture without overengineering (9.2); local/remote computation (9.3); storage (9.4); connectivity (9.5); offline/sync (9.6); portability/data ownership (9.7); scalability/sustainability (9.8).

---

## 3. Relationships and dependencies between capabilities

**Verified Foundation requirements that constrain the dependency structure**

- Capabilities must not exist as isolated tools; relationships, provenance, and analytical continuity must be preserved across them (`3.1`, `1.3`).
- Reproducibility is an **ongoing property of the research environment, not a final documentation step** (`5.5`).
- Projects are persistent and exist independently of workspaces (`6.4`).
- The architecture must be modular without unnecessary fragmentation or overengineering (`9.2`).

**Derived dependency model [R]**

```text
Layer E  Research outputs: investigations, results, presentation, reproducibility records
              ▲
Layer D  Discipline workflows: exoplanet · planetary · stellar · observational
              ▲
Layer C  Shared analysis services: statistics/uncertainty · time-series · spectral · imaging · modelling
              ▲
Layer B  Scientific data core: data model · units/time/coordinates · provenance & lineage ·
         import/export · validation · original-data preservation
              ▲
Layer A  Platform & shell: navigation · project lifecycle · settings · local storage · build/test/release

Cross-cutting: scientific integrity & validation · automation levels · education · community · external resources
```

Key dependency conclusions:

1. **Layer B is the load-bearing foundation.** Every scientific capability, every project record, and every reproducibility claim depends on the data model and provenance design. It is also the hardest thing to retrofit.
2. **Layer A must exist before anything is testable**, but it should be deliberately thin.
3. **Layer C capabilities are shared, not discipline-owned.** Photometry/time-series and spectroscopy both serve exoplanet, stellar, and planetary work. Building them once, as shared services, is required by `1.3.5` and `6.3`.
4. **Reproducibility and automation levels are cross-cutting**, not modules. If the operation-record model is not designed into Layer B/C from the start, `5.5` and `5.2` become expensive later.
5. **Education and community sit downstream.** Contextual education (`7.4`) depends on real capabilities existing; community (`8.x`) depends on research identity, permissions, and shareable outputs.
6. **External resources are a dependency, not a foundation.** `9.5` and `9.6` both require the application to remain useful when external services are unavailable, so archive integration must not be on the critical path for the first working application.

**Critical path [R]:** documentation baseline → research → application skeleton → data model + provenance → first scientific capability → reproducibility layer.

---

## 4. Initial research requirements and knowledge gaps

**Verified Foundation requirements**

- Every significant scientific capability must be investigated before implementation: scientific problem, established methods and alternatives, inputs, parameters, assumptions, limitations, uncertainty, validation, and interpretation (`12.2` §12.2.1–§12.2.9).
- Scientific foundations must include physical principles, equations, units, approximations, numerical methods, and statistics — not just a computational recipe (`12.2` §12.2.2).
- Complete workflows must be investigated, not isolated operations (`12.2` §12.2.6).
- Validation must distinguish software execution from correct implementation from scientific validation; where benchmarks are unavailable, the limitation must be documented rather than papered over (`12.2` §12.2.7).
- Research findings must be preserved in research records, with sources, assumptions, limitations, and unresolved questions (`12.2` §12.2.10; `11.4` §11.4.5).

**Scientific research still required before implementation [R], prioritised for the recommended first capability**

| # | Research question | Why it blocks implementation |
|---|---|---|
| S1 | Which photometric/time-series methods are scientifically appropriate, and under what conditions? (aperture vs differential photometry; detrending; correlated noise; Lomb–Scargle vs BLS vs TLS; transit/eclipse model fitting; limb darkening) | `12.6.2` forbids implementing a scientific capability whose methodology is insufficiently understood |
| S2 | What are the uncertainty, bias, and failure modes of each method? | Required by `5.4`, `5.6`, `12.2.8` |
| S3 | What benchmark datasets and published results can validate each method? | Required by `12.2.7`; without these, "scientific validation" cannot be claimed |
| S4 | What metadata, units, time systems, and coordinate conventions are required end-to-end? | Units/time-system errors are a persistent scientific failure mode; `4.4`, `9.7.5` |
| S5 | What are the realistic data volumes, cadences, and file sizes for the target workflows? | Drives storage, performance, and platform decisions (`9.3`, `9.4`, `9.8.3`) |
| S6 | Which reference resources are required (catalogues, ephemerides, line lists, model grids)? | Determines external dependencies and licensing (`12.2.5`, `12.4`) |
| S7 | What does a complete, defensible research workflow look like from discovery to recorded result? | Required by `12.2.6` and `3.1` |

**Knowledge gaps in the current project record**

- No scientific research records exist (`docs/science/` absent).
- No external resource register exists (`docs/resources/` absent).
- No unresolved-questions register exists; `13.1.5` requires these to be visible and linked to the roadmap.
- No validation or benchmark plan exists.

**[?]** Depth of scientific research required before Stage 2 is itself a judgement call. `12.6.2` says preparation should be proportionate to complexity and significance. My reading: S1–S4 and S7 are blocking for the first scientific capability; S5–S6 can be resolved during Stage 1 but must precede storage and integration decisions.

---

## 5. Technical research and feasibility questions

**Verified Foundation requirements**

- Technical feasibility must be investigated before major implementation decisions; technology choices must follow scientific requirements, maintainability, performance, security, and long-term direction (`12.3`).
- Platform: hybrid web+desktop is the preferred **long-term** direction; development starts on **one platform** to establish the core architecture, with the second introduced after evaluation (`9.1` §9.1.1).
- Architecture: modular, clear responsibilities, independently testable scientific functionality, no speculative infrastructure (`9.2`).
- Computation: local, remote, and potentially external resources; decisions driven by actual workload, not anticipated maximum (`9.3`, `9.8.4`).
- Storage: integrity, provenance, privacy, portability, long-term accessibility; no unnecessary duplication (`9.4`).
- Connectivity: reliable, secure, transparent; no single external provider as a point of failure (`9.5`).
- Offline: **a comprehensive offline-first architecture is not an initial requirement** unless research demonstrates it is necessary (`9.6`, "Initial Implementation Priorities").
- Portability: user ownership, standard formats, complete project export/import, no unnecessary vendor lock-in (`9.7`).
- Sustainability: maintainable architecture, dependency lifecycle, backup/recovery, controlled updates, scientific validation, cost awareness (`9.8`).
- External resources must be evaluated against consistent criteria — scientific value, coverage, accessibility, compatibility, data quality, performance, licensing, security, maintenance, cost, strategic value — and classified High/Medium/Low/Deferred/Rejected (`12.4` §12.4.5–§12.4.6; `9.5` §9.5.11).

**Technical research questions [R]**

| # | Question | Blocks |
|---|---|---|
| T1 | Which initial platform best satisfies local data access, offline use, computation, and future hybrid deployment? (desktop-first vs web-first vs local-first web) | Platform decision (D1); architecture (9.1, 9.2) |
| T2 | What runtime/language strategy supports the required scientific computing without duplicating mature libraries? (e.g. Python scientific ecosystem vs JS/TS vs embedded interpreter vs Rust) | Stack decision (D5); affects everything downstream |
| T3 | How should FITS, VOTable, CSV, HDF5 and related formats be parsed, validated, and preserved? Which libraries are credible, maintained, and correctly licensed? | Layer B; `4.4`, `9.7.2` |
| T4 | What data model represents objects, observations, datasets, derived products, operations, and relationships without premature complexity? | Layer B; `1.3.2`, `4.6`, `5.5` |
| T5 | How are operations, parameters, software versions, and inputs recorded so analyses are reproducible and replayable? | `5.5`; must be designed early |
| T6 | What storage architecture supports local-first operation, project portability, and later multi-user use? (embedded DB + files vs server DB) | D6; `9.4`, `9.7.3` |
| T7 | What visualization approach handles large light curves, spectra, and images interactively without compromising accuracy? | `3.10`, `6.7`, `9.8.5` |
| T8 | Which external archives/APIs are feasible, licensed for the intended use, and stable enough to depend on? (e.g. MAST, NASA Exoplanet Archive, SIMBAD, Gaia, ESO, ADS) | Stage 7; `12.4`, `9.5.11` |
| T9 | How should authentication and credentials be handled if/when external accounts are required? | `9.5.4`; affects architecture even if deferred |
| T10 | What testing strategy covers both software correctness and scientific correctness? | `10.6`, `12.6.5`, `11.4.4` |
| T11 | How will builds, updates, and dependency versions be managed and reproduced? | `9.8.6`–`9.8.7` |
| T12 | What is the initial backup/recovery approach for local research data? | `9.8.10` |

**Potential development challenges [R]**

1. **Provenance/reproducibility model** — the highest-risk foundational design problem; retrofitting is costly and undermines `5.5`.
2. **Scientific semantics across formats** — `4.4` explicitly warns that a file extension does not establish meaning; naive import will produce silent scientific errors.
3. **Units, time systems, coordinate frames** — a classic source of wrong results; must be first-class, not string metadata.
4. **Scope pressure** — the vision is broad and each section is internally coherent; the discipline will be in refusing to build Layer D/E before Layer B is sound.
5. **Hybrid platform path** — early choices must not foreclose the second platform (`9.1`, `9.7.4`).
6. **External service volatility** — archives change and deprecate APIs (`9.5.9`); integration must be replaceable.
7. **Licensing and redistribution** — public accessibility is not permission to redistribute (`4.11`, `9.7.1`, `12.4.8`).
8. **Validation without benchmarks** — some methods may lack accessible reference cases; `12.2.7` requires documenting that limitation rather than claiming validation.
9. **Multi-user ambiguity** — community features imply accounts and permissions, but the Foundation does not state whether the first release is single-user. This materially affects the data model and must be decided early (`8.11`, `9.8.2`). **[?]**

---

## 6. Recommended initial development scope

**Verified Foundation requirements governing scope**

- Initial scope must be researched, not chosen for ease; it must be a genuine working foundation, not disconnected demonstrations or placeholders (`12.5.1`).
- Foundational capabilities should be identified and prioritised before specialised ones (`12.5.2`).
- Prefer complete, useful workflows over disconnected features; simpler but scientifically valid implementations are acceptable if they do not misrepresent methods or results (`12.5.3`).
- Priority categories: Foundational / High / Medium / Low / Deferred / Future possibility / Rejected (`12.5.4`).
- Each stage must produce useful, verifiable progress; avoid many partially implemented capabilities (`12.5.5`).
- The initial scope must be documented in the Master Development Roadmap (`12.5.8`).

**Recommendation [R] — "Observational data workbench, photometry-first"**

A single-user, local-first application that lets a user create a research project, import and inspect real observational data, perform a scientifically valid photometric/time-series analysis, visualise it, and preserve a reproducible record of what was done.

**In scope (recommended):**

| Area | Included |
|---|---|
| Platform | One platform only; desktop-first with a web-technology UI so the hybrid path remains open. Local file access, local storage, local computation. |
| Application shell | Navigation, project create/open/save, settings, about/version, error reporting |
| Scientific data core | Data model for objects, observations, datasets, derived products; units/time/coordinate handling; provenance and lineage; original-file preservation; import of FITS, VOTable, CSV; validation and clear failure reporting |
| Inspection & visualization | Dataset browser, table view, interactive light-curve and series plots, export of figures and data |
| First scientific capability | Photometry and time-series: basic reduction/inspection, detrending, periodogram, transit/eclipse detection, simple model fitting, uncertainty reporting |
| Discipline framing | Exoplanet transits and stellar variability — two priority disciplines served by one shared capability |
| Reproducibility | Operation records, parameter capture, analysis-record export, project export/import |
| Integrity | Uncertainty surfaced, limitations stated, no unsupported interpretation; automation limited to Manual/Guided initially |

**Explicitly out of scope for the initial scope (recommended):**

Spectroscopy; imaging pipelines; radial velocity/astrometry/polarimetry; modelling and simulation; orbital/dynamical analysis; comparative multi-source analysis; AI-assisted analysis (5.7 is explicitly speculative); community and collaboration; user-created educational content; remote computation; full offline synchronisation; mobile; multi-user accounts.

**Rationale [R]:**

1. It satisfies `12.5.1`'s "genuine working foundation" test — every layer is exercised end-to-end on real data.
2. Photometry/time-series is explicitly cross-disciplinary (`3.4`), so one capability serves two priority disciplines without duplication.
3. It is computationally tractable (1-D series), has well-established methods, and has accessible public data — reducing scientific and technical risk for a first stage.
4. It forces the hard foundational work (data model, provenance, units, records) to be done properly, because those are exactly what a light-curve analysis needs.
5. It leaves spectroscopy and imaging as natural, well-prepared next expansions rather than half-built parallel efforts.

**Alternatives considered [R]:**

- *Spectroscopy-first* — equally cross-disciplinary and central to the long-term vision, but requires heavier calibration, continuum handling, and reference line data. Higher scientific risk for a first capability.
- *Imaging-first* — foundational for observational astronomy, but is a large subsystem (calibration, WCS, source detection) and would delay a complete workflow.
- *Data-discovery-first (search/retrieve only)* — useful, but `12.5.1` warns against a foundation that is only infrastructure; it would not demonstrate scientific usefulness.

---

## 7. Proposed development stages and dependencies

**Verified Foundation requirements**

- Stages must be manageable, dependency-ordered, and individually verifiable (`12.5.5`, `12.6.4`).
- Before an implementation stage: objective, scope, exclusions, dependencies, acceptance criteria, testing approach, environment, documentation, and approvals (`12.6.1`–`12.6.10`).
- Readiness is an assessment of preparation, not evidence that work occurred (`12.6.11`).
- Transition to implementation requires completed research, defined scope, documented strategy, addressed architectural decisions, approvals, and an updated roadmap (`12.7.6`).
- After the first meaningful stage, the foundation must be formally reviewed and the strategy reassessed (`12.7.8`).

**Proposed stages [R]**

| Stage | Objective | Depends on | Produces |
|---|---|---|---|
| **0. Project foundation** | Establish documentation infrastructure, identity record, roadmap, log, templates; record this assessment and your decisions | — | `docs/README.md`, roadmap, log, templates, decision records |
| **1. Research programme** | Scientific research (S1–S7) and technical research (T1–T12) for the initial scope; external resource evaluation | 0 | Research reviews, resource register, decision records for D5–D7 |
| **2. Application skeleton** | Platform shell, navigation, project lifecycle, settings, build/test/release, error handling | 0, 1 (platform + stack approved) | Running application with projects and no science yet |
| **3. Scientific data core** | Data model, units/time/coordinates, provenance and lineage, local store, FITS/VOTable/CSV import, validation, original preservation | 2 | Importable, traceable datasets |
| **4. Inspection and visualization** | Dataset browser, tables, interactive plots, export | 3 | Usable data examination |
| **5. First scientific capability** | Photometry/time-series methods, uncertainty, validation against benchmarks | 3, 4 | Validated light-curve analysis |
| **6. Reproducibility layer** | Operation records, replay, analysis-record and project export/import | 3, 5 | Reproducible investigations |
| **7. First external integration** | One archive, metadata-first retrieval, caching, licensing/auth handling | 3 | Retrieval of real archive data |
| **8. Contextual education slice** | Method explanations and reference entries attached to the capability | 5 | In-context learning support |
| **9. Review and next-capability decision** | Formal review per `12.7.8`; choose spectroscopy vs imaging vs planetary next | 5–8 | Updated roadmap and next scope proposal |

**Notes [R]:**

- Stage 3 must include provenance, not Stage 6. `5.5` makes reproducibility an ongoing property; Stage 6 adds the user-facing record/replay and export layer.
- Stage 4 and Stage 5 can overlap partially, but Stage 5 must not begin before the data model is stable enough to record its operations.
- Stage 7 is deliberately late: `9.5` and `9.6` require the application to be useful without external services.
- Stage 8 is a thin slice only. Full education (`7.x`) is not initial scope.
- Stage 9 is a gate, not a formality: it is where the next capability is chosen with evidence.

---

## 8. Decisions requiring your approval

**Verified Foundation requirements**

- Approval is required for: fundamental architecture changes; major frameworks/technologies/infrastructure; platform strategy changes; significant changes to scientific methodology; substantial new dependencies or external services; major data storage/persistence changes; removing functionality; financial/security/privacy/licensing implications; changes to scope, purpose, or direction (`10.4` §10.4.2; `10.9` §10.9.2).
- Approval requests should follow the seven-part format: decision, context, options, recommendation, consequences, scope, confirmation (`10.9` §10.9.5).
- Silence or ambiguity is never approval (`10.9` §10.9.2; `13.1` §13.1.4).
- Research completion or planning approval is not implementation authorization (`12.6.9`).

**Decisions I am asking you to make [R]**

| ID | Decision | Why it needs you | My recommendation | Status |
|---|---|---|---|---|
| **D1** | Initial platform direction: desktop-first vs web-first vs local-first web | `9.1`, `12.7.2` require an approved initial platform | Desktop-first, web-technology UI, local data and computation | Pending |
| **D2** | First scientific capability: photometry/time-series vs spectroscopy vs imaging | `12.5.3`; determines all downstream research and architecture | Photometry/time-series, framed as exoplanet transits + stellar variability | Pending |
| **D3** | Initial scope boundary: exclude community, education authoring, AI-assisted analysis, remote compute, full sync | `12.5`, `10.4.2` (scope) | Approve the exclusions in §6 | Pending |
| **D4** | Single-user vs multi-user design target for the first release | Not settled by the Foundation; materially affects data model and auth (`8.11`, `9.8.2`) | Design for single-user now, but keep identity/permissions seams so multi-user is not a rewrite | Pending |
| **D5** | Technology stack and architecture | `10.4.2` major frameworks; `12.7.4` | Defer until Stage 1 research; then present a decision record with alternatives | Deferred to Stage 1 |
| **D6** | Data storage model (embedded DB + files vs server DB) | `10.4.2` major storage decision | Defer to Stage 1; recommend local-first, portable project format | Deferred to Stage 1 |
| **D7** | External resources for the first integration | `12.4.11` — recommending is not authorizing | Defer to Stage 1 evaluation; one archive only in Stage 7 | Deferred to Stage 1 |
| **D8** | Documentation structure and the `docs/requirements/` question | `11.2.3` proposes a structure that does not account for the existing read-only Foundation | Adopt `11.2` structure; treat `docs/Foundation/` as the authoritative requirements location; do not create a duplicate `requirements/` directory initially | Pending |
| **D9** | Application name and acronym | `1.1.3` explicitly requires selection; currently unselected | Use an internal working title only; defer official naming and branding until after scope approval | Pending |
| **D10** | Project licence and distribution model | Not specified in the Foundation; required before external distribution and before redistributing external data (`4.11`, `9.7.1`) | Decide before Stage 7 at the latest; flag now so it is not forgotten | Pending |
| **D11** | Governance for changing Foundation requirements | `AGENTS.md` makes the Foundation read-only; `11.5.2` assumes requirements can be revised | Confirm that requirement changes require your explicit authorization and a recorded decision + Foundation amendment | Pending |

**Foundation conflict / ambiguity to report (not resolve silently)**

1. **`docs/requirements/` vs `docs/Foundation/`.** `11.2.3` establishes canonical locations including a `requirements/` category, but the repository's authoritative requirements already live in `docs/Foundation/`, which `AGENTS.md` declares read-only. The Foundation does not mention its own location in that table. Options: (a) index `docs/Foundation/` as the authoritative requirements category and create no duplicate; (b) create `docs/requirements/` only for derived, approved requirement records that cite the Foundation. **Recommendation: (a), with (b) only if a derived baseline is needed.** This is D8.

2. **Requirement change vs read-only Foundation.** `11.5.2` lists "new or revised application requirements are approved" as an event requiring documentation updates, while `AGENTS.md` forbids modifying the Foundation without explicit authorization. These are reconcilable — the Foundation is the requirements source, and changes to it require your authorization — but the reconciliation is not stated anywhere. This is D11.

3. **Roadmap location vs documentation index.** `10.3.4` requires the roadmap location to be documented in the project's documentation index and development instructions, but neither `docs/README.md` nor an updated `AGENTS.md` exists. Creating them is a Stage 0 action, not a Foundation change.

---

## 9. Required project documentation and records

**Verified Foundation requirements**

- Central `docs/` directory with identifiable categories, a central index, and predictable locations (`11.2` §11.2.1–§11.2.3).
- One authoritative location per major document; no competing copies (`11.2.3`, `11.3`).
- **Master Development Roadmap is mandatory** at `docs/MASTER_DEVELOPMENT_ROADMAP.md` (`10.3.4`, `10.11.2`).
- Rolling development record at `docs/development/DEVELOPMENT_LOG.md` (`10.11.3`, `11.2.3`).
- Decision, problem, test, research, handoff, and improvement records in their canonical subdirectories (`11.2.3`, `11.4`).
- Standardised templates in `docs/templates/` for decision records, problem records, test reports, research reviews, improvement records, and session handoffs (`11.4.9`).
- **Test reports are mandatory** for relevant implementation and testing tasks, with exact results and separate scientific verification (`11.4.4`, `10.11.9`).
- Documentation maintenance is part of development, not an afterthought (`11.5`).
- Session startup must consult the roadmap, log, requirements, decisions, and actual codebase (`11.6.6`, `10.11.6`).

**Minimum records required before development begins [R]**

| Path | Purpose | Source |
|---|---|---|
| `docs/README.md` | Central documentation index; must identify the Foundation as authoritative requirements and the roadmap as authoritative development status | `11.2.6`, `10.3.4` |
| `docs/MASTER_DEVELOPMENT_ROADMAP.md` | Authoritative development overview: stages, priorities, dependencies, status, risks, unresolved questions | `10.3.4`, `10.11.2`, `12.5.8` |
| `docs/development/DEVELOPMENT_LOG.md` | Chronological development record | `10.11.3`, `11.4.7` |
| `docs/development/decisions/` | Decision and approval records (starting with this assessment's approved decisions) | `11.4.2`, `10.9.5` |
| `docs/development/problems/` | Problem and investigation records | `11.4.3` |
| `docs/development/test_reports/` | Mandatory test reports | `11.4.4` |
| `docs/development/research_reviews/` | Scientific and technical research records | `11.4.5` |
| `docs/development/handoffs/` | Session handoff records | `11.4.8` |
| `docs/development/improvements/` | Improvement register | `11.4.6` |
| `docs/templates/` | Six standardised templates | `11.4.9` |
| `docs/science/` | Scientific research findings for the initial capability | `11.2.2`, `12.2.10` |
| `docs/architecture/` | Architecture record (created in Stage 2) | `11.2.2` |
| `docs/technical/` | Technical research and feasibility records (Stage 1) | `11.2.2`, `12.3` |
| `docs/resources/` | External resource register (Stage 1 onward) | `12.4.10`, `11.2.2` |
| Project identity record | Central authoritative location for name, acronym, terminology | `1.1.6` — **location not specified; needs a decision** |
| Unresolved-questions register | Visible, classified, linked to roadmap | `13.1` — **location not specified; recommend roadmap section plus decision records** |

**Also required [R]:** initialise version control, and update `AGENTS.md` to point to `docs/README.md` and the roadmap (permitted — it is not a Foundation document).

---

## 10. Recommended immediate next actions

**Not authorized yet — these are recommendations.**

1. **Approve or amend this assessment**, specifically D1–D4 and D8. These determine everything downstream. Without them, Stage 1 research has no defined target.
2. **Create the documentation baseline (Stage 0)** once you switch out of Plan mode: `docs/README.md`, roadmap, development log, templates, decision records for the approved decisions, and a project identity record (working title acceptable).
3. **Record the approved initial scope and stages in the roadmap**, with explicit status distinctions (proposed / approved / ready / in progress).
4. **Run Stage 1 research** as a bounded programme:
   - S1–S4 and S7 for photometry/time-series;
   - T1–T6 and T10 for platform, stack, data model, storage, and testing;
   - external resource evaluation for the Stage 7 candidate archive.
5. **Return with decision records for D5–D7** in the `10.9.5` approval format, with alternatives, trade-offs, and recommendations.
6. **Begin Stage 2 only after** the readiness conditions in `12.6.10` and the transition conditions in `12.7.6` are satisfied and recorded.

---

## Summary judgement

The Foundation is unusually complete and internally consistent. The project does not lack requirements; it lacks **records, decisions, and a bounded first scope**. The single most consequential planning choice is not the technology stack — it is whether the first stage is a coherent vertical slice (data → analysis → reproducible record) or a broad set of partial capabilities. `12.5.1`, `12.5.3`, and `12.5.5` all point firmly at the former.

The second most consequential choice is the data and provenance model. It is the one thing that is expensive to change later and that every scientific claim depends on. It should be designed deliberately in Stage 3, not discovered in Stage 6.

I have not created the roadmap, log, or any other file, and I have not selected technologies. The next step is your decision on D1–D4 and D8.

---

## Document status and provenance

- **Classification:** Preliminary, unapproved working assessment. Not authoritative.
- **Authority:** None beyond recording the analysis performed. The Foundation (`docs/Foundation/`) remains the governing specification.
- **Implementation authorization:** None. This document does not authorize implementation of any kind.
- **Roadmap status:** This document is **not** the Master Development Roadmap and must not be treated as one. The roadmap remains to be created at `docs/MASTER_DEVELOPMENT_ROADMAP.md`.
- **Approval status:** All decisions D1–D11 remain **pending** or **deferred** as stated in §8. No decision in this document has been approved.
- **Scope of preservation:** This file preserves the assessment produced in the planning session without substantive revision. Content was not re-researched, reinterpreted, shortened, or extended.
