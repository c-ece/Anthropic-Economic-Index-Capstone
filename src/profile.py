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