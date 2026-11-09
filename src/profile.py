import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf

api = pd.read_csv("data/aei_raw_1p_api_2025-08-04_to_2025-08-11.csv")

collab = api[
    (api["facet"] == "collaboration") &
    (api["variable"] == "collaboration_pct")
]

print(collab[["cluster_name", "value"]])
automation = collab[
    collab["cluster_name"].isin(["directive", "feedback loop"])
]["value"].sum()

augmentation = collab[
    collab["cluster_name"].isin(["learning", "task iteration", "validation"])
]["value"].sum()

print("Automation:", round(automation, 2), "%")
print("Augmentation:", round(augmentation, 2), "%")
labels = ["Automation", "Augmentation"]
values = [automation, augmentation]

plt.figure(figsize=(7, 5))
bars = plt.bar(labels, values, width=0.5)

plt.ylabel("Percentage of API Use (%)")
plt.title("Automation vs Augmentation in 1P API Usage")
plt.ylim(0, 90)

for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center"
    )

plt.savefig("figures/api_automation_augmentation.png", bbox_inches="tight")
plt.close()
claude = pd.read_csv("data/aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv")

print("\nClaude.ai geography values:")
print(claude["geography"].unique())

print("\nClaude.ai geo_id examples:")
print(claude["geo_id"].unique()[:20])
claude_global = claude[
    (claude["geography"] == "global") &
    (claude["facet"] == "collaboration") &
    (claude["variable"] == "collaboration_pct")
]

print("\nClaude.ai Global Collaboration:")
print(claude_global[["cluster_name", "value"]])
claude_automation = claude_global[
    claude_global["cluster_name"].isin(["directive", "feedback loop"])
]["value"].sum()

claude_augmentation = claude_global[
    claude_global["cluster_name"].isin(["learning", "task iteration", "validation"])
]["value"].sum()

print("\nClaude.ai Automation:", round(claude_automation, 2), "%")
print("Claude.ai Augmentation:", round(claude_augmentation, 2), "%")
import numpy as np

categories = ["Automation", "Augmentation"]

claude_values = [claude_automation, claude_augmentation]
api_values = [automation, augmentation]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(8, 5))

bars1 = plt.bar(x - width/2, claude_values, width, label="Claude.ai")
bars2 = plt.bar(x + width/2, api_values, width, label="1P API")

plt.ylabel("Percentage of Use (%)")
plt.title("Claude.ai vs 1P API Usage")
plt.xticks(x, categories)
plt.ylim(0, 90)
plt.legend()

for bars in [bars1, bars2]:
    for bar in bars:
        value = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            value + 1.5,
            f"{value:.1f}%",
            ha="center"
        )

plt.savefig("figures/claude_vs_api.png", bbox_inches="tight")
plt.close()
collaboration_types = [
    "directive",
    "feedback loop",
    "learning",
    "task iteration",
    "validation"
]

api_detail = collab[
    collab["cluster_name"].isin(collaboration_types)
][["cluster_name", "value"]]

claude_detail = claude_global[
    claude_global["cluster_name"].isin(collaboration_types)
][["cluster_name", "value"]]

print("\n1P API Collaboration Types:")
print(api_detail)

print("\nClaude.ai Collaboration Types:")
print(claude_detail)
api_values_detail = [
    api_detail.loc[api_detail["cluster_name"] == name, "value"].iloc[0]
    for name in collaboration_types
]

claude_values_detail = [
    claude_detail.loc[claude_detail["cluster_name"] == name, "value"].iloc[0]
    for name in collaboration_types
]

x = np.arange(len(collaboration_types))
width = 0.35

plt.figure(figsize=(9, 5))

plt.bar(x - width/2, claude_values_detail, width, label="Claude.ai")
plt.bar(x + width/2, api_values_detail, width, label="1P API")

plt.ylabel("Percentage of Use (%)")
plt.title("Collaboration Types: Claude.ai vs 1P API")
plt.xticks(
    x,
    ["Directive", "Feedback Loop", "Learning", "Task Iteration", "Validation"],
    rotation=20
)

plt.legend()
plt.tight_layout()

plt.savefig("figures/collaboration_types.png", bbox_inches="tight")
plt.close()

# SAME-TASK ANALYSIS

task1 = "advise clients on how they could be helped by counseling"

api_task1 = api[
    (api["facet"] == "onet_task::collaboration") &
    (api["variable"] == "onet_task_collaboration_pct") &
    (api["cluster_name"].str.startswith(task1, na=False))
]
pd.set_option("display.max_colwidth", None)
print("\nAPI - Counseling Task:")
for _, row in api_task1.iterrows():
    print(row["cluster_name"], "=", round(row["value"], 2), "%")

    # Counseling task - Claude.ai
claude_task1 = claude[
    (claude["geography"] == "global") &
    (claude["facet"] == "onet_task::collaboration") &
    (claude["variable"] == "onet_task_collaboration_pct") &
    (claude["cluster_name"].str.startswith(task1, na=False))
]
print("\nClaude.ai - Counseling Task:")
for _, row in claude_task1.iterrows():
    print(row["cluster_name"], "=", round(row["value"], 2), "%")


    # Automation and Augmentation for Counseling Task
api_task1_automation = api_task1[
    api_task1["cluster_name"].str.endswith(
        ("::directive", "::feedback loop"), na=False
    )
]["value"].sum()

api_task1_augmentation = api_task1[
    api_task1["cluster_name"].str.endswith(
        ("::learning", "::task iteration", "::validation"), na=False
    )
]["value"].sum()

claude_task1_automation = claude_task1[
    claude_task1["cluster_name"].str.endswith(
        ("::directive", "::feedback loop"), na=False
    )
]["value"].sum()

claude_task1_augmentation = claude_task1[
    claude_task1["cluster_name"].str.endswith(
        ("::learning", "::task iteration", "::validation"), na=False
    )
]["value"].sum()

print("\nCounseling Task Comparison:")
print("API Automation:", round(api_task1_automation, 2), "%")
print("API Augmentation:", round(api_task1_augmentation, 2), "%")
print("Claude.ai Automation:", round(claude_task1_automation, 2), "%")
print("Claude.ai Augmentation:", round(claude_task1_augmentation, 2), "%")
plt.savefig(
    "figures/counseling_task_comparison.png",
    bbox_inches="tight"
)
# Counseling Task Comparison Graph

categories = ["Automation", "Augmentation"]

api_task1_values = [
    api_task1_automation,
    api_task1_augmentation
]

claude_task1_values = [
    claude_task1_automation,
    claude_task1_augmentation
]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(8, 5))

bars1 = plt.bar(
    x - width/2,
    claude_task1_values,
    width,
    label="Claude.ai"
)

bars2 = plt.bar(
    x + width/2,
    api_task1_values,
    width,
    label="1P API"
)

plt.ylabel("Percentage (%)")
plt.title("Counseling Task: Claude.ai vs 1P API")
plt.xticks(x, categories)
plt.ylim(0, 80)
plt.legend()

for bars in [bars1, bars2]:
    for bar in bars:
        value = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            value + 1,
            f"{value:.1f}%",
            ha="center"
        )

plt.tight_layout()

plt.savefig(
    "figures/counseling_task_comparison.png",
    bbox_inches="tight"
)

plt.close()

# SECOND SAME-TASK ANALYSIS
# Risk and Investment Task

task2 = "analyze and classify risks and investments to determine their potential impacts on companies."

# API
api_task2 = api[
    (api["facet"] == "onet_task::collaboration") &
    (api["variable"] == "onet_task_collaboration_pct") &
    (api["cluster_name"].str.startswith(task2, na=False))
]

print("\nAPI - Risk and Investment Task:")

for _, row in api_task2.iterrows():
    print(row["cluster_name"], "=", round(row["value"], 2), "%")


# Claude.ai
claude_task2 = claude[
    (claude["geography"] == "global") &
    (claude["facet"] == "onet_task::collaboration") &
    (claude["variable"] == "onet_task_collaboration_pct") &
    (claude["cluster_name"].str.startswith(task2, na=False))
]

print("\nClaude.ai - Risk and Investment Task:")

for _, row in claude_task2.iterrows():
    print(row["cluster_name"], "=", round(row["value"], 2), "%")

# Automation and Augmentation for Risk and Investment Task

api_task2_automation = api_task2[
    api_task2["cluster_name"].str.endswith(
        ("::directive", "::feedback loop"), na=False
    )
]["value"].sum()

api_task2_augmentation = api_task2[
    api_task2["cluster_name"].str.endswith(
        ("::learning", "::task iteration", "::validation"), na=False
    )
]["value"].sum()

claude_task2_automation = claude_task2[
    claude_task2["cluster_name"].str.endswith(
        ("::directive", "::feedback loop"), na=False
    )
]["value"].sum()

claude_task2_augmentation = claude_task2[
    claude_task2["cluster_name"].str.endswith(
        ("::learning", "::task iteration", "::validation"), na=False
    )
]["value"].sum()

print("\nRisk and Investment Task Comparison:")
print("API Automation:", round(api_task2_automation, 2), "%")
print("API Augmentation:", round(api_task2_augmentation, 2), "%")
print("Claude.ai Automation:", round(claude_task2_automation, 2), "%")
print("Claude.ai Augmentation:", round(claude_task2_augmentation, 2), "%")

