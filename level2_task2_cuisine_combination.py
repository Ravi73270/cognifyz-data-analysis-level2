import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# ── 1. Load dataset ──────────────────────────────────────────────
df = pd.read_csv("Dataset_.csv")
total_restaurants = len(df)
print(f"Total Restaurants : {total_restaurants}\n")

# ── 2. Build cuisine combinations (order-independent) ────────────
combo_counter = Counter()
for entry in df["Cuisines"].dropna():
    combo = tuple(sorted(c.strip() for c in entry.split(",")))
    combo_counter[combo] += 1

# Separate single-cuisine vs multi-cuisine combos
multi_combo_counter = {k: v for k, v in combo_counter.items() if len(k) > 1}

# ── 3. Most common combinations (any size) ───────────────────────
top10_overall = combo_counter.most_common(10)

print("=" * 60)
print("   TOP 10 MOST COMMON CUISINE COMBINATIONS (overall)")
print("=" * 60)
for combo, count in top10_overall:
    pct = (count / total_restaurants) * 100
    label = " + ".join(combo)
    print(f"  {label:<35} | {count:>5} ({pct:.2f}%)")
print("=" * 60)

# ── 4. Most common MULTI-cuisine combinations ────────────────────
top10_multi = sorted(multi_combo_counter.items(), key=lambda x: x[1], reverse=True)[:10]

print("\n" + "=" * 60)
print("   TOP 10 MULTI-CUISINE COMBINATIONS")
print("=" * 60)
for combo, count in top10_multi:
    pct = (count / total_restaurants) * 100
    label = " + ".join(combo)
    print(f"  {label:<35} | {count:>5} ({pct:.2f}%)")
print("=" * 60)

# ── 5. Average rating per top combination ─────────────────────────
df["Cuisine Combo"] = df["Cuisines"].dropna().apply(
    lambda x: tuple(sorted(c.strip() for c in x.split(",")))
)

rated_df = df[df["Aggregate rating"] > 0]
combo_avg_rating = rated_df.groupby("Cuisine Combo")["Aggregate rating"].mean()

combo_rating_table = []
for combo, count in top10_multi:
    avg_r = combo_avg_rating.get(combo, float("nan"))
    combo_rating_table.append((combo, count, avg_r))

print("\n" + "=" * 60)
print("   AVG RATING FOR TOP MULTI-CUISINE COMBINATIONS")
print("=" * 60)
for combo, count, avg_r in combo_rating_table:
    label = " + ".join(combo)
    print(f"  {label:<35} | Count: {count:<5} | Avg Rating: {avg_r:.2f}")
print("=" * 60)

best_combo = max(combo_rating_table, key=lambda x: x[2])
print(f"\n→ Highest-rated popular combo: {' + '.join(best_combo[0])} "
      f"(Avg Rating: {best_combo[2]:.2f})\n")

# ── 6. Visualization ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Level 2 – Task 2: Cuisine Combination Analysis", fontsize=14, fontweight="bold", y=1.02)

# Chart 1: Top 10 multi-cuisine combos by count
labels = [" + ".join(c) for c, _ in top10_multi]
counts = [n for _, n in top10_multi]
colors = plt.cm.viridis([i / 10 for i in range(len(labels))])

bars = axes[0].barh(labels[::-1], counts[::-1], color=colors[::-1], edgecolor="white")
axes[0].set_title("Top 10 Multi-Cuisine Combinations", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Number of Restaurants", fontsize=10)
axes[0].spines[["top", "right"]].set_visible(False)
for bar in bars:
    axes[0].text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                 str(int(bar.get_width())), va="center", fontsize=9, fontweight="bold")

# Chart 2: Avg rating per top combo
combo_labels = [" + ".join(c) for c, _, _ in combo_rating_table]
ratings = [r for _, _, r in combo_rating_table]
colors2 = ["#e9c46a" if c == best_combo[0] else "#2a9d8f" for c, _, _ in combo_rating_table]

bars2 = axes[1].barh(combo_labels[::-1], ratings[::-1], color=colors2[::-1], edgecolor="white")
axes[1].set_title("Avg Rating per Multi-Cuisine Combo", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Average Rating ⭐", fontsize=10)
axes[1].set_xlim(0, 5)
axes[1].spines[["top", "right"]].set_visible(False)
for bar in bars2:
    axes[1].text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                 f"{bar.get_width():.2f}", va="center", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig("level2_task2_cuisine_combination.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved → level2_task2_cuisine_combination.png")
