# Stage 2.4 — BLS Analysis and Uncertainty

Stage 2.4 is where the application moves from displaying and inspecting astronomical light curves to performing its first scientific analysis.

The objective is to take an imported photometric light curve, search for periodic transit-like signals using the Box Least Squares (BLS) method, estimate the relevant transit parameters, and report uncertainty in those results.

This is a significant stage because it establishes the application's first actual exoplanet transit-detection workflow.

## 1. Overall objective

The Stage 2.4 objective is:

> Implement a reproducible Box Least Squares transit-search workflow that analyzes an imported light-curve dataset, identifies candidate periodic transit signals, estimates relevant transit parameters and their uncertainties, and presents the results without modifying the original scientific measurements.

The initial implementation should remain focused on transit detection from photometric time-series data.

It should not attempt to become a complete transit-fitting or atmospheric-characterization system.

## 2. What BLS analysis needs to accomplish

[Box least squares (BLS) periodogram — cuvarbase 0.2.0 documentation](https://images.openai.com/static-rsc-4/qkxiiSy5yMIQ_E69LhUzTc62NYn8gJb7hoyrDQRC8HU4GHtNulxnQKTsDKMRDom5E9QtaLJReZqGVdM-mlExIOazVogBvX7AgoKdfu4IB87e77FzGzZA43AcQrI_ltTEnXHq7UnYtfqBOBnvWW9bvRIchUrmcOxwuYzg4Zz7Xpk?purpose=inline)

[johnh2o2.github.io](https://johnh2o2.github.io/cuvarbase/bls.html?utm_source=chatgpt.com)

BLS searches for periodic decreases in stellar brightness that resemble planetary transits.

A simplified transit signal has three important characteristics:

- Period: How frequently the transit repeats.
- Duration: How long the transit lasts.
- Depth: How much the observed stellar brightness decreases.

BLS searches across possible periods and transit durations to identify the combination that best matches a repeating, box-shaped signal.

The implementation needs to:

1. Obtain the selected light-curve dataset.
2. Identify the selected flux measurement.
3. Prepare valid observations for analysis without modifying the original dataset.
4. Configure a scientifically appropriate BLS search.
5. Calculate a periodogram.
6. Identify candidate transit signals.
7. Extract the best-fitting transit parameters.
8. Present the results and their limitations.
9. Estimate and report uncertainty.
10. Preserve enough information to reproduce the analysis.

## 3. Recommended task breakdown

I recommend dividing Stage 2.4 into five subtasks.

1. 2.4.1 — BLS Analysis Design and Implementation Planning

   Establish the scientific and technical design before implementation.
2. 2.4.2 — BLS Transit Search Implementation

   Implement the actual period search, periodogram, and candidate parameter extraction.
3. 2.4.3 — Transit Parameter Uncertainty and Detection Assessment

   Establish how uncertainty and detection reliability are calculated and interpreted.
4. 2.4.4 — Application Integration and Analysis Results

   Connect BLS to the existing project, dataset, table, and plot workflow.
5. 2.4.5 — Testing, Scientific Validation, and Completion Verification

   Verify the implementation against controlled data and appropriate astronomical benchmarks.

These are proposed subtasks, not confirmed roadmap changes. The actual roadmap should be checked before adopting them.

## 4. What each subtask involves

### 2.4.1 — BLS Analysis Design and Implementation Planning

PLAN first

This subtask establishes exactly how BLS should work within the existing application.

The coding agent should inspect:

- The completed Stage 2.2 FITS importer and data model.
- The completed Stage 2.3 table and visualization.
- How the application identifies datasets and observations.
- How flux measurements and uncertainties are represented.
- Existing scientific-analysis architecture.
- Installed dependencies and existing test conventions.

The design must establish the following.

A. Input data

Determine how BLS receives:

- Observation times.
- Selected flux measurements.
- Measurement uncertainties, where available.
- Time units and reference system.
- Relevant observation quality information.

The initial default should remain consistent with the existing decision to use PDCSAP_FLUX for the detection workflow, while retaining the ability to analyze SAP_FLUX separately.

B. Data preparation

Establish how the analysis handles:

- Missing observations.
- NaN and infinite values.
- Missing uncertainties.
- Nonzero quality flags.
- Irregular observation spacing.
- Insufficient observations.
- Time-system metadata.

Original measurements must remain unchanged.

Any transformation necessary for analysis must be explicit, documented, and reproducible. It must not silently replace or modify the imported data.

C. Search configuration

Establish how users or the application specify:

- Minimum and maximum search periods.
- Transit-duration search range.
- Period-grid resolution.
- Frequency sampling.
- Search assumptions and constraints.
- Whether measurement uncertainties are used as weights.

The design must avoid arbitrarily narrow search ranges that could exclude genuine signals.

D. Results design

Determine which outputs are required:

- Best candidate period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power or equivalent detection statistic.
- Periodogram.
- Folded light curve.
- Transit model.
- Relevant uncertainty information.

E. Architecture and testing

Determine where BLS belongs in the existing scientific-analysis architecture and how it will be tested without depending on the permanent Kepler dataset.

No implementation should occur during this subtask.

### 2.4.2 — BLS Transit Search Implementation

This is the actual scientific algorithm implementation.

[Exoplanets, and Methods of Detecting Them | Quantum Nucleotides](https://images.openai.com/static-rsc-4/Y_brhQ-xNeu_h2eGmhavd5DASVpc-8p9uA3kkphwJ7FY0cfJK1jrOFuNC85Xz1C17S2C8BgG7paQ1sJF2u7TH5xkfi-D3L6zsONBoDbr9TbWyFDLhjGFzlqKh6fX4ipdkW07ogHcgFImDj871HDI_0sMQvxWA7wY9f1Xae9_2kM?purpose=inline)

[How to detect exoplanets using the transit method](https://images.openai.com/static-rsc-4/c8nx1mxRjx8PuRoz09kR94KNWVxnke96UFhU4zixyn6FR3cG7YAlmcMp1LCwZ-AXeKmbBk9XZ8m6pfw9zeVL9q7y2DknsmLVavAH7g62YJ10Czd-6RpQUbihC3GH4F2-HJaw92xreZBRKVMm3ap5d5GPLK3e0p28lFWFw7N42-8?purpose=inline)

[Transit fitting — exoplanet 0.4.3 documentation](https://images.openai.com/static-rsc-4/v_MPD243lwcryqvAnkZQn24cNMAz2cJ1jEogbXBUmOG5VKRamNSTIt42WSBWYXTzA6XEDI8HQvgj5oFx8K5v8f947BJU6I0uTI1BCAJWVIE6NTU78Z3j2wcvJGcbvRVYRfigif2nKFyk1yjeyKsifWS-ZMdz-G7UU3VNM96iXVQ?purpose=inline)

8

The implementation should cover:

A. BLS calculation

- Perform a periodic transit search.
- Evaluate candidate periods and durations.
- Calculate the BLS periodogram.
- Identify the strongest candidate.
- Extract its transit parameters.

Astropy's `astropy.timeseries.BoxLeastSquares` is a relevant existing library capability to evaluate. It is already part of the project's installed technology stack, so a new dependency may not be necessary.

B. Candidate results

The implementation should produce a structured result containing the candidate's:

| Parameter     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| Period        | Time between repeating transits                              |
| Transit epoch | Reference time associated with a transit                     |
| Duration      | Estimated transit length                                     |
| Depth         | Estimated relative decrease in flux                          |
| BLS power     | Strength of the box-shaped signal under the chosen statistic |

The result should also retain the search configuration and relevant input-data identity.

C. Visualization

The initial analysis should provide:

- A BLS periodogram.
- A phase-folded light curve.
- An overlaid transit model.
- Clearly identified candidate parameters.

The existing scientific plotting architecture should be reused where practical.

D. Scientific boundaries

BLS identifies transit-like periodic signals. It does not independently establish that a detected signal is caused by a planet.

The implementation must not claim planetary confirmation from a BLS peak alone.

### 2.4.3 — Transit Parameter Uncertainty and Detection Assessment

Important scientific design work

This is arguably the most scientifically demanding part of Stage 2.4.

Finding a candidate period is not enough. The application must also communicate how reliable the estimated parameters are.

There are several different concepts that must not be confused.

A. Parameter uncertainty

Estimate uncertainty associated with:

- Orbital period.
- Transit epoch.
- Transit duration.
- Transit depth.

The design must establish which uncertainty methods are appropriate for the available data and which assumptions they require.

Possible approaches to investigate include:

- Statistical uncertainty estimation from the fitted transit model.
- Bootstrap or resampling methods.
- Injection-and-recovery experiments.
- Synthetic-data calibration.

The selected method must be justified and tested. It should not simply report a numerical uncertainty because a library returns one.

B. Detection significance

The application should investigate whether the detected signal is distinguishable from an appropriate noise-only scenario.

This may involve a false alarm probability (FAP) or another calibrated detection statistic.

An important distinction:

- Parameter uncertainty describes uncertainty in estimated values.
- Detection significance assesses how unusual the observed signal is under a specified null hypothesis.
- Neither automatically establishes that a candidate is a real planet.

For example, a low false alarm probability does not mean there is an equally high probability that the candidate is a planet.

C. Aliases and competing signals

The analysis must account for the possibility that the strongest period is not the actual orbital period.

Potential complications include:

- Harmonics.
- Period aliases.
- Sampling-related artifacts.
- Stellar variability.
- Instrumental systematics.
- Multiple competing periodogram peaks.

The application should avoid treating the highest BLS peak as unquestionably correct.

D. Empirical calibration

There is an existing unresolved project question, UQ-009, concerning empirical calibration of BLS uncertainty and tolerances.

This should be addressed here.

The application needs a defensible basis for determining whether its uncertainty estimates and detection behavior are reasonable.

Controlled synthetic datasets and published astronomical benchmarks will be particularly important.

The exact uncertainty and detection-assessment methods should be selected during planning, not assumed in advance.

### 2.4.4 — Application Integration and Analysis Results

This subtask connects the scientific analysis to the existing application.

The user should be able to:

1. Open a project.
2. Select a light-curve dataset.
3. Select SAP_FLUX or PDCSAP_FLUX.
4. Configure a BLS search.
5. Run the analysis.
6. Inspect the periodogram.
7. Inspect the phase-folded light curve.
8. Examine the candidate parameters.
9. Review uncertainty and detection-assessment information.

The application should also handle:

- Missing or unsuitable datasets.
- Invalid search configurations.
- Insufficient observations.
- Analysis failures.
- Switching datasets.
- Repeating an analysis with different parameters.

Results should remain associated with the correct project and dataset.

There is also an important connection to Stage 2.5: analysis operations must eventually be recorded with their parameters and provenance.

Stage 2.4 should establish whatever result structure and information Stage 2.5 will need, but should not silently expand into implementing the complete operation-history system.

### 2.4.5 — Testing, Scientific Validation, and Completion Verification

This subtask verifies that the analysis actually works scientifically.

It should include several categories of tests.

A. Controlled synthetic data

Generate light curves with known properties:

- Known transit periods.
- Known transit epochs.
- Known durations.
- Known transit depths.
- Different noise levels.
- Missing observations.
- Irregular sampling.
- No-transit control datasets.

Because the expected parameters are known, the results can be compared against ground truth.

B. Published astronomical benchmarks

Use appropriate published examples with known detections and non-detections.

The existing Kepler-10b dataset is a natural initial benchmark.

Its published orbital period is approximately:

\\[ P = 0.837491225 \text{ days} \\]

The available local file is a short Q0 Kepler long-cadence observation, so the validation must account for its approximately 9.7-day observation span and actual data quality.

The benchmark should compare recovered results against published values using scientifically justified tolerances, not arbitrary exact-match requirements.

C. Negative controls

Test datasets where no genuine transit signal should be present.

Examples include carefully constructed synthetic noise-only datasets using the relevant sampling and uncertainty characteristics.

A dataset from a quarter without an obvious transit should not automatically be considered a valid negative control.

D. Uncertainty validation

Verify that:

- Reported uncertainties are finite and meaningful.
- Known injected parameters are recovered within expected uncertainty ranges.
- Uncertainty behavior responds sensibly to changes in noise and sampling.
- Detection statistics behave appropriately under the specified null hypothesis.
- Aliases and competing peaks are not misrepresented.

E. Regression and integrity

Verify that:

- Original imported measurements remain unchanged.
- SAP_FLUX and PDCSAP_FLUX remain separate.
- Uncertainties remain correctly associated.
- Missing measurements are handled correctly.
- Quality flags are not silently filtered.
- Analysis results are reproducible from recorded inputs and parameters.
- Existing Stage 2.2 and 2.3 functionality continues to work.

## 5. Scientific decisions that need particular attention

These are the areas I would expect the planning stage to examine most carefully.

| Topic                  | What needs to be decided                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| Flux preparation       | How to handle baseline and relative flux without modifying original measurements           |
| Quality flags          | Whether any quality-based exclusions are supported, and how they are explicitly controlled |
| Uncertainties          | How measurement errors enter the BLS calculation                                           |
| Search ranges          | How period and duration ranges are selected                                                |
| Period resolution      | How finely the algorithm searches possible periods                                         |
| Aliases                | How competing periods and harmonics are identified                                         |
| Parameter uncertainty  | Which methods produce defensible period, epoch, duration, and depth uncertainties          |
| Detection significance | Whether and how FAP or another detection statistic is calibrated                           |
| Validation             | How synthetic and published benchmarks establish reliability                               |

One particularly important distinction: BLS parameter estimation, uncertainty estimation, and detection significance are related but separate scientific problems. They should not be collapsed into one generic confidence score.

## 6. What Stage 2.4 should produce

By the end of the stage, the application should be capable of:

Input

An imported astronomical light curve associated with a project.

Analysis

BLS periodic transit search using an explicitly documented configuration.

Results

- Candidate period, epoch, duration, and depth.
- BLS periodogram.
- Phase-folded light curve.
- Transit model.
- Parameter uncertainties.
- Detection assessment and its assumptions.
- Warnings, limitations, and competing candidate information.

Reproducibility

Results associated with the input dataset and analysis configuration, ready for the operation-recording work in Stage 2.5.

## 7. What Stage 2.4 does not include

To keep the scope manageable, I would exclude:

- Full transit-model fitting and detailed physical parameter estimation.
- Atmospheric retrieval.
- Stellar parameter estimation.
- Planetary mass and radius determination beyond what the available data and approved analysis support.
- Radial-velocity analysis.
- Multi-planet system analysis as a complete capability.
- Automatic detrending or sophisticated stellar variability removal.
- Automatic quality-flag filtering.
- Transit validation sufficient to confirm a planet.
- Archive integration or remote data retrieval.
- Permanent storage architecture redesign.
- Complete analysis-history implementation (Stage 2.5).

These may become later capabilities, but BLS should first be implemented and scientifically validated as a focused transit-search method.

## 8. Completion criteria

Stage 2.4 should only be marked complete when:

- BLS operates on actual imported light-curve data.
- Search configuration is explicit and reproducible.
- Candidate transit parameters are extracted correctly.
- The periodogram and folded light curve are available.
- Parameter uncertainties use a justified method.
- Detection assessment is clearly distinguished from parameter uncertainty.
- Aliases and competing signals are handled appropriately.
- Synthetic data tests demonstrate recovery of known signals.
- Negative controls behave appropriately.
- Published benchmarks are evaluated with justified tolerances.
- Original measurements remain unchanged.
- Existing project, dataset, table, and plot functionality remains intact.
- Documentation accurately describes the implementation and limitations.
- The full test suite passes.

My recommendation: Give 2.4.3 particular attention during planning. A BLS implementation can produce an attractive periodogram and a plausible candidate period without providing scientifically defensible uncertainty. The uncertainty and calibration work is what turns the feature into a useful research tool rather than simply a signal-search demonstration.

Stage 2.5 can then build on this by recording the analysis, its inputs, parameters, results, and provenance.