# Risk and Investment Task Comparison Graph

categories = ["Automation", "Augmentation"]

api_task2_values = [
    api_task2_automation,
    api_task2_augmentation
]

claude_task2_values = [
    claude_task2_automation,
    claude_task2_augmentation
]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(8, 5))

bars1 = plt.bar(
    x - width/2,
    claude_task2_values,
    width,
    label="Claude.ai"
)

bars2 = plt.bar(
    x + width/2,
    api_task2_values,
    width,
    label="1P API"
)

plt.ylabel("Percentage (%)")
plt.title("Risk and Investment Task: Claude.ai vs 1P API")
plt.xticks(x, categories)
plt.ylim(0, 105)
plt.legend()

for bars in [bars1, bars2]:
    for bar in bars:
        value = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            value + 1,
            f"{value:.1f}%",
            ha="center"
        )

plt.tight_layout()

plt.savefig(
    "figures/risk_investment_task_comparison.png",
    bbox_inches="tight"
)

plt.close()

# =============================================================================
# ALL-TASKS ANALYSIS (this replaces doing task1, task2, task3... one by one)
# =============================================================================

# Step 1: Take ALL rows that are task-level collaboration data (same filter
# you already used for api_task1 / claude_task1, but WITHOUT picking one task)
api_all_tasks = api[
    (api["facet"] == "onet_task::collaboration") &
    (api["variable"] == "onet_task_collaboration_pct")
].copy()

claude_all_tasks = claude[
    (claude["geography"] == "global") &
    (claude["facet"] == "onet_task::collaboration") &
    (claude["variable"] == "onet_task_collaboration_pct")
].copy()

# Step 2: cluster_name looks like "task text::directive"
# We split it into two columns: task name, and collaboration type
api_all_tasks[["task", "collab_type"]] = api_all_tasks["cluster_name"].str.rsplit(
    "::", n=1, expand=True
)
claude_all_tasks[["task", "collab_type"]] = claude_all_tasks["cluster_name"].str.rsplit(
    "::", n=1, expand=True
)

# Step 3: label each row as "automation" or "augmentation"
# (this is the same rule you used with .isin(...) for automation/augmentation)
def bucket_collab_type(ct):
    if ct in ["directive", "feedback loop"]:
        return "automation"
    elif ct in ["learning", "task iteration", "validation"]:
        return "augmentation"
    else:
        return None  # not_classified / none -> we drop these

api_all_tasks["bucket"] = api_all_tasks["collab_type"].apply(bucket_collab_type)
claude_all_tasks["bucket"] = claude_all_tasks["collab_type"].apply(bucket_collab_type)

api_all_tasks = api_all_tasks.dropna(subset=["bucket"])
claude_all_tasks = claude_all_tasks.dropna(subset=["bucket"])

# Step 4: for each task, sum up the automation % and augmentation %
# groupby("task") = "do this separately for every unique task"
# unstack() = turn the automation/augmentation rows into two columns
api_summary = (
    api_all_tasks.groupby(["task", "bucket"])["value"].sum().unstack(fill_value=0)
)
claude_summary = (
    claude_all_tasks.groupby(["task", "bucket"])["value"].sum().unstack(fill_value=0)
)

api_summary = api_summary.rename(columns={"automation": "automation_api"})
claude_summary = claude_summary.rename(columns={"automation": "automation_claude"})

# Step 5: merge API and Claude.ai side by side, matched on the SAME task
comparison = api_summary[["automation_api"]].merge(
    claude_summary[["automation_claude"]], left_index=True, right_index=True
)

# Step 6: compute the difference for every task
comparison["diff"] = comparison["automation_api"] - comparison["automation_claude"]

print(f"\nNumber of matched tasks: {len(comparison)}")
print(comparison.head(10))
print(f"\nMean difference (API - Claude.ai): {comparison['diff'].mean():.2f} pp")
print(f"Median difference: {comparison['diff'].median():.2f} pp")

# =============================================================================
# HYPOTHESIS TEST (H1): is API automation % systematically higher than
# Claude.ai automation %, across all tasks, or could this be random noise?
# =============================================================================

from scipy import stats

# Paired t-test: compares the two columns task-by-task (paired), and tests
# whether the API column is *greater* than the Claude.ai column on average.
t_stat, p_value = stats.ttest_rel(
    comparison["automation_api"],
    comparison["automation_claude"],
    alternative="greater",
)

print(f"\nPaired t-test: t = {t_stat:.3f}, p = {p_value:.3e}")

if p_value < 0.05:
    print("=> p < 0.05, so we reject H0: the difference is statistically significant.")
    print("=> This supports H1: API automation % is systematically higher than Claude.ai.")
else:
    print("=> p >= 0.05, not enough evidence to reject H0.")

# =============================================================================
# HISTOGRAM: distribution of the difference (API - Claude.ai) across all tasks
# =============================================================================

plt.figure(figsize=(9, 5))

plt.hist(comparison["diff"], bins=30, color="#2E86AB", edgecolor="white")

# Draw a vertical line at the mean, so we can see where the average sits
mean_diff = comparison["diff"].mean()
plt.axvline(mean_diff, color="red", linestyle="--", linewidth=2,
            label=f"Mean = {mean_diff:.1f} pp")

# Draw a vertical line at 0, so we can see how far we are from "no difference"
plt.axvline(0, color="black", linestyle="-", linewidth=1,
            label="No difference (0)")

plt.xlabel("Difference in Automation % (API - Claude.ai)")
plt.ylabel("Number of Tasks")
plt.title("Distribution of Automation Gap Across 1,193 Matched Tasks")
plt.legend()
plt.tight_layout()

plt.savefig("figures/automation_gap_histogram.png", bbox_inches="tight")
plt.close()

print("\nHistogram saved to figures/automation_gap_histogram.png")

negative = comparison[comparison["diff"] < 0].sort_values("diff")
print(f"\nNegative tasks: {len(negative)} of {len(comparison)} "
      f"({len(negative) / len(comparison) * 100:.1f}%)")
print(negative[["automation_api", "automation_claude", "diff"]].to_string())

# =============================================================================
# REGRESSION MODEL - STEP 1: BUILD THE DATASET (one row per task x platform)
# =============================================================================
COLLAB_TYPES = ["directive", "feedback loop", "learning", "task iteration", "validation"]
AUTOMATION = ["directive", "feedback loop"]
AUGMENTATION = ["learning", "task iteration", "validation"]


def build_platform_table(df, platform_name):
    """Return one row per task with collaboration shares and usage volume."""
    if "geography" in df.columns:
        df = df[df["geography"] == "global"]

    # collaboration shares per task
    collab_rows = df[
        (df["facet"] == "onet_task::collaboration")
        & (df["variable"] == "onet_task_collaboration_pct")
    ].copy()
    collab_rows[["task", "collab_type"]] = collab_rows["cluster_name"].str.rsplit(
        "::", n=1, expand=True
    )

    # one column per collaboration type
    shares = collab_rows.pivot_table(
        index="task", columns="collab_type", values="value", aggfunc="sum", fill_value=0
    )
    for col in COLLAB_TYPES + ["none", "not_classified"]:
        if col not in shares.columns:
            shares[col] = 0.0

    out = pd.DataFrame(index=shares.index)
    for col in COLLAB_TYPES:
        out[col] = shares[col]
    out["automation_pct"] = shares[AUTOMATION].sum(axis=1)
    out["augmentation_pct"] = shares[AUGMENTATION].sum(axis=1)
    out["unclassified_pct"] = shares[["none", "not_classified"]].sum(axis=1)

    # usage volume = number of conversations for the task
    counts = df[(df["facet"] == "onet_task") & (df["variable"] == "onet_task_count")]
    counts = counts.set_index("cluster_name")["value"]
    out["volume"] = counts.reindex(out.index)

    out["platform"] = platform_name
    out["api"] = 1 if platform_name == "1P API" else 0   # dummy variable
    return out.reset_index()


api_tab = build_platform_table(api, "1P API")
claude_tab = build_platform_table(claude, "Claude.ai")


# keep tasks observed on BOTH platforms with some classified conversations
def classified_tasks(tab):
    return set(tab.loc[tab["automation_pct"] + tab["augmentation_pct"] > 0, "task"])


matched = classified_tasks(api_tab) & classified_tasks(claude_tab)

panel = pd.concat([api_tab, claude_tab], ignore_index=True)
panel = panel[panel["task"].isin(matched)].dropna(subset=["volume"])
panel = panel[panel["task"].map(panel["task"].value_counts()) == 2]
panel["log_volume"] = np.log(panel["volume"])

print(f"\nObservations: {len(panel)}  ({panel['task'].nunique()} tasks x 2 platforms)")
print(panel.groupby("platform")[["automation_pct", "unclassified_pct", "volume"]].mean().round(2))

# =============================================================================
# REGRESSION MODEL - STEP 2: MAIN MODEL
#   automation_pct = b0 + b1*api + b2*log_volume + e
# =============================================================================
# Standard errors are clustered by task, because the two rows of the same
# task (API and Claude.ai) are not independent observations.
task_groups = pd.factorize(panel["task"])[0]

