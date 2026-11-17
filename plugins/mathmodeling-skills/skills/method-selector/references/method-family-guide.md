# Method-Family Routing Guide

Use this guide to form a shortlist, not as a menu that must be exhausted.

## Evaluation and ranking

- Credible baselines: equal-weight normalized score or an existing operational rule, when they complete the real task.
- Main families: entropy/TOPSIS, PCA-assisted evaluation, grey/fuzzy evaluation when their assumptions fit.
- Key risks: redundant indicators, unjustified directions or weights, weight dominance, concentrated scores, unstable top-k ranks.

## Prediction

- Credible baselines: seasonal naive, last value, moving average, or simple regression selected to match the time structure.
- Main families: exponential smoothing, ARIMA/SARIMA, regression, tree boosting, small-data grey models.
- Key risks: leakage, invalid split, short series, nonstationarity, over-capacity, poor interval coverage.

## Optimization

- Credible baselines: current policy, a feasible greedy rule, or a relaxed exact formulation.
- Main families: LP/MILP, network flow, dynamic or nonlinear programming, justified metaheuristics.
- Key risks: missing constraints, infeasibility, meaningless objectives, nonimplementable solutions, excessive runtime.

## Classification and clustering

- Credible baselines: rule-based or majority/stratified reference when meaningful.
- Main families: logistic/tree models, SVM, random forest, k-means or other clustering with validation.
- Key risks: label absence, class imbalance, arbitrary cluster count, instability, accuracy-only evaluation.

## Mechanism and simulation

- Credible baselines: simplified algebraic or deterministic scenario model that preserves the core mechanism.
- Main families: differential/difference equations, compartment models, Monte Carlo, discrete-event or agent-based simulation.
- Key risks: unidentified parameters, unit errors, invalid boundary conditions, hidden distribution assumptions, too few replications.

## Graph and routing

- Credible baselines: feasible direct rule or nearest-neighbor heuristic.
- Main families: shortest path, flow, matching, spanning tree, TSP/VRP formulations.
- Key risks: unrealistic edges or weights, omitted operational constraints, mathematically valid but unusable routes.

## Plan roles and validation scope

- This guide supports the existing role-based shortlist; it does not choose methods, approve the full code plan, or create a Gate. All six original families remain applicable only when their data, constraints and intended outputs fit.
- A usable baseline must complete the actual task with comparable outputs; a toy or diagnostic_reference cannot satisfy it. Do not add candidates to reach a quota or use source-line count as evidence quality.
- Connect family suggestions to real original task IDs/source/output/data. Missing coverage is COVERAGE_UNVERIFIABLE, not a reason to discard tasks. Method Selector recommendations inform Analyzer's proposed four-category code plan: Required Main Model, Required Baseline, Required Validation Experiments, and Non-required Exploratory Methods. Distinguish genuinely pre-authorized exploration from unapproved exploration suggestions; inclusion in a candidate list alone does not authorize execution or make an exploratory method required. Generator execution requires explicit human confirmation of the complete current plan content and all other applicable execution-release/Gate evidence. This guide does not grant approval.
- A screening probe is not formal validation. Applicable designs include continuous-gap versus random-gap interpolation backtests; fit versus rolling versus independent prediction tests; optimization feasibility/objective/boundary checks; weight/rank stability; dynamic equilibrium/stability/initial-boundary and parameter evidence; learning leakage/splits/generalization; and justified uncertainty for estimation. Select relevant checks with stated reasons, not a universal experiment template.
- Sensitivity or one perturbation is not automatically uncertainty quantification; training fit or a probe PASS is not an independent test. Required validation needs actual input/script/execution/output/criteria evidence; generated code and intended metrics are not completion.
- A conditional fallback remains dormant until genuine trigger evidence and a specific effective human activation/replacement decision identify the affected method and authorized change scope. The actual human change decision may be recorded before Analyzer drafts or obtains confirmation of the revised full plan; that decision alone does not authorize replacement execution. Generator release for the replacement additionally requires the updated complete code plan, explicit human confirmation of its current content, applicable supersession, and all other required Gate evidence. Preserve original failed attempts and history; never lower requiredness because a model is expensive, slow or failed.
- Preserve genuine failures, Warnings, NOT RUN and limitations using existing contracts; no invented JSON statuses/roles. Non-required exploration failure alone need not block completed required work, but its material effects must be disclosed. Exempt needs real scoped human authority and never means Completed or automatic G6.
