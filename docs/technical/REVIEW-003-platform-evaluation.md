# REVIEW-003 — T1 Platform Evaluation

**Record ID:** REVIEW-003
**Date:** 2026-11-02
**Researcher:** AI Development Partner
**Type:** Technical research

## Research Question

Which initial platform strategy best satisfies Foundation §9.1.9 criteria for this astronomy research application?

## Sources Consulted

| Source | Location | Relevance |
|---|---|---|
| Foundation §9.1 | docs/Foundation/9.1_Platform Strategy and Application Deployment.md | Platform strategy requirements and selection criteria |
| Foundation §9.1.9 | docs/Foundation/9.1_Platform Strategy and Application Deployment.md | Ten selection criteria |
| Electron vs Tauri comparison | GitHub martinkoutecky/tine discussion #313 | Desktop framework trade-offs |
| Desktop frameworks 2026 | digitalapplied.com/blog/desktop-apps-web-stack-tauri-electron-deno-2026 | Framework comparison |
| Local-first web architecture | plainvanillaweb.com/blog/articles/2025-07-16-local-first-architecture | Local-first web patterns |
| Pyodide/WASM browser Python | byteiota.com (2026), modelcitizendeveloper.com survey | Browser-based scientific computing |
| Foundation §9.1.2 | docs/Foundation/9.1_Platform Strategy and Application Deployment.md | One platform first, preserve hybrid path |

## Findings

### D1 vs D5 distinction

**D1 (Platform Strategy):** Where does computation run? Where is data stored? How is it accessed? Desktop-first vs browser-first vs local-first web.

**D5 (Technology Stack):** Which specific languages, frameworks, libraries? Python vs JS/Rust. Electron vs Tauri vs Wails.

These were previously conflated. They are separate decisions:
- D1: Platform strategy (desktop-first recommended)
- D5: Technology stack (deferred — no stack selected)

### Platform strategy evaluation against §9.1.9 criteria

| Criterion | Desktop-first | Browser-first | Local-first web |
|---|---|---|---|
| 1. Scientific functionality | Strong — full access to scientific libraries | Limited — browser computation constraints | Moderate — WASM ports immature |
| 2. Scientific computing performance | Strong — native performance | Weak — JS execution limits | Moderate — WASM near-native for compiled code |
| 3. Development complexity | Strong — mature frameworks | Moderate — science gaps need custom work | Moderate — emerging patterns |
| 4. Local system access | Strong — full file system access | Weak — sandboxed | Moderate — File System Access API incomplete browser support |
| 5. Future hybrid compatibility | Strong — logic can be exposed via API | Weak — logic tied to browser | Strong — local core portable |
| 6. Data management | Strong — database, large files, export | Moderate — server or browser storage | Moderate — browser storage less mature |
| 7. Security/privacy | Strong — local data, no transmission | Moderate — data may transit servers | Strong — data on device |
| 8. Deployment/testing | Strong — local install, automated testing | Strong — zero install | Moderate — browser version dependency |
| 9. Cost/infrastructure | Strong — no hosting costs | Moderate — hosting required | Strong — no hosting |
| 10. Expansion/maintainability | Strong — modular, maintained libraries | Moderate — tied to web ecosystem | Moderate — emerging standards |

### Browser-based computing correction

Previous claim that browser-based scientific computing is "weak" was overstated. WebAssembly (WASM) with Pyodide enables CPython with NumPy, SciPy, pandas in the browser. Performance near-native for NumPy (1–16x slower for pure Python). However: JIT-compiled libraries (JAX, PyMC) lack WASM support; browser memory/storage APIs have cross-browser inconsistencies; large astronomical dataset handling in-browser unproven at scale. Browser computing is viable for some workloads but not categorically equivalent to native for all scientific requirements.

### Integration complexity

| Architecture | Integration requirements | Additional complexity |
|---|---|---|
| Desktop-first, Python backend | Python runtime, scientific libraries, GUI framework | Packaging, dependency management, environment distribution |
| Desktop-first, web-tech UI (Electron/Tauri/Wails) | Desktop framework + backend communication layer | IPC between UI and backend, two codebases |
| Browser-first, WASM Python (Pyodide) | WASM runtime, Pyodide distribution, browser APIs | WASM binary size, browser compatibility, limited library support |
| Local-first web | Browser storage APIs, service workers | Cross-browser API inconsistencies, storage quota, offline sync |

### Assumptions

- Desktop-first preserves hybrid path per §9.1.2 (scientific logic in Python can be exposed via API to future web platform)
- No specific framework selected (D5 deferred)

### Limitations

- No implementation testing performed
- Framework integration patterns not empirically evaluated
- Cross-platform compatibility not tested
- Hybrid path proof is architectural reasoning, not demonstrated

## Unresolved Questions

| Question | Why unresolved | Revisit condition |
|---|---|---|
| D1 platform strategy approval | Requires user decision | User reviews and approves D1 decision record |
| D5 technology stack selection | Deferred per user direction | After D1 approval |

## Recommendation

Desktop-first platform strategy as leading recommendation for D1. Satisfies §9.1.9 criteria for scientific computing, local file access, offline use, and hybrid path. D5 technology stack remains separate and deferred. No stack (Python, Electron, Tauri, Wails) selected as part of D1.

## Related Records

- Related decisions: DEC-004 (D1 platform decision record - pending)
- Related problem records: None
- Related research reviews: None