main_model = smf.ols("automation_pct ~ api + log_volume", data=panel).fit(
    cov_type="cluster", cov_kwds={"groups": task_groups}
)

print("\n" + "=" * 70)
print("MAIN MODEL:  automation_pct = b0 + b1*api + b2*log_volume + e")
print("=" * 70)
print(main_model.summary())

# =============================================================================
# REGRESSION MODEL - STEP 3: ROBUSTNESS CHECKS
# Does the api coefficient stay the same when we add more controls?
# =============================================================================
def fit(formula):
    """OLS with standard errors clustered by task."""
    return smf.ols(formula, data=panel).fit(
        cov_type="cluster", cov_kwds={"groups": task_groups}
    )


models = {
    "(1) api only":          fit("automation_pct ~ api"),
    "(2) + log_volume":      fit("automation_pct ~ api + log_volume"),
    "(3) + unclassified":    fit("automation_pct ~ api + log_volume + unclassified_pct"),
    }

# comparison table: only the variables we care about (not the 1,192 task dummies)
rows = ["api", "log_volume", "unclassified_pct", "Intercept"]
results = pd.DataFrame(index=rows + ["R-squared", "N"])
for name, m in models.items():
    col = {}
    for var in rows:
        if var in m.params and not (var == "Intercept" and "C(task)" in m.model.formula):
            stars = "***" if m.pvalues[var] < 0.01 else "**" if m.pvalues[var] < 0.05 else "*" if m.pvalues[var] < 0.1 else ""
            col[var] = f"{m.params[var]:.3f}{stars}"
        else:
            col[var] = ""
    col["R-squared"] = f"{m.rsquared:.3f}"
    col["N"] = f"{int(m.nobs)}"
    results[name] = pd.Series(col)

print("\n" + "=" * 70)
print("ROBUSTNESS CHECKS (clustered SE by task; *** p<0.01, ** p<0.05, * p<0.1)")
print("=" * 70)
print(results.to_string())

