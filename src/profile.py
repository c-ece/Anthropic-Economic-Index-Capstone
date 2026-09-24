import pandas as pd
import matplotlib.pyplot as plt

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