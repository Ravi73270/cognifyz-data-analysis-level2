import pandas as pd
import matplotlib.pyplot as plt

# ── 1. Load dataset ──────────────────────────────────────────────
df = pd.read_csv("Dataset_.csv")
total_restaurants = len(df)
total_unique_names = df["Restaurant Name"].nunique()
print(f"Total Restaurants      : {total_restaurants}")
print(f"Total Unique Names     : {total_unique_names}\n")

# ── 2. Identify chains: a name appearing at more than one outlet ─
name_counts = df["Restaurant Name"].value_counts()
chains = name_counts[name_counts > 1]
num_chains = len(chains)
chain_outlets_total = chains.sum()

print("=" * 55)
print("            RESTAURANT CHAIN DETECTION")
print("=" * 55)
print(f"  Restaurant names appearing >1 time (chains) : {num_chains}")
print(f"  Total outlets belonging to chains            : {chain_outlets_total}")
print(f"  % of dataset that is chain outlets            : "
      f"{chain_outlets_total/total_restaurants*100:.2f}%")
print("=" * 55)

# ── 3. Top 15 largest chains by outlet count ──────────────────────
top15_chains = chains.head(15)

print("\nTop 15 Largest Restaurant Chains (by number of outlets):")
for name, count in top15_chains.items():
    print(f"  {name:<22} | {count:>3} outlets")

# ── 4. Analyze ratings & popularity (votes) of chains ─────────────
chain_names = chains.index.tolist()
chain_df = df[df["Restaurant Name"].isin(chain_names)]
rated_chain_df = chain_df[chain_df["Aggregate rating"] > 0]

chain_stats = (
    rated_chain_df.groupby("Restaurant Name")
    .agg(outlets=("Restaurant Name", "count"),
         avg_rating=("Aggregate rating", "mean"),
         total_votes=("Votes", "sum"))
    .round(2)
)

# Restrict to the top 15 chains for a clean comparison
top15_stats = chain_stats.loc[chain_stats.index.intersection(top15_chains.index)]
top15_stats = top15_stats.sort_values("outlets", ascending=False)

print("\n" + "=" * 70)
print("   TOP CHAINS — OUTLETS, AVG RATING & TOTAL VOTES")
print("=" * 70)
for name, row in top15_stats.iterrows():
    print(f"  {name:<22} | Outlets: {int(row['outlets']):>3} | "
          f"Avg Rating: {row['avg_rating']:.2f} | Total Votes: {int(row['total_votes']):>6}")
print("=" * 70)

best_rated_chain = chain_stats["avg_rating"].idxmax()
best_rated_value = chain_stats["avg_rating"].max()
most_voted_chain = chain_stats["total_votes"].idxmax()
most_voted_value = chain_stats["total_votes"].max()

print(f"\n→ Highest-rated chain overall : {best_rated_chain} "
      f"(Avg Rating: {best_rated_value:.2f})")
print(f"→ Most popular chain (by votes): {most_voted_chain} "
      f"(Total Votes: {int(most_voted_value)})\n")

# ── 5. Visualization ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Level 2 – Task 4: Restaurant Chains Analysis", fontsize=14, fontweight="bold", y=1.02)

# Chart 1: Top 15 chains by outlet count
bars = axes[0].barh(top15_chains.index[::-1], top15_chains.values[::-1],
                     color=plt.cm.cool([i / 15 for i in range(15)]), edgecolor="white")
axes[0].set_title("Top 15 Restaurant Chains by Outlet Count", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Number of Outlets", fontsize=10)
axes[0].spines[["top", "right"]].set_visible(False)
for bar in bars:
    axes[0].text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                 str(int(bar.get_width())), va="center", fontsize=8, fontweight="bold")

# Chart 2: Avg rating per top chain
top15_stats_sorted = top15_stats.sort_values("avg_rating")
colors2 = ["#e9c46a" if name == best_rated_chain else "#2a9d8f"
           for name in top15_stats_sorted.index]
bars2 = axes[1].barh(top15_stats_sorted.index, top15_stats_sorted["avg_rating"],
                      color=colors2, edgecolor="white")
axes[1].set_title("Average Rating of Top Chains", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Average Rating", fontsize=10)
axes[1].set_xlim(0, 5)
axes[1].spines[["top", "right"]].set_visible(False)
for bar in bars2:
    axes[1].text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                 f"{bar.get_width():.2f}", va="center", fontsize=8, fontweight="bold")

plt.tight_layout()
plt.savefig("level2_task4_restaurant_chains.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved → level2_task4_restaurant_chains.png")