"""
HOW do consumers (Claude.ai) and businesses (1P API) use AI differently
on the same task?

Part A - Collaboration types, task by task
    For every matched task, compare each of the five collaboration types
    (directive, feedback loop, learning, task iteration, validation)
    between the API and Claude.ai.
      A1. Summary table: mean gap per type, share of tasks where the API
          is higher, and a regression per type
          (same spec as the main model: y = b0 + b1*api + b2*log_volume).
      A2. Coefficient plot of the API effect per collaboration type.

Part B - Negative tasks (Claude.ai automates MORE than the API)
      B1. Table of all tasks with diff < 0.
      B2. Dumbbell chart: Claude.ai vs API automation for each negative task.

Data: Aug 2025 week (release_2025_09_15), same files as src/profile.py.
Run from the repository root:   python src/how_and_negatives.py
Outputs go to figures/ and tables/.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

API_FILE = "data/aei_raw_1p_api_2025-08-04_to_2025-08-11.csv"
CLAUDE_FILE = "data/aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv"

COLLAB_TYPES = ["directive", "feedback loop", "learning", "task iteration", "validation"]
AUTOMATION = ["directive", "feedback loop"]
AUGMENTATION = ["learning", "task iteration", "validation"]
TYPE_LABELS = {
    "directive": "Directive",
    "feedback loop": "Feedback loop",
    "learning": "Learning",
    "task iteration": "Task iteration",
    "validation": "Validation",
}

# same colors as the other figures (matplotlib defaults: C0 = Claude.ai, C1 = API)
CLAUDE_COLOR = "C0"
API_COLOR = "C1"

os.makedirs("figures", exist_ok=True)
os.makedirs("tables", exist_ok=True)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", 80)


# =============================================================================
# STEP 0: BUILD THE DATA (same logic as the regression section of profile.py)
# =============================================================================
def build_platform_table(df, platform_name):
    """Return one row per task with collaboration shares and usage volume."""
    if "geography" in df.columns:
        df = df[df["geography"] == "global"]

    collab_rows = df[
        (df["facet"] == "onet_task::collaboration")
        & (df["variable"] == "onet_task_collaboration_pct")
    ].copy()
    collab_rows[["task", "collab_type"]] = collab_rows["cluster_name"].str.rsplit(
        "::", n=1, expand=True
    )

    shares = collab_rows.pivot_table(
        index="task", columns="collab_type", values="value", aggfunc="sum", fill_value=0
    )
    for col in COLLAB_TYPES + ["none", "not_classified"]:
        if col not in shares.columns:
            shares[col] = 0.0

    out = pd.DataFrame(index=shares.index)
    for col in COLLAB_TYPES:
        out[col] = shares[col]
    out["automation_pct"] = shares[AUTOMATION].sum(axis=1)
    out["augmentation_pct"] = shares[AUGMENTATION].sum(axis=1)
    out["unclassified_pct"] = shares[["none", "not_classified"]].sum(axis=1)

    counts = df[(df["facet"] == "onet_task") & (df["variable"] == "onet_task_count")]
    counts = counts.set_index("cluster_name")["value"]
    out["volume"] = counts.reindex(out.index)

    out["platform"] = platform_name
    out["api"] = 1 if platform_name == "1P API" else 0
    return out.reset_index()


api = pd.read_csv(API_FILE)
claude = pd.read_csv(CLAUDE_FILE)

api_tab = build_platform_table(api, "1P API")
claude_tab = build_platform_table(claude, "Claude.ai")


def classified_tasks(tab):
    return set(tab.loc[tab["automation_pct"] + tab["augmentation_pct"] > 0, "task"])


matched = classified_tasks(api_tab) & classified_tasks(claude_tab)

# long format (one row per task x platform) -> used for the regressions
panel = pd.concat([api_tab, claude_tab], ignore_index=True)
panel = panel[panel["task"].isin(matched)].dropna(subset=["volume"])
panel = panel[panel["task"].map(panel["task"].value_counts()) == 2].copy()
panel["log_volume"] = np.log(panel["volume"])
task_groups = pd.factorize(panel["task"])[0]

# wide format (one row per task, API and Claude.ai side by side) -> per-task gaps
wide = (
    panel[panel["api"] == 1].set_index("task")
    .join(panel[panel["api"] == 0].set_index("task"), lsuffix="_api", rsuffix="_claude")
)
for col in COLLAB_TYPES + ["automation_pct", "augmentation_pct", "unclassified_pct"]:
    wide[f"diff_{col}"] = wide[f"{col}_api"] - wide[f"{col}_claude"]
wide["diff"] = wide["diff_automation_pct"]   # same 'diff' as in profile.py

n_tasks = len(wide)
print(f"Matched tasks: {n_tasks}  (should be 1,193 with the Aug 2025 data)")
print(f"Mean automation gap: {wide['diff'].mean():.2f} pp  (should be ~31.0)")


# =============================================================================
# PART A: COLLABORATION TYPES, TASK BY TASK
# =============================================================================

# ---- A1. Summary table --------------------------------------------------------
rows = []
for t in COLLAB_TYPES:
    d = wide[f"diff_{t}"]

    # regression, same spec as the main model, SE clustered by task
    panel["y"] = panel[t]
    m = smf.ols("y ~ api + log_volume", data=panel).fit(
        cov_type="cluster", cov_kwds={"groups": task_groups}
    )
    lo, hi = m.conf_int().loc["api"]

    rows.append({
        "collab_type": t,
        "mean_claude_pct": wide[f"{t}_claude"].mean(),
        "mean_api_pct": wide[f"{t}_api"].mean(),
        "mean_diff_pp": d.mean(),
        "pct_tasks_api_higher": (d > 0).mean() * 100,
        "pct_tasks_claude_higher": (d < 0).mean() * 100,
        "api_coef": m.params["api"],
        "ci_low": lo,
        "ci_high": hi,
    })

type_summary = pd.DataFrame(rows).set_index("collab_type")
type_summary.round(4).to_csv("tables/collab_type_summary.csv")

print("\n" + "=" * 78)
print("A1. COLLABORATION TYPES: API vs Claude.ai on the same tasks")
print("=" * 78)
print(type_summary[[
    "mean_claude_pct", "mean_api_pct", "mean_diff_pp",
    "pct_tasks_api_higher", "pct_tasks_claude_higher", "api_coef",
]].round(2).to_string())
print("\nNote: the five shares plus 'unclassified' add up to 100% within a task,")
print("so the gaps balance out: what the API gains in one type, it loses in others.")

# ---- A2. Coefficient plot -----------------------------------------------------
plot_df = type_summary.sort_values("api_coef")
y_pos = np.arange(len(plot_df))
colors = [API_COLOR if c > 0 else CLAUDE_COLOR for c in plot_df["api_coef"]]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.axvline(0, color="black", linewidth=1)
ax.errorbar(
    plot_df["api_coef"], y_pos,
    xerr=[plot_df["api_coef"] - plot_df["ci_low"], plot_df["ci_high"] - plot_df["api_coef"]],
    fmt="none", ecolor="gray", capsize=4, linewidth=1.5,
)
ax.scatter(plot_df["api_coef"], y_pos, color=colors, s=60, zorder=3)
span = plot_df["ci_high"].max() - plot_df["ci_low"].min()
for y, c, hi in zip(y_pos, plot_df["api_coef"], plot_df["ci_high"]):
    ax.text(hi + span * 0.02, y, f"{c:+.1f} pp", va="center", fontsize=9)
ax.set_xlim(min(plot_df["ci_low"].min(), 0) - span * 0.05,
            max(plot_df["ci_high"].max(), 0) + span * 0.15)
ax.set_yticks(y_pos)
ax.set_yticklabels([TYPE_LABELS[t] for t in plot_df.index])
ax.set_xlabel("API coefficient (pp)   ← more on Claude.ai  |  more on 1P API →")
ax.set_title(f"How the API differs from Claude.ai on the same task (n = {n_tasks:,} tasks)")
ax.text(1, -0.24, "Points: API coefficient, y = b0 + b1·api + b2·log_volume. "
        "Bars: 95% CI, SE clustered by task.",
        transform=ax.transAxes, ha="right", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("figures/collab_type_api_coefficients.png", dpi=150, bbox_inches="tight")
plt.close()


# =============================================================================
# PART B: NEGATIVE TASKS (Claude.ai automation > API automation)
# =============================================================================
neg = wide[wide["diff"] < 0].sort_values("diff")

# ---- B1. Table ----------------------------------------------------------------
neg_table = neg[[
    "automation_pct_claude", "automation_pct_api", "diff",
    "augmentation_pct_claude", "augmentation_pct_api",
    "unclassified_pct_claude", "unclassified_pct_api",
    "volume_claude", "volume_api",
]].round(2)
neg_table.to_csv("tables/negative_tasks.csv")

print("\n" + "=" * 78)
print(f"B1. NEGATIVE TASKS: {len(neg)} of {n_tasks} ({len(neg) / n_tasks * 100:.1f}%)")
print("=" * 78)
print(neg_table[["automation_pct_claude", "automation_pct_api", "diff",
                 "volume_claude", "volume_api"]].to_string())

# ---- B2. Dumbbell chart -------------------------------------------------------
MAX_SHOWN = 30
show = neg.head(MAX_SHOWN).iloc[::-1]   # most negative at the top


def short(text, n=65):
    return text if len(text) <= n else text[: n - 1] + "…"


if len(show) > 0:
    fig, ax = plt.subplots(figsize=(10, max(3.0, 0.32 * len(show) + 1.6)))
    y = np.arange(len(show))
    ax.hlines(y, show["automation_pct_api"], show["automation_pct_claude"],
              color="lightgray", linewidth=2.5, zorder=1)
    ax.scatter(show["automation_pct_claude"], y, color=CLAUDE_COLOR, s=40,
               label="Claude.ai", zorder=2)
    ax.scatter(show["automation_pct_api"], y, color=API_COLOR, s=40,
               label="1P API", zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels([short(t) for t in show.index], fontsize=8)
    ax.set_xlabel("Automation share of the task (%)")
    ax.set_xlim(0, 100)
    shown = f"the {len(show)} most negative of {len(neg)}" if len(neg) > MAX_SHOWN else f"all {len(neg)}"
    ax.set_title(f"Tasks where Claude.ai automates more than the API ({shown})", pad=26)
    ax.set_ylim(-0.7, len(show) - 0.3)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig("figures/negative_tasks_dumbbell.png", dpi=150, bbox_inches="tight")
    plt.close()

print("\nSaved figures: collab_type_api_coefficients.png"
      + (", negative_tasks_dumbbell.png" if len(neg) > 0 else " (no negative tasks -> no dumbbell)"))
print("Saved tables:  tables/collab_type_summary.csv, tables/negative_tasks.csv")

# =============================================================================
# WEEK 9-10  REPLICATION ON THE FEBRUARY 2026 RELEASE
# =============================================================================
# Research question (unchanged): do consumers (Claude.ai) and businesses
# (1P API) use AI differently on the same tasks?
#
# Weeks 2-8 above used the 2025-09-15 release (data for 2025-08-04 .. 08-11).
# This section re-runs the SAME analysis on the 2026-03-24 release (data for
# 2026-02-05 .. 02-12) and puts the two periods side by side. The point is
# external validity: if the gap is real and not an artifact of one week, the
# coefficients should reproduce.
#
# Nothing in the method changes - same collaboration buckets, same task
# matching rule, same paired t-test, same regression with standard errors
# clustered by task. Only the input files change.
#
# Everything below is prefixed w9_ / W9_ so it does not clash with the
# Week 2-8 names above (W9_COLLAB_TYPES, w9_build_platform_table, ...). This
# section is self-contained: it does not read any variable defined earlier.
#
#   PART 1  Automation vs augmentation, global shares (both platforms)
#   PART 2  Hypothesis test on the same-task automation gap
#   PART 3  Regression model + robustness checks
#   PART 4  Which collaboration types drive the gap
#   PART 5  Side-by-side comparison with Aug 2025 (the replication table)
#
# Writes figures/feb2026_*.png and tables/week9_*.csv
# =============================================================================
 
import glob     # os, pandas, numpy, pyplot, smf and stats are imported above
 
 
# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
 
# Resolve paths from this file's location, NOT from the shell's working
# directory. The repo is often opened one folder above the project folder,
# and a bare "data" would then point at the wrong place.
_W9_HERE = os.path.dirname(os.path.abspath(__file__))     # .../src
W9_ROOT = os.path.dirname(_W9_HERE)                          # .../<project root>
 
W9_DATA_DIR = os.path.join(W9_ROOT, "data")
W9_FIG_DIR = os.path.join(W9_ROOT, "figures")
W9_TAB_DIR = os.path.join(W9_ROOT, "tables")
 
# The two releases we compare. Keys are short labels used in every table.
# Each entry gives the date range in the filename. The loader matches on
# platform + date range, so a browser suffix like " (1)" or "__1_" from a
# second download does not need renaming.
W9_RELEASES = {
    "2025-08": {
        "claude": "claude_ai_2025-08-04_to_2025-08-11",
        "api": "1p_api_2025-08-04_to_2025-08-11",
        "release": "release_2025_09_15",
    },
    "2026-02": {
        "claude": "claude_ai_2026-02-05_to_2026-02-12",
        "api": "1p_api_2026-02-05_to_2026-02-12",
        "release": "release_2026_03_24",
    },
}
 
# Collaboration taxonomy. IMPORTANT: the labels contain SPACES, not
# underscores. "feedback_loop" silently matches nothing and would drop a
# whole automation category.
W9_COLLAB_TYPES = ["directive", "feedback loop", "learning", "task iteration", "validation"]
W9_AUTOMATION = ["directive", "feedback loop"]
W9_AUGMENTATION = ["learning", "task iteration", "validation"]
 
# Colors. Kept consistent with the Week 8 dumbbell figure:
# blue = Claude.ai (consumer), orange = 1P API (business).
C_CLAUDE = "#2a78d6"
C_API = "#eb6834"
# Periods get their own two hues so platform colors keep their meaning.
C_AUG25 = "#1baf7a"
C_FEB26 = "#6250d6"
C_INK = "#0b0b0b"
C_MUTED = "#52514e"
C_GRID = "#d8d7d2"
 
 
def w9_style_axes(ax, ylabel=None, title=None, xlabel=None):
    """Recessive grid and axes, ink-colored text. Applied to every figure."""
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=C_GRID, linewidth=0.8)
    ax.xaxis.grid(False)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(C_GRID)
    ax.tick_params(colors=C_MUTED, labelsize=9, length=0)
    if ylabel:
        ax.set_ylabel(ylabel, color=C_MUTED, fontsize=10)
    if xlabel:
        ax.set_xlabel(xlabel, color=C_MUTED, fontsize=10)
    if title:
        ax.set_title(title, color=C_INK, fontsize=12, pad=12, loc="left")
 
 
# --------------------------------------------------------------------------
# LOADING
# --------------------------------------------------------------------------
 
def w9_find_csv(token):
    """Find the one CSV in data/ whose name contains `token`.
 
    Tolerates download suffixes, so both
        aei_raw_1p_api_2026-02-05_to_2026-02-12.csv
        aei_raw_1p_api_2026-02-05_to_2026-02-12 (1).csv
    are found. Raises a readable error listing what IS in data/.
    """
    hits = [
        p for p in glob.glob(os.path.join(W9_DATA_DIR, "*.csv"))
        if token in os.path.basename(p)
    ]
    if not hits:
        present = sorted(os.path.basename(p)
                         for p in glob.glob(os.path.join(W9_DATA_DIR, "*.csv")))
        raise FileNotFoundError(
            f"\n  No CSV matching '{token}' in {W9_DATA_DIR}"
            f"\n  Files currently in data/: {present if present else 'none'}"
            f"\n  Download the release from Hugging Face and put the CSV there."
        )
    # Shortest name wins, so the original beats a " (1)" copy.
    return sorted(hits, key=len)[0]
 
 
def w9_load_release(period):
    """Read the Claude.ai and 1P API raw CSVs for one period."""
    cfg = W9_RELEASES[period]
    out = {}
    for platform in ["claude", "api"]:
        path = w9_find_csv(cfg[platform])
        df = pd.read_csv(path, low_memory=False)
        out[platform] = df
        print(
            f"  {period}  {platform:6s}  {len(df):>8,} rows  "
            f"{df['facet'].nunique():>3} facets  "
            f"[{df['platform_and_product'].unique()[0]}]"
        )
    return out
 
 
# --------------------------------------------------------------------------
# PART 1 - GLOBAL W9_AUTOMATION VS W9_AUGMENTATION
# --------------------------------------------------------------------------
 
def w9_global_shares(df):
    """Overall automation / augmentation share for one platform."""
    collab = df[
        (df["geography"] == "global")
        & (df["facet"] == "collaboration")
        & (df["variable"] == "collaboration_pct")
    ]
    automation = collab[collab["cluster_name"].isin(W9_AUTOMATION)]["value"].sum()
    augmentation = collab[collab["cluster_name"].isin(W9_AUGMENTATION)]["value"].sum()
    return automation, augmentation
 
 
def w9_part1_shares(frames, period):
    print(f"\n{'=' * 72}")
    print(f"PART 1  Automation vs augmentation, global shares  ({period})")
    print(f"{'=' * 72}")
 
    shares = {}
    for platform, label in [("claude", "Claude.ai"), ("api", "1P API")]:
        auto, aug = w9_global_shares(frames[platform])
        shares[label] = (auto, aug)
        print(f"  {label:<10}  automation {auto:6.2f}%   augmentation {aug:6.2f}%")
 
    # Grouped bars: two platforms x two buckets.
    fig, ax = plt.subplots(figsize=(7, 4.6))
    groups = ["Automation", "Augmentation"]
    x = np.arange(len(groups))
    width = 0.34
 
    for i, (label, color) in enumerate([("Claude.ai", C_CLAUDE), ("1P API", C_API)]):
        vals = shares[label]
        bars = ax.bar(
            x + (i - 0.5) * (width + 0.02), vals, width,
            label=label, color=color, edgecolor="#fcfcfb", linewidth=2,
        )
        # Direct labels on every bar - only 4 bars, so no clutter, and the
        # validator flagged a contrast WARN that labels relieve.
        for bar, v in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2, v + 1.2, f"{v:.1f}%",
                ha="center", va="bottom", fontsize=9, color=C_INK,
            )
 
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylim(0, max(max(v) for v in shares.values()) * 1.22)
    w9_style_axes(ax, ylabel="Share of conversations (%)",
               title=f"Automation vs augmentation, {period}")
    ax.legend(frameon=False, fontsize=9, labelcolor=C_MUTED, loc="upper right")
    fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_claude_vs_api.png"),
                bbox_inches="tight", dpi=200)
    plt.close(fig)
 
    return shares
 
 
# --------------------------------------------------------------------------
# PART 2 - HYPOTHESIS TEST ON THE SAME-TASK W9_AUTOMATION GAP
# --------------------------------------------------------------------------
# H0: mean(diff) = 0        no difference on the same task
# H1: mean(diff) > 0        automation share is higher on the API
#     where diff(t) = automation%_API(t) - automation%_Claude.ai(t)
 
def w9_bucket_collab_type(ct):
    """Map a collaboration label to automation / augmentation, or drop it."""
    if ct in W9_AUTOMATION:
        return "automation"
    elif ct in W9_AUGMENTATION:
        return "augmentation"
    else:
        return None      # not_classified / none -> dropped
 
 
def w9_task_automation(df):
    """Automation % per O*NET task for one platform (global level only)."""
    rows = df[
        (df["geography"] == "global")
        & (df["facet"] == "onet_task::collaboration")
        & (df["variable"] == "onet_task_collaboration_pct")
    ].copy()
 
    # cluster_name is "<task text>::<collaboration label>"
    rows[["task", "collab_type"]] = rows["cluster_name"].str.rsplit(
        "::", n=1, expand=True
    )
    rows["bucket"] = rows["collab_type"].apply(w9_bucket_collab_type)
    rows = rows.dropna(subset=["bucket"])
 
    summary = rows.groupby(["task", "bucket"])["value"].sum().unstack(fill_value=0)
    for col in ["automation", "augmentation"]:
        if col not in summary.columns:
            summary[col] = 0.0
    return summary
 
 
def w9_part2_ttest(frames, period, make_figure=True):
    print(f"\n{'=' * 72}")
    print(f"PART 2  Hypothesis test on the same-task automation gap  ({period})")
    print(f"{'=' * 72}")
 
    api_summary = w9_task_automation(frames["api"]).rename(
        columns={"automation": "automation_api"}
    )
    claude_summary = w9_task_automation(frames["claude"]).rename(
        columns={"automation": "automation_claude"}
    )
 
    # Match on the SAME task. A task only appears here if it had at least one
    # classified conversation on that platform, so tasks that are entirely
    # not_classified drop out on their own.
    comparison = api_summary[["automation_api"]].merge(
        claude_summary[["automation_claude"]], left_index=True, right_index=True
    )
    comparison["diff"] = comparison["automation_api"] - comparison["automation_claude"]
 
    t_stat, p_value = stats.ttest_rel(
        comparison["automation_api"],
        comparison["automation_claude"],
        alternative="greater",
    )
 
    n_neg = int((comparison["diff"] < 0).sum())
    print(f"  matched tasks (n)        {len(comparison):>9,}")
    print(f"  mean   diff (API - C.ai) {comparison['diff'].mean():>9.2f} pp")
    print(f"  median diff              {comparison['diff'].median():>9.2f} pp")
    print(f"  std dev of diff          {comparison['diff'].std():>9.2f} pp")
    print(f"  t-statistic              {t_stat:>9.2f}")
    print(f"  p-value                  {p_value:>9.3e}")
    print(f"  tasks with diff < 0      {n_neg:>9,}  "
          f"({n_neg / len(comparison) * 100:.1f}%)")
    print(f"  conclusion               "
          f"{'reject H0 -> H1 supported' if p_value < 0.05 else 'fail to reject H0'}")
 
    if make_figure:
        fig, ax = plt.subplots(figsize=(7.5, 4.6))
        counts, _, _ = ax.hist(comparison["diff"], bins=40, color=C_CLAUDE,
                               edgecolor="#fcfcfb", linewidth=0.8)
        # Headroom so the annotations sit in clear space, not on the bars.
        ax.set_ylim(0, counts.max() * 1.22)
        mean_diff = comparison["diff"].mean()
        # Zero is the decision line for H0 - mark it, and mark the mean.
        ax.axvline(0, color=C_INK, linewidth=1.4)
        ax.axvline(mean_diff, color=C_API, linewidth=2, linestyle="--")
        ax.text(mean_diff, counts.max() * 1.16, f"  mean {mean_diff:.1f} pp",
                color=C_API, fontsize=9, va="center", ha="left")
        ax.text(0, counts.max() * 1.16, "H0: no difference  ",
                color=C_MUTED, fontsize=9, ha="right", va="center")
        w9_style_axes(
            ax,
            xlabel="Automation gap (1P API - Claude.ai), percentage points",
            ylabel="Number of tasks",
            title=f"Distribution of the same-task automation gap, {period}",
        )
        fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_automation_gap_histogram.png"),
                    bbox_inches="tight", dpi=200)
        plt.close(fig)
 
    result = {
        "period": period,
        "n_tasks": len(comparison),
        "mean_diff": comparison["diff"].mean(),
        "median_diff": comparison["diff"].median(),
        "sd_diff": comparison["diff"].std(),
        "t_stat": t_stat,
        "p_value": p_value,
        "pct_negative": n_neg / len(comparison) * 100,
    }
    return comparison, result
 
 
# --------------------------------------------------------------------------
# PART 3 - REGRESSION MODEL
# --------------------------------------------------------------------------
#   automation_pct = b0 + b1*api + b2*log_volume + e
# One row per task x platform, so each task appears twice. Standard errors
# are clustered by task because those two rows are not independent.
 
def w9_build_platform_table(df, platform_name):
    """One row per task: collaboration shares plus usage volume."""
    df = df[df["geography"] == "global"]
 
    collab_rows = df[
        (df["facet"] == "onet_task::collaboration")
        & (df["variable"] == "onet_task_collaboration_pct")
    ].copy()
    collab_rows[["task", "collab_type"]] = collab_rows["cluster_name"].str.rsplit(
        "::", n=1, expand=True
    )
 
    shares = collab_rows.pivot_table(
        index="task", columns="collab_type", values="value",
        aggfunc="sum", fill_value=0,
    )
    for col in W9_COLLAB_TYPES + ["none", "not_classified"]:
        if col not in shares.columns:
            shares[col] = 0.0
 
    out = pd.DataFrame(index=shares.index)
    for col in W9_COLLAB_TYPES:
        out[col] = shares[col]
    out["automation_pct"] = shares[W9_AUTOMATION].sum(axis=1)
    out["augmentation_pct"] = shares[W9_AUGMENTATION].sum(axis=1)
    out["unclassified_pct"] = shares[["none", "not_classified"]].sum(axis=1)
 
    counts = df[(df["facet"] == "onet_task") & (df["variable"] == "onet_task_count")]
    counts = counts.set_index("cluster_name")["value"]
    out["volume"] = counts.reindex(out.index)
 
    out["platform"] = platform_name
    out["api"] = 1 if platform_name == "1P API" else 0
    return out.reset_index()
 
 
def w9_classified_tasks(tab):
    """Tasks with at least some classified conversations."""
    return set(tab.loc[tab["automation_pct"] + tab["augmentation_pct"] > 0, "task"])
 
 
def w9_build_panel(frames):
    api_tab = w9_build_platform_table(frames["api"], "1P API")
    claude_tab = w9_build_platform_table(frames["claude"], "Claude.ai")
 
    matched = w9_classified_tasks(api_tab) & w9_classified_tasks(claude_tab)
 
    panel = pd.concat([api_tab, claude_tab], ignore_index=True)
    panel = panel[panel["task"].isin(matched)].dropna(subset=["volume"])
    # Keep only tasks that survived on BOTH platforms (exactly 2 rows).
    panel = panel[panel["task"].map(panel["task"].value_counts()) == 2]
    panel["log_volume"] = np.log(panel["volume"])
    return panel
 
 
def w9_stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
 
 
def w9_part3_regression(frames, period):
    print(f"\n{'=' * 72}")
    print(f"PART 3  Regression model  ({period})")
    print(f"{'=' * 72}")
 
    panel = w9_build_panel(frames)
    task_groups = pd.factorize(panel["task"])[0]
 
    print(f"  observations {len(panel):,}  "
          f"({panel['task'].nunique():,} tasks x 2 platforms)")
    print(panel.groupby("platform")[
        ["automation_pct", "augmentation_pct", "unclassified_pct", "volume"]
    ].mean().round(2).to_string())
 
    def fit(formula):
        """OLS with standard errors clustered by task."""
        return smf.ols(formula, data=panel).fit(
            cov_type="cluster", cov_kwds={"groups": task_groups}
        )
 
    models = {
        "(1) api only": fit("automation_pct ~ api"),
        "(2) + log_volume": fit("automation_pct ~ api + log_volume"),
        "(3) + unclassified": fit("automation_pct ~ api + log_volume + unclassified_pct"),
    }
 
    print("\n  MAIN MODEL: automation_pct = b0 + b1*api + b2*log_volume + e")
    week9_main = models["(2) + log_volume"]
    print(f"    api coefficient  {week9_main.params['api']:.3f} pp   "
          f"SE {week9_main.bse['api']:.3f}   p {week9_main.pvalues['api']:.3e}")
    ci = week9_main.conf_int().loc["api"]
    print(f"    95% CI           [{ci[0]:.3f}, {ci[1]:.3f}]")
 
    rows = ["api", "log_volume", "unclassified_pct", "Intercept"]
    table = pd.DataFrame(index=rows + ["R-squared", "N"])
    for name, m in models.items():
        col = {}
        for var in rows:
            col[var] = (f"{m.params[var]:.3f}{w9_stars(m.pvalues[var])}"
                        if var in m.params.index else "")
        col["R-squared"] = f"{m.rsquared:.3f}"
        col["N"] = f"{int(m.nobs)}"
        table[name] = pd.Series(col)
 
    print("\n  ROBUSTNESS CHECKS (clustered SE by task; *** p<0.01, ** p<0.05, * p<0.1)")
    print(table.to_string())
 
    coefs = {name: (m.params["api"], m.bse["api"], m.pvalues["api"])
             for name, m in models.items()}
    return panel, table, coefs
 
 
# --------------------------------------------------------------------------
# PART 4 - WHICH COLLABORATION TYPES DRIVE THE GAP
# --------------------------------------------------------------------------
# The regression above shows *that* the API automates more. This shows *how*:
# one regression per collaboration type, same specification as the week9_main model.
 
def w9_part4_collab_types(panel, period, make_figure=True):
    print(f"\n{'=' * 72}")
    print(f"PART 4  Collaboration types on the same task  ({period})")
    print(f"{'=' * 72}")
 
    task_groups = pd.factorize(panel["task"])[0]
    wide = panel.pivot(index="task", columns="platform", values=W9_COLLAB_TYPES)
 
    rows = []
    for ct in W9_COLLAB_TYPES:
        # statsmodels formulas can't handle spaces, so use a safe column name.
        d = panel.rename(columns={ct: "share"})
        m = smf.ols("share ~ api + log_volume", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": task_groups}
        )
        api_share = panel.loc[panel["api"] == 1, ct]
        claude_share = panel.loc[panel["api"] == 0, ct]
        higher = (wide[ct]["1P API"] > wide[ct]["Claude.ai"]).mean() * 100
        rows.append({
            "period": period,
            "collab_type": ct,
            "claude_mean_pct": claude_share.mean(),
            "api_mean_pct": api_share.mean(),
            "api_coef_pp": m.params["api"],
            "se": m.bse["api"],
            "p_value": m.pvalues["api"],
            "api_higher_pct_of_tasks": higher,
        })
 
    decomp = pd.DataFrame(rows)
    print(decomp.drop(columns=["period"]).to_string(
        index=False,
        formatters={
            "claude_mean_pct": "{:.1f}".format,
            "api_mean_pct": "{:.1f}".format,
            "api_coef_pp": "{:+.2f}".format,
            "se": "{:.2f}".format,
            "p_value": "{:.2e}".format,
            "api_higher_pct_of_tasks": "{:.1f}".format,
        },
    ))
 
    if make_figure:
        # Horizontal bars with 95% CI. Sorted so the story reads top to bottom.
        d = decomp.sort_values("api_coef_pp")
        fig, ax = plt.subplots(figsize=(7.5, 4.2))
        y = np.arange(len(d))
        ax.barh(y, d["api_coef_pp"], height=0.55, color=C_API,
                edgecolor="#fcfcfb", linewidth=2)
        ax.errorbar(d["api_coef_pp"], y, xerr=1.96 * d["se"], fmt="none",
                    ecolor=C_INK, elinewidth=1.2, capsize=3)
        ax.axvline(0, color=C_INK, linewidth=1.2)
        for yi, v in zip(y, d["api_coef_pp"]):
            off = 1.2 if v >= 0 else -1.2
            ax.text(v + off, yi, f"{v:+.1f}", va="center",
                    ha="left" if v >= 0 else "right",
                    fontsize=9, color=C_INK)
        ax.set_yticks(y)
        ax.set_yticklabels(d["collab_type"])
        span = d["api_coef_pp"].max() - d["api_coef_pp"].min()
        ax.set_xlim(d["api_coef_pp"].min() - 0.22 * span,
                    d["api_coef_pp"].max() + 0.22 * span)
        w9_style_axes(ax, xlabel="API effect on share (percentage points)",
                   title=f"Where the gap comes from, {period}")
        ax.xaxis.grid(True, color=C_GRID, linewidth=0.8)
        ax.yaxis.grid(False)
        fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_collab_type_coefficients.png"),
                    bbox_inches="tight", dpi=200)
        plt.close(fig)
 
    return decomp
 
 
# --------------------------------------------------------------------------
# PART 5 - SIDE BY SIDE WITH AUG 2025 (the replication table)
# --------------------------------------------------------------------------
 
def w9_part5_compare(summaries, decomps, coef_sets):
    print(f"\n{'=' * 72}")
    print("PART 5  Replication: Aug 2025 vs Feb 2026")
    print(f"{'=' * 72}")
 
    summary = pd.DataFrame(summaries).set_index("period")
    print("\n  Hypothesis test")
    print(summary.T.to_string(float_format=lambda v: f"{v:,.3g}"))
 
    print("\n  Main regression, api coefficient (pp)")
    coef_tab = pd.DataFrame(
        {per: {name: f"{c[0]:.3f}{w9_stars(c[2])}" for name, c in cs.items()}
         for per, cs in coef_sets.items()}
    )
    print(coef_tab.to_string())
 
    decomp = pd.concat(decomps, ignore_index=True)
    pivot = decomp.pivot(index="collab_type", columns="period", values="api_coef_pp")
    pivot = pivot.reindex(W9_COLLAB_TYPES)
    print("\n  API effect by collaboration type (pp)")
    print(pivot.to_string(float_format=lambda v: f"{v:+.1f}"))
 
    # Paired horizontal bars, one pair per collaboration type.
    d = pivot.loc[pivot.mean(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    y = np.arange(len(d))
    h = 0.34
    for i, (per, color) in enumerate([("2025-08", C_AUG25), ("2026-02", C_FEB26)]):
        bars = ax.barh(y + (0.5 - i) * (h + 0.02), d[per], height=h,
                       label=per, color=color, edgecolor="#fcfcfb", linewidth=2)
        for bar, v in zip(bars, d[per]):
            off = 1.2 if v >= 0 else -1.2
            ax.text(v + off, bar.get_y() + bar.get_height() / 2, f"{v:+.1f}",
                    va="center", ha="left" if v >= 0 else "right",
                    fontsize=8.5, color=C_INK)
    ax.axvline(0, color=C_INK, linewidth=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(d.index)
    span = d.values.max() - d.values.min()
    ax.set_xlim(d.values.min() - 0.22 * span, d.values.max() + 0.22 * span)
    w9_style_axes(ax, xlabel="API effect on share (percentage points)",
               title="The gap reproduces six months later")
    ax.xaxis.grid(True, color=C_GRID, linewidth=0.8)
    ax.yaxis.grid(False)
    ax.legend(frameon=False, fontsize=9, labelcolor=C_MUTED, loc="lower right")
    fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_replication_comparison.png"),
                bbox_inches="tight", dpi=200)
    plt.close(fig)
 
    return summary, coef_tab, pivot
 
 
# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
 
def week9_main():
    os.makedirs(W9_FIG_DIR, exist_ok=True)
    os.makedirs(W9_TAB_DIR, exist_ok=True)
 
    print("Loading releases")
    data = {per: w9_load_release(per) for per in W9_RELEASES}
 
    summaries, decomps, coef_sets, tables = [], [], {}, {}
 
    # Feb 2026 is the new period: full analysis with figures.
    # Aug 2025 is re-run with the identical code so the two periods are
    # comparable - no figures, those already exist from Weeks 2-8.
    for period in ["2026-02", "2025-08"]:
        is_new = period == "2026-02"
        if is_new:
            w9_part1_shares(data[period], period)
        comparison, result = w9_part2_ttest(data[period], period, make_figure=is_new)
        panel, table, coefs = w9_part3_regression(data[period], period)
        decomp = w9_part4_collab_types(panel, period, make_figure=is_new)
 
        summaries.append(result)
        decomps.append(decomp)
        coef_sets[period] = coefs
        tables[period] = table
        if is_new:
            comparison.to_csv(os.path.join(W9_TAB_DIR, "week9_feb2026_task_gaps.csv"))
            table.to_csv(os.path.join(W9_TAB_DIR, "week9_feb2026_regression.csv"))
 
    # Order the summary with the earlier period first.
    summaries = sorted(summaries, key=lambda r: r["period"])
    decomps = sorted(decomps, key=lambda d: d["period"].iloc[0])
    coef_sets = dict(sorted(coef_sets.items()))
 
    summary, coef_tab, pivot = w9_part5_compare(summaries, decomps, coef_sets)
 
    summary.to_csv(os.path.join(W9_TAB_DIR, "week9_period_summary.csv"))
    coef_tab.to_csv(os.path.join(W9_TAB_DIR, "week9_period_coefficients.csv"))
    pivot.to_csv(os.path.join(W9_TAB_DIR, "week9_period_collab_decomp.csv"))
 
    print(f"\n  figures -> {W9_FIG_DIR}/feb2026_*.png")
    print(f"  tables  -> {W9_TAB_DIR}/week9_*.csv")
 
 
# profile.py runs top to bottom, so call the Week 9-10 section directly.
week9_main()

 # =============================================================================
# WEEK 11  WHY DOES THE GAP EXIST? USE_CASE AND HUMAN_ONLY_ABILITY
# =============================================================================
# Weeks 9-10 showed the automation gap reproduces on a second release. This
# section uses two facets that only exist from the 2026-01-15 release onward
# to ask two questions the August data could not answer.
#
#   1. Is the consumer/business proxy correct at all? The whole project assumes
#      Claude.ai = consumers and 1P API = businesses, but never tested it.
#      `use_case` labels every conversation work / personal / coursework, so
#      the assumption can be checked instead of assumed.
#
#   2. Is the gap just "work tasks vs personal tasks"? If the API automates
#      more only because it handles work while Claude.ai handles personal
#      things, then the finding is about task mix, not about who the user is.
#      Adding work_pct to the regression tests this directly.
#
# `human_only_ability` (could the user have done the task without Claude?)
# is added as a second control and as a question of its own.
#
# Everything is prefixed w11_ / W11_. This section REUSES helpers defined in
# the Week 9-10 section above (w9_load_release, w9_style_axes, w9_stars,
# C_CLAUDE, C_API, W9_FIG_DIR, W9_TAB_DIR), so keep that section in place.
#
#   PART 1  use_case: does the consumer/business proxy hold?
#   PART 2  human_only_ability: could the user have done it alone?
#   PART 3  Does the api coefficient survive these two controls?
#
# Writes figures/feb2026_use_case.png, feb2026_human_only_ability.png,
# feb2026_api_coefficient_controls.png and tables/week11_*.csv
# =============================================================================

W11_PERIOD = "2026-02"
W11_COLLAB_TYPES = ["directive", "feedback loop", "learning", "task iteration", "validation"]
W11_AUTOMATION = ["directive", "feedback loop"]
W11_AUGMENTATION = ["learning", "task iteration", "validation"]


def w11_wide(df, facet, variable):
    """Task x label table of percentages for an intersection facet."""
    rows = df[
        (df["geography"] == "global")
        & (df["facet"] == facet)
        & (df["variable"] == variable)
    ].copy()
    split = rows["cluster_name"].str.rsplit("::", n=1, expand=True)
    rows["task"], rows["label"] = split[0], split[1]
    return rows.pivot_table(
        index="task", columns="label", values="value", aggfunc="sum"
    ).fillna(0.0)


def w11_global_shares(df, facet, variable):
    """Overall shares for one platform, not split by task."""
    rows = df[
        (df["geography"] == "global")
        & (df["facet"] == facet)
        & (df["variable"] == variable)
    ]
    return rows.groupby("cluster_name")["value"].sum()


# -----------------------------------------------------------------------------
# PANEL - one row per task x platform, with the Week 11 variables attached
# -----------------------------------------------------------------------------

def w11_build_panel(frames):
    def one(df, platform_name):
        shares = w11_wide(df, "onet_task::collaboration", "onet_task_collaboration_pct")
        for col in W11_COLLAB_TYPES + ["none", "not_classified"]:
            if col not in shares.columns:
                shares[col] = 0.0

        out = pd.DataFrame(index=shares.index)
        out["automation_pct"] = shares[W11_AUTOMATION].sum(axis=1)
        out["augmentation_pct"] = shares[W11_AUGMENTATION].sum(axis=1)
        out["unclassified_pct"] = shares[["none", "not_classified"]].sum(axis=1)

        use_case = w11_wide(df, "onet_task::use_case", "onet_task_use_case_pct")
        for col in ["work", "personal", "coursework"]:
            out[f"{col}_pct"] = use_case.reindex(out.index).get(col)

        ability = w11_wide(
            df, "onet_task::human_only_ability", "onet_task_human_only_ability_pct"
        )
        out["human_only_yes_pct"] = ability.reindex(out.index).get("yes")
        out["human_only_no_pct"] = ability.reindex(out.index).get("no")

        counts = df[
            (df["geography"] == "global")
            & (df["facet"] == "onet_task")
            & (df["variable"] == "onet_task_count")
        ]
        out["volume"] = counts.set_index("cluster_name")["value"].reindex(out.index)

        out["platform"] = platform_name
        out["api"] = 1 if platform_name == "1P API" else 0
        return out.reset_index()

    api_tab = one(frames["api"], "1P API")
    claude_tab = one(frames["claude"], "Claude.ai")

    # Same matching rule as Weeks 6-10: classified conversations on both sides.
    def classified(tab):
        return set(tab.loc[tab["automation_pct"] + tab["augmentation_pct"] > 0, "task"])

    matched = classified(api_tab) & classified(claude_tab)

    panel = pd.concat([api_tab, claude_tab], ignore_index=True)
    panel = panel[panel["task"].isin(matched)]
    panel = panel.dropna(subset=["volume", "work_pct", "human_only_yes_pct"])
    panel = panel[panel["task"].map(panel["task"].value_counts()) == 2]
    panel["log_volume"] = np.log(panel["volume"])
    return panel


# -----------------------------------------------------------------------------
# PART 1 - use_case: does the consumer/business proxy hold?
# -----------------------------------------------------------------------------

def w11_part1_use_case(frames, panel):
    print(f"\n{'=' * 72}")
    print("PART 1  use_case: is Claude.ai really consumer and the API business?")
    print(f"{'=' * 72}")

    print("\n  Overall shares (all conversations, global)")
    print(f"    {'category':<16}{'Claude.ai':>11}{'1P API':>10}")
    overall = {}
    for platform, key in [("Claude.ai", "claude"), ("1P API", "api")]:
        overall[platform] = w11_global_shares(frames[key], "use_case", "use_case_pct")
    for cat in ["work", "personal", "coursework"]:
        c_val = overall["Claude.ai"].get(cat, 0.0)
        a_val = overall["1P API"].get(cat, 0.0)
        print(f"    {cat:<16}{c_val:>10.2f}%{a_val:>9.2f}%")

    print("\n  Same-task comparison (mean across matched tasks)")
    print(f"    {'category':<16}{'Claude.ai':>11}{'1P API':>10}{'diff':>11}{'p':>12}")
    rows = []
    for cat in ["work", "personal", "coursework"]:
        col = f"{cat}_pct"
        a_vals = panel.loc[panel["api"] == 1, col].to_numpy()
        c_vals = panel.loc[panel["api"] == 0, col].to_numpy()
        t_stat, p_val = stats.ttest_rel(a_vals, c_vals)
        print(f"    {cat:<16}{c_vals.mean():>10.1f}%{a_vals.mean():>9.1f}%"
              f"{a_vals.mean() - c_vals.mean():>+10.1f}pp{p_val:>12.2e}")
        rows.append({
            "category": cat,
            "claude_pct": c_vals.mean(), "api_pct": a_vals.mean(),
            "diff_pp": a_vals.mean() - c_vals.mean(),
            "t_stat": t_stat, "p_value": p_val,
        })
    summary = pd.DataFrame(rows)

    # Grouped bars, same platform colors as every other figure in this file.
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    cats = ["work", "personal", "coursework"]
    x = np.arange(len(cats))
    width = 0.34
    for i, (label, color, key) in enumerate(
        [("Claude.ai", C_CLAUDE, "claude_pct"), ("1P API", C_API, "api_pct")]
    ):
        vals = summary[key].to_numpy()
        bars = ax.bar(x + (i - 0.5) * (width + 0.02), vals, width,
                      label=label, color=color, edgecolor="#fcfcfb", linewidth=2)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 1.0, f"{v:.1f}%",
                    ha="center", va="bottom", fontsize=9, color=C_INK)
    ax.set_xticks(x)
    ax.set_xticklabels(["Work", "Personal", "Coursework"])
    ax.set_ylim(0, max(summary[["claude_pct", "api_pct"]].max()) * 1.25)
    w9_style_axes(ax, ylabel="Share of conversations (%)",
                  title="What the two platforms are used for, Feb 2026")
    ax.legend(frameon=False, fontsize=9, labelcolor=C_MUTED, loc="upper right")
    fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_use_case.png"),
                bbox_inches="tight", dpi=200)
    plt.close(fig)

    return summary


# -----------------------------------------------------------------------------
# PART 2 - human_only_ability: could the user have done it without Claude?
# -----------------------------------------------------------------------------

def w11_part2_ability(panel):
    print(f"\n{'=' * 72}")
    print("PART 2  human_only_ability: could the user have done it alone?")
    print(f"{'=' * 72}")

    rows = []
    print(f"\n    {'answer':<16}{'Claude.ai':>11}{'1P API':>10}{'diff':>11}{'p':>12}")
    for label, col in [("yes", "human_only_yes_pct"), ("no", "human_only_no_pct")]:
        a_vals = panel.loc[panel["api"] == 1, col].to_numpy()
        c_vals = panel.loc[panel["api"] == 0, col].to_numpy()
        t_stat, p_val = stats.ttest_rel(a_vals, c_vals)
        print(f"    {label:<16}{c_vals.mean():>10.1f}%{a_vals.mean():>9.1f}%"
              f"{a_vals.mean() - c_vals.mean():>+10.1f}pp{p_val:>12.2e}")
        rows.append({"answer": label, "claude_pct": c_vals.mean(),
                     "api_pct": a_vals.mean(),
                     "diff_pp": a_vals.mean() - c_vals.mean(),
                     "t_stat": t_stat, "p_value": p_val})
    summary = pd.DataFrame(rows)

    # Does the automation gap close for tasks people could NOT do alone?
    # Bin tasks by their human_only "yes" share and plot mean automation.
    edges = [0, 80, 85, 90, 95, 98, 100.01]
    names = ["<80", "80–85", "85–90", "90–95", "95–98", "98–100"]
    binned = panel.copy()
    binned["bin"] = pd.cut(binned["human_only_yes_pct"], edges, right=False,
                           labels=names)
    grid = binned.groupby(["bin", "platform"], observed=True).agg(
        n=("task", "size"), automation=("automation_pct", "mean")
    ).reset_index()

    print("\n  Mean automation % by how often the user could have done it alone")
    print(grid.pivot(index="bin", columns="platform", values="automation")
          .round(1).to_string())

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    x = np.arange(len(names))
    for platform, color in [("Claude.ai", C_CLAUDE), ("1P API", C_API)]:
        sub = grid[grid["platform"] == platform].set_index("bin").reindex(names)
        ax.plot(x, sub["automation"], color=color, linewidth=2, marker="o",
                markersize=8, markeredgecolor="#fcfcfb", markeredgewidth=2,
                label=platform)
    # Label the ends only, so the line stays readable.
    for platform, color in [("Claude.ai", C_CLAUDE), ("1P API", C_API)]:
        sub = grid[grid["platform"] == platform].set_index("bin").reindex(names)
        ax.text(x[-1] + 0.12, sub["automation"].iloc[-1],
                f"{sub['automation'].iloc[-1]:.0f}%", color=C_INK,
                fontsize=9, va="center")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_xlim(-0.4, len(names) - 0.2)
    ax.set_ylim(0, 100)
    w9_style_axes(
        ax,
        xlabel="Share of the task's conversations the user could have done alone (%)",
        ylabel="Automation share (%)",
        title="The gap does not close at any ability level",
    )
    ax.legend(frameon=False, fontsize=9, labelcolor=C_MUTED, loc="center right")
    fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_human_only_ability.png"),
                bbox_inches="tight", dpi=200)
    plt.close(fig)

    return summary, grid


# -----------------------------------------------------------------------------
# PART 3 - does the api coefficient survive these controls?
# -----------------------------------------------------------------------------

def w11_part3_controls(panel):
    print(f"\n{'=' * 72}")
    print("PART 3  Does the api coefficient survive work_pct and ability?")
    print(f"{'=' * 72}")

    groups = pd.factorize(panel["task"])[0]

    def fit(formula):
        return smf.ols(formula, data=panel).fit(
            cov_type="cluster", cov_kwds={"groups": groups}
        )

    base = "automation_pct ~ api + log_volume + unclassified_pct"
    models = {
        "(1) Week 9 model": fit(base),
        "(2) + work_pct": fit(base + " + work_pct"),
        "(3) + ability": fit(base + " + human_only_yes_pct"),
        "(4) + both": fit(base + " + work_pct + human_only_yes_pct"),
    }

    rows = ["api", "work_pct", "human_only_yes_pct", "log_volume",
            "unclassified_pct", "Intercept"]
    table = pd.DataFrame(index=rows + ["R-squared", "N"])
    for name, m in models.items():
        col = {v: (f"{m.params[v]:.3f}{w9_stars(m.pvalues[v])}"
                   if v in m.params.index else "") for v in rows}
        col["R-squared"] = f"{m.rsquared:.3f}"
        col["N"] = f"{int(m.nobs)}"
        table[name] = pd.Series(col)

    print("\n  (clustered SE by task; *** p<0.01, ** p<0.05, * p<0.1)")
    print(table.to_string())

    # Visual version: the api coefficient with 95% CI in each specification.
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    names = list(models)
    y = np.arange(len(names))[::-1]
    coefs = np.array([models[n].params["api"] for n in names])
    errs = np.array([1.96 * models[n].bse["api"] for n in names])
    ax.errorbar(coefs, y, xerr=errs, fmt="o", color=C_API, markersize=9,
                markeredgecolor="#fcfcfb", markeredgewidth=2,
                ecolor=C_INK, elinewidth=1.4, capsize=4)
    for yi, v in zip(y, coefs):
        ax.text(v, yi + 0.22, f"{v:.1f}", ha="center", fontsize=9, color=C_INK)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlim(0, max(coefs + errs) * 1.15)
    ax.set_ylim(-0.6, len(names) - 0.4)
    w9_style_axes(ax, xlabel="api coefficient (percentage points)",
                  title="The gap is not explained by task purpose or difficulty")
    ax.xaxis.grid(True, color=C_GRID, linewidth=0.8)
    ax.yaxis.grid(False)
    fig.savefig(os.path.join(W9_FIG_DIR, "feb2026_api_coefficient_controls.png"),
                bbox_inches="tight", dpi=200)
    plt.close(fig)

    return table


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

def week11_main():
    print("\nWeek 11: loading the February 2026 release")
    frames = w9_load_release(W11_PERIOD)

    panel = w11_build_panel(frames)
    print(f"\n  panel: {len(panel):,} observations "
          f"({panel['task'].nunique():,} tasks x 2 platforms)")
    print(panel.groupby("platform")[
        ["automation_pct", "work_pct", "personal_pct", "human_only_yes_pct"]
    ].mean().round(2).to_string())

    use_case = w11_part1_use_case(frames, panel)
    ability, ability_grid = w11_part2_ability(panel)
    controls = w11_part3_controls(panel)

    use_case.to_csv(os.path.join(W9_TAB_DIR, "week11_use_case.csv"), index=False)
    ability.to_csv(os.path.join(W9_TAB_DIR, "week11_human_only_ability.csv"), index=False)
    ability_grid.to_csv(os.path.join(W9_TAB_DIR, "week11_ability_bins.csv"), index=False)
    controls.to_csv(os.path.join(W9_TAB_DIR, "week11_controls_regression.csv"))

    print(f"\n  figures -> {W9_FIG_DIR}/feb2026_use_case.png, "
          f"feb2026_human_only_ability.png, feb2026_api_coefficient_controls.png")
    print(f"  tables  -> {W9_TAB_DIR}/week11_*.csv")


week11_main()
