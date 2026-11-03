I checked the latest pushed commit on `master`.

The 2.1.6 work is present on GitHub. The latest commit is `057ad1d` (“Stage 2.1.6”), and its changes include:

- Project status management for Active, Paused, Completed, and Archived.
- Model and service methods for changing status.
- A Project → Status submenu in the UI.
- Dirty-state handling and status persistence.
- 21 new status-management tests.
- Roadmap and development-log updates marking all six Task 2.1 subtasks complete.

The commit also contains the earlier corrective work for custom project locations and unsaved-project protection. The development log records the full test suite at 135 passing tests. That is the reported result in the commit; I have not run the tests against your local checkout.

So the next major development area is Task 2.2: importing a light-curve dataset. The readiness-report wording corrections are a separate documentation cleanup, not a new scientific feature.

# Future development plan — New_Project

The project is at a useful transition point: the initial project-management foundation is complete, and the next work shifts toward the actual scientific workflow.

I reviewed the current roadmap, development log, unresolved-questions register, BLS research, Kepler-10b dataset profile, and relevant Foundation requirements.

The plan below separates what is already established, what still needs to be built, and what should remain future work. It is a proposed working plan, not approval to implement everything listed.

## 1. Where the project stands

Stage 0 — Documentation and decision baseline

Complete

Stage 1 — Scientific and technical research

Complete

Stage 2 — First useful scientific vertical slice

In progress

Completed within Stage 2

- 2.1.1 — Project metadata model
- 2.1.2 — Project configuration and persistence
- 2.1.3 — Project creation
- 2.1.4 — Project discovery and opening
- 2.1.5 — Project saving and closing
- 2.1.6 — Project lifecycle status management

  All six subtasks complete; 135 tests reported passing.

  Remaining within Stage 2
- 2.2 — Light-curve dataset import
- 2.3 — Data table and light-curve visualization
- 2.4 — BLS transit-period analysis with uncertainty
- 2.5 — Recording analysis operations and parameters

The current roadmap defines these remaining tasks at a high level. The detailed breakdown below is my proposed organization of the work.

# 2. Finish the readiness-review documentation

Before beginning 2.2, finish the small documentation correction we had already planned.

The remaining corrections identified during the review were:

- Qualify the claim about cross-computer data-reference preservation. Saving a path successfully does not establish that the path will work on another computer.
- Remove the redundant statement in §4.7.
- Verify that the other scientific-data preservation corrections remain intact.

This is a documentation-only Build task. It should not involve source-code or test changes.

Once verified, the readiness review is finished. We should not repeat the entire readiness review unless new evidence warrants it.

# 3. Stage 2 — Build the first scientific workflow

This is the immediate development priority.

The intended outcome is a functioning desktop application that can open a research project, import a real astronomical light curve, examine it, perform a transit-period search, and retain a record of the analysis.

## 2.2 — Import a light-curve dataset

Next development task

