# Weekly Progress Log

**Research question:** Do consumers (Claude.ai) and businesses (1P API) use
AI differently on the same tasks?

---

## Week 1 — Dataset & Research Question

Selected the Anthropic Economic Index and chose Research Question 3. The plan
is to hold the O*NET task fixed and compare how people work with AI
(automation vs. augmentation) on Claude.ai (consumers) and the 1P API
(businesses).

## Week 2 — Setup & Verification

**What I did**
- Set up the repository (`notebooks/`, `src/`, `data/` [git-ignored],
  `NOTES.md`, `README.md`).
- Downloaded the 2025-09-15 release (data from Aug 4–11, 2025) and recorded
  the source, license and citation in `NOTES.md`.
- Wrote `src/inventory.py` to check file sizes, row counts, columns and
  missing values.
- Looked at raw example rows to understand the collaboration labels.

**Result**
- Reproduced Anthropic's published numbers: **77.37% automation / 12.41%
  augmentation** on the API (report: ~77% / ~12%).

## Week 3 — Two Example Tasks

**What I did**
- Compared Claude.ai and the API on two single O*NET tasks.

**Results**

| Task | API automation | Claude.ai automation |
|---|---|---|
| Counseling | 30.98% | 16.06% |
| Risk & investment analysis | 96.32% | 32.39% |

Both examples show the same pattern as the overall data, so the next step
was a formal test across all tasks.

## Week 4–5 — Hypothesis Test

**Hypotheses**
- **H0:** No difference in automation share between the API and Claude.ai
  for the same task.
- **H1:** The automation share is higher on the API.

**What I did**
- Matched all tasks that appear on both platforms and computed
  `diff = automation% API − automation% Claude.ai` for each task.
- Ran a one-tailed paired t-test and plotted a histogram of the differences.

**Results**

| Metric | Value |
|---|---|
| Matched tasks | 1,193 |
| Mean difference | +31.03 pp |
| Median difference | +31.43 pp |
| t-statistic | 63.26 |
| p-value | < .001 |

H0 is rejected. Almost all tasks are on the positive side of the histogram.

## Week 6–7 — Regression Model

**What I did**
- Rebuilt the data with one row per task and platform (1,193 × 2 = 2,386
  rows).
- Estimated `automation_pct = β0 + β1·api + β2·log_volume + ε` with
  standard errors clustered by task.
- Robustness check: added the unclassified share as a control.

**Results**
- API coefficient: **31.08 pp** (p < .001).
- Stays between 31 and 32 pp in all three models.
- Usage volume does not explain the gap (p = 0.49).

**Challenges**
- The first merge gave 1,604 tasks instead of 1,193, because some tasks had
  only unclassified conversations. Fixed by keeping tasks with classified
  conversations on both platforms.
- The sign of `log_volume` changed after adding the unclassified share
  (omitted variable bias).

## Week 8 — How Do They Differ?

**What I did**
- Added a new section to `src/profile.py` that compares the five
  collaboration types task by task, with one regression per type.
- Studied the exceptions: tasks where Claude.ai automates more than the API.
- Added the results to `PROFILE.md` (Figures 4–7) and saved tables in
  `tables/`.

**Results**

| Collaboration type | API effect |
|---|---|
| Directive | **+31.6 pp** (API higher in 97.6% of tasks) |
| Task iteration | **−18.0 pp** |
| Learning | **−13.3 pp** |
| Validation | −1.3 pp |
| Feedback loop | −0.5 pp |

- In about 95% of tasks, the type that grows the most on the API is
  directive.
- **Interpretation:** businesses hand the task over in one step; consumers
  work on it together with Claude or use it to learn.
- **Exceptions:** 37 of 1,193 tasks (3.1%). They are not just rare tasks
  (p = 0.25), but their API unclassified share is much higher (38.5% vs.
  14.6%), so some of them are probably a measurement effect. Many are
  education, counseling or technical support tasks.

