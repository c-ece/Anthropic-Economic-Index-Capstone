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
