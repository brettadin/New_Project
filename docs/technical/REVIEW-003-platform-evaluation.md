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

**D5 (Technology Stack):** Which specific languages, frameworks, libraries? Python vs JS/Rust. PySide6 vs PyQt6 vs other UI frameworks.

These are separate decisions:
- D1: Platform strategy (desktop-first — approved)
- D5: Technology stack (Python approved as primary language; UI framework selection delegated to OpenCode)

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

### Integration complexity

| Architecture | Integration requirements | Additional complexity |
|---|---|---|
| Desktop-first, Python backend | Python runtime, scientific libraries, GUI framework | Packaging, dependency management, environment distribution |
| Desktop-first, Python + Qt UI | Python backend + Qt bindings (PySide6 or PyQt6) | Packaging Qt dependencies; Qt licensing considerations |
| Browser-first, WASM Python (Pyodide) | WASM runtime, Pyodide distribution, browser APIs | WASM binary size, browser compatibility, limited library support |
| Local-first web | Browser storage APIs, service workers | Cross-browser API inconsistencies, storage quota, offline sync |

### Python UI framework comparison (PySide6 vs PyQt6)

| Criterion | PySide6 | PyQt6 |
|---|---|---|
| **Licensing** | LGPL/GPL dual licensing | GPLv3 or commercial |
| **Distribution** | LGPL permits linking without requiring application to be LGPL | GPL requires derivative works to be GPL; commercial license available |
| **Backend** | Qt Company-backed | Riverbank Computing-backed |
| **Python compatibility** | Python 3.8+ | Python 3.8+ |
| **Scientific library integration** | Native; compatible with NumPy, SciPy, Astropy, Matplotlib | Native; compatible with NumPy, SciPy, Astropy, Matplotlib |
| **Matplotlib integration** | QtAgg backend | QtAgg backend |
| **Documentation** | Official Qt docs + PySide6 docs | Official Qt docs + PyQt6 docs |
| **Packaging** | PyInstaller, cx_Freeze, Nuitka | PyInstaller, cx_Freeze, Nuitka |

### Licensing considerations

PySide6 is distributed under both LGPL and GPL licenses, giving flexibility for distribution. PyQt6 is distributed under GPLv3 (which requires derivative works to be GPL) or a commercial license. Licensing considerations are relevant to possible future distribution of the application.

### Matplotlib backend note

When discussing Qt integration with Matplotlib, use the QtAgg backend (not Qt5Agg) for Qt6-based applications.

### Assumptions

- Desktop-first preserves hybrid path per §9.1.2 (scientific logic in Python can be exposed via API to future web platform)
- Python is the primary language; UI framework selection delegated to OpenCode

### Limitations

- No implementation testing performed
- Framework integration patterns not empirically evaluated
- Cross-platform compatibility not tested
- Hybrid path proof is architectural reasoning, not demonstrated

## Unresolved Questions

| Question | Why unresolved | Revisit condition |
|---|---|---|
| D5 UI framework selection | Delegated to OpenCode | OpenCode selection during Stage 2 implementation |

## Recommendation

Desktop-first platform strategy as the foundation for D1. D5 technology stack: Python approved as primary language; UI framework selection delegated to OpenCode with PySide6 as a recommended candidate (not mandatory).

## Related Records

- Related decisions: DEC-004 (D1 platform decision record - pending)
- Related problem records: None
- Related research reviews: None
