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

## Week 9–10 — Replication on a Second Release

**Goal:** check whether the Week 4–8 result is specific to one week of data.
Everything so far came from a single release (data for Aug 4–11, 2025). If the
automation gap is real, it should still be there in a different week, with
different models serving the traffic.

**What I did**
- Downloaded the `release_2026_03_24` files (data for Feb 5–12, 2026) and added
  the release and citation to `NOTES.md`.
- Checked that the two releases are comparable: same 10 columns, same 5
  collaboration labels, same `onet_task::collaboration` facet. The February
  files are much larger (477,717 and 195,156 rows vs 100,062 and 33,794) and
  carry 30 extra facets that did not exist in August.
- Added a Week 9–10 section to `src/profile.py`. It reuses the Week 2–8 method without changing
  it: same automation/augmentation buckets, same task matching rule, same
  paired t-test, same regression with standard errors clustered by task. Only
  the input files change.
- The script also re-runs August 2025 through the identical code, so the two
  periods are produced by one pipeline and not by two slightly different ones.
  As a check, it reproduces my Week 4–8 numbers exactly (n = 1,193,
  mean = 31.03 pp, t = 63.26, api = 31.082).

**Results**

| Metric | Aug 2025 | Feb 2026 |
|---|---|---|
| Matched tasks | 1,193 | 1,359 |
| Mean difference | +31.03 pp | +29.97 pp |
| Median difference | +31.43 pp | +30.70 pp |
| t-statistic | 63.26 | 55.52 |
| p-value | < .001 | < .001 |
| Tasks where Claude.ai automates more | 3.1% | 6.7% |

| api coefficient | Aug 2025 | Feb 2026 |
|---|---|---|
| (1) api only | 31.029*** | 29.965*** |
| (2) + log_volume | 31.082*** | 29.893*** |
| (3) + unclassified | 31.847*** | 31.684*** |

| Collaboration type | Aug 2025 | Feb 2026 |
|---|---|---|
| Directive | +31.6 pp | +31.4 pp |
| Feedback loop | −0.5 pp | −1.5 pp |
| Validation | −1.3 pp | −1.0 pp |
| Learning | −13.3 pp | −14.2 pp |
| Task iteration | −18.0 pp | −18.1 pp |

H0 is rejected in both periods. The collaboration-type pattern repeats almost
exactly: the gap is still directive, and what the API gives up is still task
iteration and learning.

**What changed and what did not**

The overall levels moved. Automation fell on both platforms (API 77.4% → 67.6%,
Claude.ai 49.1% → 44.2%) and augmentation rose. But the *difference between the
two platforms on the same task* did not move. That is the part my research
question is about, and it is the part that held.

**Challenges**
- The two releases are not perfectly comparable. `platform_and_product` changed
  from "Claude AI (Free and Pro)" to "Claude AI (Free, Pro, and Max)", so the
  consumer pool is not the same population. The March 2026 report also states
  that the 1P API sample includes Claude Code, which the September 2025
  documentation does not mention. So the business side may have shifted too.
- The unclassified share rose (API 17.9% → 21.6%, Claude.ai 14.9% → 16.4%), and
  the number of tasks where Claude.ai automates more doubled (3.1% → 6.7%).
  These two move together, which supports the Week 8 guess that many of those
  exception tasks are a measurement effect rather than a real reversal.
- Because of this, I did not pool the two periods into one regression. I ran
  them separately and compared coefficients.

**Next step**

The February release adds facets that did not exist in August: `use_case`,
`ai_autonomy`, `task_success`, `multitasking`, `human_only_ability` and the two
time measures. `use_case` in particular can test the assumption the whole
project rests on — that Claude.ai is consumer use and the 1P API is business
use — instead of just assuming it.

## Week 11 — Why Does the Gap Exist? Use Case and Ability

**Goal:** test the two biggest objections to the Week 4–10 result. First, the
whole project assumes Claude.ai is consumer use and the 1P API is business
use, and I had never checked that. Second, someone could argue the gap is not
about *who* the user is but about *what* they are doing — the API handles work
tasks, Claude.ai handles personal ones, and work tasks are simply easier to
automate. The February release has two facets that can answer both.

**What I did**
- Added a Week 11 section to `src/profile.py` using two facets that do not
  exist in the August release: `use_case` (work / personal / coursework) and
  `human_only_ability` (could the user have completed the task without
  Claude?).
- Compared both facets across platforms on the same 1,359 matched tasks, with
  paired t-tests, exactly as in Week 4–5.
- Grouped tasks by their `human_only_ability` share and plotted mean
  automation per group, to see whether the gap closes anywhere.
- Extended the Week 9 regression with the two new variables as controls:
  `automation_pct = β0 + β1·api + β2·log_volume + β3·unclassified_pct + β4·work_pct + β5·human_only_yes_pct + ε`,
  standard errors still clustered by task, 2,718 observations.

**Results — the proxy holds**

| Use case | Claude.ai | 1P API | Difference |
|---|---|---|---|
| Work | 50.5% | 65.2% | **+14.6 pp** |
| Personal | 34.8% | 18.4% | **−16.3 pp** |
| Coursework | 8.0% | 5.7% | −2.3 pp |

All three differences are significant at p < .001. Across all conversations
rather than matched tasks the split is even sharper: the API is 74.2% work,
Claude.ai is 45.2% work and 42.3% personal. So the consumer/business proxy is
supported by the data instead of only assumed.

**Results — ability**

| Could the user have done it alone? | Claude.ai | 1P API | Difference |
|---|---|---|---|
| Yes | 90.8% | 94.3% | +3.5 pp |
| No | 5.8% | 2.3% | −3.5 pp |

Businesses hand over work people could already do themselves. Consumers use
Claude for things they could not do alone about two and a half times as often.
This matches the high `learning` share I found in Week 8, from a completely
separate measure.

Grouping tasks by this share shows the automation gap is about 30 pp in every
group, from tasks under 80% up to tasks at 98–100%. It does not close anywhere.

**Results — the regression**

| | (1) Week 9 | (2) + work | (3) + ability | (4) + both |
|---|---|---|---|---|
| api | 31.684*** | **30.161*** | 31.974*** | **30.410*** |
| work_pct | | 0.099*** | | 0.098*** |
| human_only_yes_pct | | | −0.086* | −0.071 |
| R² | 0.526 | 0.543 | 0.527 | 0.543 |
| N | 2,718 | 2,718 | 2,718 | 2,718 |

*** p < 0.01, * p < 0.1. Clustered SE by task.

Controlling for how work-oriented a task is moves the api coefficient from
31.68 to 30.16. Task purpose explains about 1.5 pp of the gap and leaves 30 pp
unexplained. `human_only_ability` is marginal on its own and not significant
once `work_pct` is in the model. The objection is real but small: the gap is
not a task-mix artifact.

**Challenges**
- The proxy is directional, not clean. Claude.ai is still 50.5% work and the
  API is still 18.4% personal, so the two groups overlap. If consumer and
  business use are mixed inside both platforms, the true consumer–business
  difference is probably *larger* than the 30 pp I measure, not smaller.
- `use_case` and `human_only_ability` are Claude's own classifications of the
  conversation, not answers from the users, so they carry the same measurement
  uncertainty as the collaboration labels.
- I kept these models on February 2026 only. The August release has neither
  facet, so this check cannot be repeated across periods.

**Where the argument stands now**

Week 6–7 showed there is a gap. Week 8 showed it comes from directive use.
Week 9–10 showed it reproduces six months later. Week 11 rules out the
strongest alternative explanation: the two platforms are not simply doing
different kinds of work.