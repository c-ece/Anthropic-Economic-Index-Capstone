# Weekly Progress Log

### Week 1 — Dataset & Research Question
Selected the Anthropic Economic Index dataset and chose **Research Question
3**: *Do consumers and businesses use AI differently on the same tasks?*
The plan is to hold the O*NET task fixed and compare interaction style
(automation vs. augmentation) between Claude.ai (consumer) and the 1P API
(business).

### Week 2 — Setup & Verification (Step 1)
- Set up the repository structure (`notebooks/`, `src/`, `data/` [git-ignored],
  `NOTES.md`, `README.md`).
- Downloaded the Aug 2025 release from the primary source and recorded
  provenance (URL, release date, license, citation) in `NOTES.md`.
- Read the Anthropic Economic Index documentation and recorded the unit of
  observation, labeling method, and headline numbers to use as verification
  targets.
- Built an inventory script (`src/inventory.py`) covering file sizes, row
  counts, columns, and missing-value rates.
- Reproduced Anthropic's published numbers as a sanity check: **77.37%
  automation / 12.41% augmentation** in the 1P API data, matching the
  report's published ~77% / ~12%.
- Reviewed raw example rows to build intuition about the collaboration-type
  labels and task text.
- Produced `PROFILE.md` with the exploratory data summary.

### Week 3 — Manual Task-Level Comparisons
Compared Claude.ai vs. 1P API on two individual O*NET tasks, to see whether
the aggregate gap (automation-heavy API vs. augmentation-heavy Claude.ai)
also holds at the single-task level:

- **Counseling task** ("advise clients on how they could be helped by
  counseling"): API automation 30.98% vs. Claude.ai 16.06%; Claude.ai
  augmentation was much higher (70.26% vs. 23.91%).
- **Risk & investment task** ("analyze and classify risks and investments"):
  an even larger gap — API automation 96.32% vs. Claude.ai 32.39%.

These two examples suggested the aggregate pattern holds at the task level
too, motivating a formal test across *all* matched tasks.

### Week 4-5 — Hypothesis Formulation & First Test (H1)
Formulated the hypotheses for Q3:
- **H0:** No difference in automation share between API and Claude.ai for
  the same task (`mean(diff) = 0`).
- **H1:** Automation share is systematically higher on the API
  (`mean(diff) > 0`), driven by businesses optimizing for cost/efficiency
  vs. individuals favoring learning and control.

Generalized the Week 3 manual comparisons into a script that matches *all*
tasks present in both sources and computes the automation-share difference
for each. Ran a one-tailed paired t-test.

| Metric | Value |
|---|---|
| Matched tasks (n) | **1,193** |
| Mean diff (API − Claude.ai) | **+31.03 pp** |
| Median diff | **+31.43 pp** |
| t-statistic | **63.26** |
| p-value | **< .001** |
| Conclusion | **Reject H0 → H1 supported** |

The gap is large and statistically significant across nearly the full task
set, not just the two examples from Week 3. Next steps: test whether the
gap size depends on occupation wage/complexity (H2) and whether it changes
across later data releases (H3).

To visualize this result, I also plotted a histogram of the diff values
across all 1,193 matched tasks (`figures/automation_gap_histogram.png`).
Almost all tasks fall on the positive side (API higher than Claude.ai), and
the distribution is roughly bell-shaped around the mean, which supports the
assumptions behind the paired t-test.

### Week 6-7 — REGRESSION MODEL
- Moved from a hypothesis test to a regression model, as suggested.
  Restructured the data so that each matched task appears twice (once for
  the 1P API, once for Claude.ai): 1,193 tasks × 2 platforms = 2,386
  observations.
- Estimated a multiple linear regression in Python (statsmodels):
  `automation_pct = β0 + β1·api + β2·log_volume + ε`, where `api` is a
  dummy variable and `log_volume` is the log of the task's conversation
  count. Standard errors are clustered by task.
- Ran robustness checks: adding the unclassified share and adding task
  fixed effects.

### Main findings
- The API coefficient is **31.08 pp** (p < 0.001): on the same task,
  businesses use automation about 31 percentage points more than
  consumers.
- The result is robust: the API coefficient stays between 31 and 32 pp
  and significant at the 1% level in all four models.
- Usage volume does not explain the gap (p = 0.49 in the main model).
- The model with only the API dummy reproduces the earlier paired t-test
  exactly (31.03 pp), so the regression extends the previous result
  rather than replacing it.

### Challenges
- My first data merge included tasks with only unclassified conversations,
  which produced 1,604 tasks instead of 1,193. I fixed this by keeping only
  tasks with classified conversations on both platforms.
- The sign of `log_volume` changed when the unclassified share was added,
  which I interpreted as omitted variable bias.

### Next steps
- Answer the "how" part of the research question: estimate a separate
  model for each collaboration type (directive, feedback loop, learning,
  task iteration, validation) and visualize the API coefficients.
  Preliminary results: directive +32 pp, task iteration −17.6 pp,
  learning −12.9 pp on the API.