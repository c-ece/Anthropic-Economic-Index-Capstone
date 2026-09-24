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

### Week 4 — Hypothesis Formulation & First Test (H1)
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
