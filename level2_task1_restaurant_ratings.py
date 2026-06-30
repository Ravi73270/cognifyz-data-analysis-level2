import pandas as pd
import matplotlib.pyplot as plt

# ── 1. Load dataset ──────────────────────────────────────────────
df = pd.read_csv("Dataset_.csv")
total_restaurants = len(df)
print(f"Total Restaurants : {total_restaurants}\n")

# ── 2. Rating distribution ───────────────────────────────────────
# 0.0 means "Not rated" — handle separately
not_rated = (df["Aggregate rating"] == 0).sum()
rated_df = df[df["Aggregate rating"] > 0].copy()

# Bin ratings into meaningful ranges
bins = [0, 1, 2, 3, 3.5, 4, 4.5, 5]
labels = ["0-1", "1-2", "2-3", "3-3.5", "3.5-4", "4-4.5", "4.5-5"]
rated_df["Rating Range"] = pd.cut(rated_df["Aggregate rating"], bins=bins, labels=labels, include_lowest=True)

rating_dist = rated_df["Rating Range"].value_counts().sort_index()
most_common_range = rating_dist.idxmax()
most_common_count = rating_dist.max()

print("=" * 50)
print("       AGGREGATE RATING DISTRIBUTION")
print("=" * 50)
print(f"  Not Rated (0.0)        : {not_rated} restaurants")
for rng, count in rating_dist.items():
    pct = (count / total_restaurants) * 100
    print(f"  Rating {rng:<10}     : {count:>5} restaurants ({pct:.2f}%)")
print("=" * 50)
print(f"\n→ Most common rating range: {most_common_range} "
      f"({most_common_count} restaurants)\n")

# ── 3. Average votes ──────────────────────────────────────────────
avg_votes = df["Votes"].mean()
median_votes = df["Votes"].median()

print("=" * 50)
print("              VOTES ANALYSIS")
print("=" * 50)
print(f"  Average votes per restaurant : {avg_votes:.2f}")
print(f"  Median votes per restaurant  : {median_votes:.2f}")
print(f"  Max votes (most voted)       : {df['Votes'].max()}")
print(f"  Min votes                    : {df['Votes'].min()}")
print("=" * 50)

# ── 4. Visualization ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Level 2 – Task 1: Restaurant Ratings & Votes Analysis", fontsize=14, fontweight="bold", y=1.02)

# Chart 1: Rating distribution bar chart
colors = plt.cm.RdYlGn([i / (len(rating_dist) - 1) for i in range(len(rating_dist))])
bars = axes[0].bar(rating_dist.index.astype(str), rating_dist.values, color=colors, edgecolor="white")
axes[0].set_title("Aggregate Rating Distribution", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Rating Range", fontsize=10)
axes[0].set_ylabel("Number of Restaurants", fontsize=10)
axes[0].spines[["top", "right"]].set_visible(False)
for bar in bars:
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                 str(int(bar.get_height())), ha="center", va="bottom",
                 fontsize=9, fontweight="bold")

# Highlight the most common range
most_common_idx = list(rating_dist.index.astype(str)).index(str(most_common_range))
bars[most_common_idx].set_edgecolor("#e63946")
bars[most_common_idx].set_linewidth(2.5)

# Chart 2: Votes distribution (log scale histogram)
axes[1].hist(df["Votes"], bins=50, color="#2a78d6", edgecolor="white")
axes[1].axvline(avg_votes, color="#e63946", linestyle="--", linewidth=2,
                 label=f"Mean = {avg_votes:.0f}")
axes[1].axvline(median_votes, color="#f4a261", linestyle="--", linewidth=2,
                 label=f"Median = {median_votes:.0f}")
axes[1].set_title("Distribution of Votes per Restaurant", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Votes", fontsize=10)
axes[1].set_ylabel("Number of Restaurants", fontsize=10)
axes[1].set_xlim(0, 2000)  # zoom in, since a few outliers go up to 10,934
axes[1].spines[["top", "right"]].set_visible(False)
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.savefig("level2_task1_restaurant_ratings.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved → level2_task1_restaurant_ratings.png")
