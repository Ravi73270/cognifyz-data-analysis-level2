import pandas as pd
import matplotlib.pyplot as plt

# ── 1. Load dataset ──────────────────────────────────────────────
df = pd.read_csv("Dataset_.csv")
total_restaurants = len(df)
print(f"Total Restaurants : {total_restaurants}\n")

# ── 2. Basic geographic stats ────────────────────────────────────
print("=" * 50)
print("        GEOGRAPHIC COVERAGE SUMMARY")
print("=" * 50)
print(f"  Longitude range : {df['Longitude'].min():.2f} to {df['Longitude'].max():.2f}")
print(f"  Latitude range  : {df['Latitude'].min():.2f} to {df['Latitude'].max():.2f}")
print(f"  Total countries : {df['Country Code'].nunique()}")
print(f"  Total cities    : {df['City'].nunique()}")
print("=" * 50)

# ── 3. Identify clusters: top 5 cities by restaurant density ────
top_cities = df["City"].value_counts().head(5)
print("\nTop 5 City Clusters (by restaurant count):")
for city, count in top_cities.items():
    pct = (count / total_restaurants) * 100
    print(f"  {city:<20} | {count:>5} restaurants ({pct:.2f}%)")

# ── 4. Visualization ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Level 2 – Task 3: Geographic Analysis of Restaurant Locations", fontsize=14, fontweight="bold", y=1.02)

# Chart 1: World-scale scatter (all restaurants)
axes[0].scatter(df["Longitude"], df["Latitude"], s=4, alpha=0.4, color="#2a78d6")
axes[0].set_title("Global Distribution of Restaurants", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Longitude", fontsize=10)
axes[0].set_ylabel("Latitude", fontsize=10)
axes[0].spines[["top", "right"]].set_visible(False)
axes[0].grid(alpha=0.2)

# Chart 2: Zoomed-in cluster scatter, colored by top 5 cities
top5_names = top_cities.index.tolist()
colors_map = {city: color for city, color in zip(top5_names,
              ["#e63946", "#2a9d8f", "#f4a261", "#9b5de5", "#118ab2"])}

other_df = df[~df["City"].isin(top5_names)]
axes[1].scatter(other_df["Longitude"], other_df["Latitude"], s=4, alpha=0.25,
                color="lightgray", label="Other cities")

for city in top5_names:
    city_df = df[df["City"] == city]
    axes[1].scatter(city_df["Longitude"], city_df["Latitude"], s=6, alpha=0.6,
                     color=colors_map[city], label=city)

axes[1].set_title("Restaurant Clusters — Top 5 Cities Highlighted", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Longitude", fontsize=10)
axes[1].set_ylabel("Latitude", fontsize=10)
axes[1].spines[["top", "right"]].set_visible(False)
axes[1].grid(alpha=0.2)
axes[1].legend(fontsize=8, loc="lower left", markerscale=2)

plt.tight_layout()
plt.savefig("level2_task3_geographic_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved → level2_task3_geographic_analysis.png")

# ── 5. Key insight ────────────────────────────────────────────────
print("\n" + "=" * 50)
print("  KEY INSIGHT")
print("=" * 50)
print(f"  Restaurants are heavily clustered around the")
print(f"  Delhi-NCR region (New Delhi, Gurgaon, Noida,")
print(f"  Faridabad), which together account for")
ncr_cities = ["New Delhi", "Gurgaon", "Noida", "Faridabad"]
ncr_count = df[df["City"].isin(ncr_cities)].shape[0]
ncr_pct = (ncr_count / total_restaurants) * 100
print(f"  {ncr_count} restaurants ({ncr_pct:.2f}% of the dataset).")
print("=" * 50)
