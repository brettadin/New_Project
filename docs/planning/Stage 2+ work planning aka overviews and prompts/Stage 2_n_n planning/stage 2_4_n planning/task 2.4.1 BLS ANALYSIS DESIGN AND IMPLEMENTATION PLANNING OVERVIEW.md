# Task 2.4.1 — BLS Analysis Design and Implementation Planning

Purpose: Establish how BLS analysis will work within the application before beginning its implementation.

This task is entirely about researching, evaluating, and designing the first BLS analysis capability. No code is implemented yet.

## 1. Review the existing application

Examine the completed Stage 2.2 and 2.3 functionality to understand how BLS will fit into the application.

Specifically, review:

- How imported light-curve measurements are represented.
- How observation times and time metadata are stored.
- How SAP_FLUX and PDCSAP_FLUX are accessed.
- How measurement uncertainties are associated.
- How missing values and quality flags are handled.
- How projects and datasets are selected.
- How the existing plotting components work.

The goal is to design BLS around the actual application rather than create an isolated analysis system.

## 2. Determine how data will be prepared for BLS

BLS requires suitable time-series measurements.

Determine how the application should prepare its input data, including:

- Selecting the flux measurement.
- Handling missing and non-finite observations.
- Handling measurement uncertainties.
- Handling quality flags.
- Accounting for observation spacing and data gaps.
- Interpreting timestamps and time systems.
- Determining whether flux normalization or baseline adjustment is necessary.

Any preparation must be explicit and reproducible. Original imported measurements must remain unchanged.

## 3. Design the BLS search configuration

Determine what parameters are needed to conduct a transit search.

This includes:

- Minimum search period.
- Maximum search period.
- Transit-duration range.
- Period-search resolution.
- Frequency sampling.
- Whether measurement uncertainties should be used as weights.

Establish sensible defaults and determine which parameters should eventually be configurable by the user.

The goal is to establish a search strategy that is scientifically reasonable without unnecessarily restricting the periods that can be detected.

## 4. Determine how candidate transit signals will be identified

Design how the application will use BLS to identify possible periodic transit signals.

Determine how it will:

- Calculate the BLS periodogram.
- Identify significant peaks.
- Select candidate periods.
- Extract transit epoch.
- Estimate transit duration.
- Estimate transit depth.
- Represent competing candidate signals.

Also consider harmonics and aliases, since the strongest periodogram peak is not necessarily the true orbital period.

## 5. Design the expected analysis results

Establish what the user should be able to inspect after running BLS.

The initial results should include:

- Candidate orbital period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Periodogram.
- Phase-folded light curve.
- Transit model.

Determine how these results should be represented internally so that later tasks can use them for uncertainty calculations and application integration.

## 6. Evaluate the existing scientific libraries

Inspect the installed dependencies and determine whether the existing Astropy functionality is suitable.

In particular, evaluate:

`astropy.timeseries.BoxLeastSquares`

Determine whether it provides the capabilities required for the initial BLS implementation.

The intention is to use the existing technology stack where possible rather than introduce unnecessary dependencies.

## 7. Establish scientific limitations

Identify the conditions that could affect the reliability of BLS results.

Consider:

- Short observation baselines.
- Missing observations.
- Irregular sampling.
- Stellar variability.
- Instrumental systematics.
- Measurement noise.
- Multiple possible periods.
- Period aliases and harmonics.
- Insufficient observed transits.

Use the available Kepler-10b dataset as a practical consideration when evaluating the proposed search strategy.

The design should recognize that BLS identifies transit-like signals, not confirmed planets.

## 8. Plan reproducibility and future integration

Determine what information must eventually be retained with an analysis so that its results can be reproduced.

This includes:

- Dataset identity.
- Selected flux measurement.
- Search configuration.
- Data-preparation steps.
- Algorithm information.
- Candidate parameters.
- Relevant warnings and limitations.

The design should also prepare for Stage 2.5, where analysis operations will be recorded.

However, implementing that operation-history system is not part of this task.

## 9. Establish the testing strategy

Determine how the subsequent implementation will be validated.

Plan for:

- Synthetic light curves with known transit periods.
- Known transit depths and durations.
- Different noise levels.
- Missing observations.
- Irregular sampling.
- Noise-only datasets.
- Published astronomical benchmarks.

The testing strategy should establish how accurately the implementation can recover known transit signals and how it behaves when no genuine transit is present.

## 10. Define the implementation plan for subsequent tasks

The final part of 2.4.1 is to turn the design into an actionable implementation plan.

Identify:

- Which modules will need to be created or modified.
- How BLS will interact with the existing data model.
- How results will be represented.
- How visualization will work.
- Which functionality belongs in the next subtasks.
- Any unresolved scientific or architectural decisions requiring approval.

No implementation should occur until the design has been reviewed and approved.

## Expected outcome

At the end of Task 2.4.1, you should have a clear technical and scientific design for the BLS feature.

| Area                 | Expected result                                                      |
| -------------------- | -------------------------------------------------------------------- |
| Input data           | Defined requirements for light-curve measurements                    |
| Data preparation     | Defined handling of missing values, uncertainties, and quality flags |
| Search configuration | Defined period and duration search strategy                          |
| BLS algorithm        | Selected implementation approach                                     |
| Candidate extraction | Defined transit parameters and candidate identification              |
| Results              | Defined periodogram and phase-folded outputs                         |
| Reproducibility      | Defined information to retain with each analysis                     |
| Architecture         | Defined integration points with the existing application             |
| Validation           | Defined synthetic and astronomical benchmark strategy                |
| Implementation       | Approved plan for the remaining Stage 2.4 tasks                      |

In short: Task 2.4.1 determines exactly how BLS should be implemented, what scientific decisions must be made, and how its results will be evaluated. Task 2.4.2 is where the actual BLS algorithm gets built.