[Identifying transiting exoplanet signals in a light curve — Lightkurve](https://images.openai.com/static-rsc-4/JuVPmY5eBNrZFU4Ypn0ASe6HIeyV7oloCfVo8-UjUMaXy-5R8ky0jiyZQAQdSs10tz7pCfBYlg5cn1cFGP8fiSZyoqwezkK3v460fRvMczdRao0TR0V1b6QEu1dsWhP3yk42tHlHxTC9MjrjnvZ1HsDs2aDhrfvk1K5nKW5wjoI?purpose=inline)

[lightkurve.github.io](https://lightkurve.github.io/lightkurve/tutorials/3-science-examples/exoplanets-identifying-transiting-planet-signals.html?utm_source=chatgpt.com)

This is the first major scientific-data capability.

The initial implementation should use the Kepler-10b FITS dataset already inspected during Stage 1.

Proposed work:

1\. FITS file selection

- Select a local FITS file.
- Read it using Astropy.
- Identify relevant HDUs, headers, and table columns.

2\. Scientific data interpretation

- Identify the time column.
- Identify available flux measurements.
- Identify uncertainty columns.
- Identify quality flags.
- Read available units, time references, and observational metadata.

3\. Data validation

- Detect missing or invalid values.
- Identify incompatible or missing columns.
- Handle NaN values and non-finite measurements.
- Report warnings rather than silently discarding information.

4\. Data preservation and provenance

- Preserve the original scientific file unchanged.
- Retain source information and relevant FITS metadata.
- Establish how the project references or retains the original file.
- Record the relationship between original measurements and any derived data.

5\. Project integration

- Associate imported datasets with the active project.
- Preserve the imported dataset's information when saving and reopening the project.

Important design consideration: D6, the formal storage architecture, remains deferred. We should not turn this first importer into a premature permanent storage-system design.

The first importer should be scientifically sound and appropriately scoped, without attempting to support every possible astronomical file format immediately.

## 2.3 — Data table and light-curve visualization

[Simultaneous Fitting of a Transit with Stellar Variability — exoplanet](https://images.openai.com/static-rsc-4/5Vb8Fe-K2083k0Amp1cv4oYk6FaJnOfKvwBgFtctNU0GP7gwEcxvirU91peMO1RIPSjhn1cgPZ2_g55Zl_Ka3snCYp0z1zNNJNK6R-K9ijf_OEZKY1O8rVFrOasI-9ot3eQnsWSXl6YiovPPiNTFnRpmwKq55P-1YbvUoulSeIs?purpose=inline)

[gallery.exoplanet.codes](https://gallery.exoplanet.codes/tutorials/lc-gp-transit/?utm_source=chatgpt.com)

Once data can be imported, users need to examine it.

Proposed work:

- Display imported measurements in a table.
- Display the light curve as a scientific plot.
- Label axes using the actual measurement units and time representation.
- Allow users to select and inspect measurements.
- Display uncertainty information when available.
- Make missing and invalid measurements identifiable.
- Provide appropriate zooming and navigation.
- Keep plotted data and displayed data connected to the same underlying dataset.
- Avoid modifying the original measurements through visualization.

For Kepler-10b, an important distinction is the difference between `SAP_FLUX` and `PDCSAP_FLUX`.

The latter is the pipeline-corrected flux and is the preferred starting point for the initial exoplanet detection workflow. However, both should remain identifiable as different measurements.

Normalization, filtering, detrending, and other transformations should not silently overwrite the original data.

## 2.4 — BLS transit-period analysis

[How to detect exoplanets using the transit method](https://images.openai.com/static-rsc-4/c8nx1mxRjx8PuRoz09kR94KNWVxnke96UFhU4zixyn6FR3cG7YAlmcMp1LCwZ-AXeKmbBk9XZ8m6pfw9zeVL9q7y2DknsmLVavAH7g62YJ10Czd-6RpQUbihC3GH4F2-HJaw92xreZBRKVMm3ap5d5GPLK3e0p28lFWFw7N42-8?purpose=inline)

[webwidewit.com](https://webwidewit.com/how-to-detect-exoplanets-using-the-transit-method?utm_source=chatgpt.com)

This is the first actual scientific analysis operation.

The method has already been selected and approved in DEC-005.

Proposed work:

1. Select an appropriate light-curve dataset and flux column.
2. Establish the input requirements and data-quality handling.
3. Configure the BLS search parameters.
4. Run Astropy's `BoxLeastSquares`.
5. Display the resulting periodogram.
6. Identify candidate periods.
7. Examine candidate transit characteristics, including depth, duration, and reference time.
8. Present relevant uncertainty and statistical information.
9. Preserve the analysis parameters and results.

### Scientific validation

The primary benchmark is Kepler-10b's published period:

\\[ P = 0.837491225 \pm 3.03\times10^{-7}\text{ days} \\]

The initial Q0 dataset has approximately 9.7 days of observations. It is suitable for targeted period-recovery testing, but not sufficient to demonstrate general-purpose blind transit discovery.

We should also develop:

- Positive controls using injected synthetic transit signals.
- Negative controls using synthetic noise-only data.
- Tests for aliases and period-grid sensitivity.
- Tests involving missing measurements and uncertainties.

UQ-009 remains important: empirical calibration of BLS uncertainty and acceptance tolerances is still outstanding. We should address this during validation rather than inventing precision estimates.

We must also distinguish measurement uncertainty from uncertainty in the recovered orbital period. They are not interchangeable.

## 2.5 — Record analysis operations and parameters

The application needs to remember what it did, not merely display the most recent result.

Proposed work:

- Record which dataset was analyzed.
- Record the selected measurements and input columns.
- Record the operation performed.
- Record the BLS parameters.
- Record any preprocessing or quality filtering.
- Record relevant software and method information.
- Retain the analysis results.
- Preserve relevant uncertainty and limitation information.
- Associate the operation record with the research project.
- Allow the record to be inspected after reopening the project.

This should establish the foundation for later reproducibility.

It should not become a complete analysis-replay engine yet. That is a later stage.

## Stage 2 completion target

The first useful scientific vertical slice

A user should be able to:

1. Create or open a research project.
2. Import a real Kepler-10b light-curve FITS file.
3. Inspect its scientific data and metadata.
4. View its measurements in a table.
5. Visualize its light curve.
6. Run a BLS transit-period search.
7. Examine the resulting candidate and relevant uncertainties.
8. Save the project.
9. Close and reopen it.
10. Inspect the preserved dataset and analysis record.

This is the most important near-term milestone. We should avoid expanding the scope until this workflow is coherent and scientifically defensible.

# 4. Stage 3 — Reproducibility and research continuity

The current roadmap identifies this as the next major stage after the first scientific vertical slice.

The focus shifts from merely retaining analysis results to making investigations understandable and reproducible.

Proposed work:

- Inspect previously recorded analysis operations.
- Review their inputs, parameters, and outputs.
- Reproduce or replay supported analyses.
- Identify missing dependencies or unavailable source data.
- Create portable analysis packages.
- Export and import research projects.
- Preserve relationships between datasets, operations, and results.
- Verify that imported research packages retain their scientific context.

This is where the application starts becoming a more complete research environment rather than simply an analysis program.

Important distinction: Stage 2 establishes operation recording. Stage 3 develops broader inspection, replay, and portability capabilities.

# 5. Stage 4 — First external scientific integration

The roadmap proposes integrating one external archive.

This should happen after the project has a reliable local import and analysis workflow.

Proposed work:

- Evaluate and select the first archive.
- Research its API and data-access methods.
- Retrieve metadata before downloading large datasets.
- Search for astronomical targets and observations.
- Present available observations and their relevant metadata.
- Retrieve selected datasets.
- Cache retrieved data appropriately.
- Preserve source attribution and provenance.
- Handle licensing, authentication, and credentials correctly.

D7, the first external-resource decision, remains deferred.

D10, the project licence and distribution model, must be approved before the roadmap's external-integration milestone.

I would not begin building archive integrations during 2.2. A dependable local workflow should come first.

# 6. Stage 5 — Contextual education

This stage adds educational support directly to the scientific workflow.

The Foundation envisions education as an integrated part of the application, rather than a separate collection of unrelated tutorials.

Possible capabilities:

- Explanations of scientific methods.
- Definitions of relevant terminology.
- Mathematical explanations and equations.
- Parameter descriptions.
- Interpretation of graphs and results.
- Explanations of scientific limitations.
- References to relevant literature and resources.
- Guided learning activities.

For example, when examining a BLS periodogram, the application could explain what period, duration, depth, and periodogram power represent.

This should be developed around real implemented capabilities, rather than building an extensive educational system before the scientific functionality exists.

# 7. Stage 6 — Review and next scientific capability

After Stages 2–5, the roadmap calls for a formal reassessment under Foundation §12.7.8.

The goal is to evaluate the application's actual development experience and decide what scientific capability should come next.

The roadmap currently identifies three broad candidates:

- Spectroscopy.
- Astronomical imaging.
- Planetary science.

This is a future decision, not something we need to settle now.

The decision should be based on scientific requirements, technical feasibility, available data, existing architecture, and what the completed application can support.

# 8. Smaller outstanding work from Task 2.1

There are a few things from the completed project-lifecycle work that remain deferred.

| Item                                                            | Suggested timing                                          |
| --------------------------------------------------------------- | --------------------------------------------------------- |
| Application window-close / exit handling for unsaved projects   | Revisit when appropriate; not a scientific-import blocker |
| Fix the misconfigured New Project save-failure UI test          | Separate test-maintenance task                            |
| Prevent test error dialogs from flashing during automated tests | Test-maintenance task                                     |
| Status filtering/searching in project discovery                 | Future usability improvement                              |
| Historical audit trail for status changes                       | Later provenance/reproducibility work                     |

I would not interrupt the next scientific task to address all of these. The first two test issues can be handled as a small maintenance task when convenient.

# 9. Long-term capabilities beyond the current roadmap

The Foundation describes a much broader application than the first few stages.

These are legitimate long-term directions, but they should not become immediate development commitments.

[Hot sub-Neptune exoplanet TOI-421 b (NIRISS/NIRSpec transmission spectrum) | ESA/Webb](https://images.openai.com/static-rsc-4/sqFFpPMxYNBFDA0d8XIbwBdeERJAAsDb39a_Zeu1NDDXij5cz-sqvC-3EDpQyF8aPvvDxfZsNTLobna2EiSjTGqG4QCFvFNlxHQ-YqAMURWXF9XmknAMkmCEDBJP-x72JR2xN4TKxwkdcgAMnz1iTbBMg6GTkEjimzPhCIFoNGA?purpose=inline)

Spectroscopy and spectral analysis

Spectral data import, calibration, feature identification, molecular reference comparisons, atmospheric characterization, and spectral modelling.

[Vera Rubin Observatory zooms into deep space photo of the day for June 24, 2025 | Space](https://images.openai.com/static-rsc-4/6Qzbo_zSQHnxw9ZLloJG0YmId9wlCZzl2_V4V_xZdH2caWPJEAmOIS-7clMe1Gk1_gdjaBe8YhmwkvvI2Zr70N89nDtA7mss-BTGWAVPn4XLEofxQ_yymA4reQFGYLB9I0JVy94umbKG59yOJOetwHVxYD5m7s2_f5gkjujz7rE?purpose=inline)

Astronomical imaging

Image inspection, calibration, processing, source identification, measurements, and image-based analysis.

[جريدة الرياض  | علماء الفلك يكتشفون نظاماً من ستة كواكب خارج المجموعة الشمسية](https://images.openai.com/static-rsc-4/WXnHkwdrzW8bMxQ1fr6V8KoTakAjvSZ3YtRVcLxVHfDP_ANjALYTgKdVniUdac-AqrCmxqqKU7n_mnAWCeanjn2U6rx1KNzA0ZSwop6tBiOYx6njC8BlhegOfhEqgVsd-fzzMjJDL2--zmUDlAS28i9_TNITuCyMAEgzFU4BbPU?purpose=inline)

Planetary and orbital modelling

Orbital dynamics, planetary modelling, atmospheric models, simulations, and predictions.

[ESA Science & Technology - ESASky's intuitive interface](https://images.openai.com/static-rsc-4/1wNIh85oDc-APxEBywN7Pla15BRt_FDiWU3AU-w30ilf8zt3DE8qC5PBSem7G6ZNXx03R5dvZzhNKkZX_YQBgcM4h-BOo9-OXrAG73FK_f0WUsZWKrhNMNUmUVCr601gaa4PFBeszlXmkopRM-XdzbJ9NUPDjUt0H2Ycvhrg1nU?purpose=inline)

Integrated research environment

Multi-source comparisons, research workspaces, project organization, scientific references, and interconnected investigations.

[Undergraduate Astronomy Researchers Search for Exoplanets | College of Arts and Sciences](https://images.openai.com/static-rsc-4/96R3sF9YvZPDNmwRQrsu0wEMLL5z98zs_ZuPySVKenzi6eu9VimpK6YcAWaA2O8HmVnAGdVpcyeSnXcyuRbnGqxmJiR7nYYa8HCYhPYj1w9l0FXgm8FejslvJPYQMg1yti1kpheNuIo3TusUBZ-pEOZFAL420g54NTjvAjR-TPM?purpose=inline)

Collaboration and community

Shared research, permissions, scientific discussion, resource sharing, and publication-oriented workflows.

The Foundation also establishes long-term expectations for offline functionality, portability, data ownership, scientific integrity, and adaptability. These should influence architectural choices now, without requiring their full implementation in the first vertical slice.

# 10. Recommended working sequence

This is the order I recommend we use when development access returns.

| Order | Work                                        | Mode sequence                                          |
| ----- | ------------------------------------------- | ------------------------------------------------------ |
| 1     | Finish readiness-report wording corrections | Build → review                                         |
| 2     | Subtask 2.2 — Import one light curve        | Plan → review → Build → verify                         |
| 3     | Subtask 2.3 — Table and visualization       | Plan → review → Build → verify                         |
| 4     | Subtask 2.4 — BLS analysis                  | Research/Plan → review → Build → scientific validation |
| 5     | Subtask 2.5 — Operation records             | Plan → review → Build → verify                         |
| 6     | Stage 2 formal review                       | Plan/review                                            |
| 7     | Stage 3 reproducibility                     | Plan → review → Build                                  |
| 8     | Stage 4 external integration                | Research → decision/approval → Plan → Build            |
| 9     | Stage 5 contextual education                | Plan → review → Build                                  |
| 10    | Stage 6 reassessment                        | Research/review                                        |

Each subtask should remain independently scoped. We should revise the saved plans as we approach each task, based on the actual repository state, implementation experience, and any new scientific findings.

## 11. How I suggest we manage the planning documents

Your idea of saving the major planning prompts outside the repository is sensible.

I suggest maintaining two separate kinds of documents:

A. Long-term development overview

This is essentially the plan above. It gives us continuity and makes the intended order of work clear.

It should not duplicate the authoritative roadmap in the repository or become a second source of truth for task status.

B. Individual Plan-mode prompts

Create one document for each upcoming major task:

- Stage 2 readiness-report corrections.
- Subtask 2.2 — Light-curve import.
- Subtask 2.3 — Data table and visualization.
- Subtask 2.4 — BLS analysis and uncertainty.
- Subtask 2.5 — Analysis operation records.
- Stage 3 — Reproducibility.

Each prompt will instruct whichever coding AI you use to inspect the current repository, Foundation requirements, existing decisions, and relevant research before proposing an implementation.

We will revise each prompt immediately before use, rather than treating a plan written today as permanently accurate.

My recommendation: Start by preparing the individual Plan-mode document for Subtask 2.2, after we finish the readiness-report correction. That is the next meaningful scientific capability, and it will establish the data-handling foundation needed by everything that follows.