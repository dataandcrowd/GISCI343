# Week 4 Lecture: Data Visualisation + Geospatial Intro

## Today's Structure (2 hours total)

**Hour 1: Data Visualisation with Python** (60 mins)
- Why visualisation matters
- Matplotlib foundations  
- Seaborn for statistical graphics
- Best practices for urban data

**Hour 2: Guest Lecture - Transport + Geospatial Intro** (60 mins)
- Guest: Transport expert
- Real-world applications
- Introduction to geospatial concepts

---

# Part 1: Why Visualisation Matters

---

## Anscombe's Quartet: The Classic Example

**Four datasets, identical statistics:**

```python
# All four have:
mean_x = 9.0
mean_y = 7.5
std_x = 3.3
std_y = 2.0
correlation = 0.816
```

**But completely different patterns!**

---

![Anscombe's Quartet]

**The lesson**: Always visualise your data!

Statistics alone don't show the full picture.

---

## Urban Analytics Example

**Pedestrian count statistics:**
```
Mean: 234 pedestrians/hour
Std: 145
Min: 12
Max: 678
```

**But we need to ask:**
- When are the peaks?
- Which days are busiest?
- Are there weekly patterns?
- Any anomalies?

**Answer**: Visualise!

---

## The Python Visualisation Stack

```
┌──────────────────────────────┐
│  Your Plots                   │
├──────────────────────────────┤
│  seaborn (statistical)        │ ← High-level
├──────────────────────────────┤
│  matplotlib (foundation)      │ ← Low-level
├──────────────────────────────┤
│  pandas plotting (quick)      │ ← Built-in
└──────────────────────────────┘
```

**We'll learn all three layers**

---

# Matplotlib: The Foundation

---

## Anatomy of a Matplotlib Figure

```
┌─────────────────────────────┐
│ Figure                       │ ← Container
│  ┌───────────────────────┐  │
│  │ Axes (plot area)       │  │ ← Where you plot
│  │                        │  │
│  │  Title                 │  │
│  │  ┌──────────────┐     │  │
│  │  │ Plot         │     │  │
│  │  │              │     │  │
│  │  └──────────────┘     │  │
│  │  X-axis  Y-axis       │  │
│  │  Legend               │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

---

## Your First Plot

```python
import matplotlib.pyplot as plt

# Data
hours = [0, 6, 12, 18, 24]
pedestrians = [45, 123, 234, 567, 89]

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(hours, pedestrians, marker='o')
plt.xlabel('Hour of Day')
plt.ylabel('Pedestrian Count')
plt.title('Pedestrian Traffic Pattern')
plt.grid(True, alpha=0.3)
plt.show()
```

---

![Line plot example]

**Key elements:**
- `figsize`: Control size
- `marker='o'`: Add points
- `grid`: Show gridlines
- `alpha`: Transparency

---

## Plot Types: Choose Wisely

**Line plots**: Time series, trends
```python
plt.plot(dates, counts)
```

**Scatter plots**: Relationships, correlations
```python
plt.scatter(income, walkability)
```

**Bar charts**: Categorical comparisons
```python
plt.bar(suburbs, avg_counts)
```

**Histograms**: Distributions
```python
plt.hist(pedestrian_counts, bins=30)
```

---

## Customising Plots

```python
# Create figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Plot with custom styling
ax.plot(hours, counts, 
        color='steelblue',       # Colour
        linewidth=2.5,           # Line thickness
        marker='o',              # Point markers
        markersize=8,            # Marker size
        label='Weekday')         # Legend label

# Customise
ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
ax.set_ylabel('Pedestrian Count', fontsize=12, fontweight='bold')
ax.set_title('Auckland CBD Pedestrian Patterns', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', frameon=True)
ax.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Multiple Plots: Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Top left: Line plot
axes[0, 0].plot(hours, weekday_counts)
axes[0, 0].set_title('Weekday Pattern')

# Top right: Line plot
axes[0, 1].plot(hours, weekend_counts, color='orange')
axes[0, 1].set_title('Weekend Pattern')

# Bottom left: Bar chart
axes[1, 0].bar(days, daily_avg)
axes[1, 0].set_title('Average by Day')

# Bottom right: Histogram
axes[1, 1].hist(all_counts, bins=30, color='green', alpha=0.7)
axes[1, 1].set_title('Distribution')

plt.tight_layout()
plt.show()
```

---

![Subplots example - 2x2 grid]

**Use subplots for:**
- Comparing patterns
- Multiple views of same data
- Dashboard-style layouts

---

# Seaborn: Statistical Graphics

---

## Why Seaborn?

**Matplotlib**:
- Lots of control
- Verbose code
- Manual styling

**Seaborn**:
- Less code
- Beautiful defaults
- Statistical focus
- Integrated with pandas

```python
import seaborn as sns
sns.set_theme()  # Better defaults
```

---

## Distribution Plots

```python
import seaborn as sns
import pandas as pd

# Load data
df = pd.read_csv('pedestrian_counts.csv')

# Histogram with KDE
sns.histplot(data=df, x='count', kde=True, bins=50)
plt.title('Pedestrian Count Distribution')
plt.show()
```

![Histogram with KDE curve]

**KDE** (Kernel Density Estimate) = smoothed distribution

---

## Box Plots: Compare Groups

```python
# Compare across days
sns.boxplot(data=df, x='day_of_week', y='count')
plt.title('Pedestrian Counts by Day')
plt.xticks(rotation=45)
plt.show()
```

![Box plot comparing days]

**Quickly see:**
- Median (middle line)
- Quartiles (box)
- Outliers (points)

---

## Violin Plots: Richer Distribution View

```python
# Like box plot but shows full distribution
sns.violinplot(data=df, x='day_of_week', y='count',
               palette='muted')
plt.title('Pedestrian Distribution by Day')
plt.show()
```

![Violin plot]

**Shows** shape of distribution, not just summary stats

---

## Relationships: Scatter with Regression

```python
# Relationship between two variables
sns.scatterplot(data=sa2_data, x='median_income', y='walkability',
                hue='area_type', size='population')
sns.regplot(data=sa2_data, x='median_income', y='walkability',
            scatter=False, color='red')
plt.title('Income vs Walkability in Auckland SA2')
plt.show()
```

![Scatter with regression line]

---

## Heatmaps: Hourly × Daily Patterns

```python
# Create pivot table
pivot = df.pivot_table(values='count',
                       index='hour',
                       columns='day_of_week',
                       aggfunc='mean')

# Heatmap
sns.heatmap(pivot, cmap='YlOrRd', annot=True, fmt='.0f',
            cbar_kws={'label': 'Pedestrian Count'})
plt.title('Pedestrian Heatmap: Hour × Day')
plt.tight_layout()
plt.show()
```

---

![Heatmap showing hour vs day patterns]

**Instantly see:**
- Peak hours
- Busiest days
- Quiet periods
- Pattern anomalies

---

## Pair Plots: Multiple Relationships

```python
# Multiple variables at once
sns.pairplot(sa2_data[['population', 'density', 
                       'median_income', 'walkability']],
             diag_kind='kde')
plt.show()
```

![Pair plot matrix]

**Great for**:
- Exploratory analysis
- Finding correlations
- Identifying patterns

---

# Best Practices for Urban Data

---

## Choosing Colours Wisely

**For sequential data** (low → high):
```python
# Good: Single colour gradient
cmap='YlOrRd'  # Yellow → Orange → Red
cmap='Blues'   # Light → Dark Blue
```

**For diverging data** (negative ↔ positive):
```python
# Good: Two-colour divergence
cmap='RdBu'    # Red ↔ Blue
cmap='PiYG'    # Pink ↔ Green
```

**For categories**:
```python
# Good: Distinct colours
palette='Set2'
palette='tab10'
```

---

## Accessibility Considerations

```python
# Colorblind-friendly palettes
sns.color_palette('colorblind')

# Add patterns for print
hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']

# Always use labels + colour
ax.bar(x, y, label='Weekday', color='steelblue')
ax.bar(x, y2, label='Weekend', color='coral')
ax.legend()  # Labels help everyone!
```

---

## Design Principles

**1. Clear titles and labels**
```python
plt.title('Pedestrian Counts: Auckland CBD, 2024',
          fontsize=14, fontweight='bold')
plt.xlabel('Hour of Day (24h)', fontsize=12)
plt.ylabel('Average Count (pedestrians/hour)', fontsize=12)
```

**2. Remove chart junk**
```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

**3. Add context**
```python
ax.text(0.99, 0.01, 'Source: Auckland Transport, 2024',
        transform=ax.transAxes, ha='right', fontsize=8)
```

---

## Real Example: Auckland Weather Analysis

```python
# Load data
weather = pd.read_csv('auckland_weather_2024.csv',
                      parse_dates=['date'])

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Temperature over time
axes[0, 0].plot(weather['date'], weather['temp_max'], 
                label='Max', color='red')
axes[0, 0].plot(weather['date'], weather['temp_min'], 
                label='Min', color='blue')
axes[0, 0].set_title('Temperature Range 2024')
axes[0, 0].legend()

# 2. Rainfall distribution
axes[0, 1].hist(weather['rainfall'], bins=30, 
                color='steelblue', edgecolor='black')
axes[0, 1].set_title('Rainfall Distribution')
axes[0, 1].set_xlabel('Rainfall (mm)')

# 3. Monthly average temp
monthly_avg = weather.groupby(weather['date'].dt.month)['temp_max'].mean()
axes[1, 0].bar(range(1, 13), monthly_avg, color='coral')
axes[1, 0].set_title('Average Max Temperature by Month')
axes[1, 0].set_xlabel('Month')

# 4. Scatter: Temp vs Humidity
axes[1, 1].scatter(weather['temp_max'], weather['humidity'],
                   alpha=0.5, c=weather['rainfall'],
                   cmap='Blues')
axes[1, 1].set_title('Temperature vs Humidity')
axes[1, 1].set_xlabel('Max Temperature (°C)')
axes[1, 1].set_ylabel('Humidity (%)')

plt.tight_layout()
plt.savefig('weather_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Saving Plots

```python
# Save as PNG (for web, presentations)
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

# Save as PDF (for publications)
plt.savefig('plot.pdf', bbox_inches='tight')

# Save as SVG (vector, for editing)
plt.savefig('plot.svg', bbox_inches='tight')

# Multiple formats
for fmt in ['png', 'pdf', 'svg']:
    plt.savefig(f'plot.{fmt}', dpi=300, bbox_inches='tight')
```

**Tip**: Always use `bbox_inches='tight'` to avoid cut-off labels!

---

## Assignment 1 Context

**Next week you submit Assignment 1: Pedestrian Blog Post**

**Required visualisations:**
1. Time series (hourly/daily patterns)
2. Comparison plots (locations, days)
3. Statistical distributions
4. At least one Seaborn plot

**Use what you learned today!**

---

# Break (5 minutes)

---

# Hour 2: Guest Lecture + Geospatial Intro

---

## Transition to Guest Lecture

**Guest speaker**: [Transport Expert Name]

**Topics:**
- Transport analytics in practice
- Real-world data challenges
- Career pathways
- Q&A

**After guest lecture**: Geospatial concepts introduction

---

## [Guest Lecture: 50 minutes]

**Student instructions:**
- Take notes
- Prepare questions
- Think about connections to your assignments

---

## Geospatial Concepts: Quick Introduction

**After guest lecture, brief intro to Week 5 topics:**

---

## What is Geospatial Data?

**Regular data:**
```python
{'name': 'Queen Street', 'count': 567}
```

**Geospatial data:**
```python
{
    'name': 'Queen Street', 
    'count': 567,
    'geometry': POINT(174.7633, -36.8485)  # ← Location!
}
```

**Location enables spatial analysis**

---

## Coordinate Reference Systems (CRS)

**Two main types:**

**Geographic** (latitude/longitude):
- EPSG:4326 (WGS 84) - GPS coordinates
- Degrees, not metres
- Good for: Web maps, GPS data

**Projected** (metres):
- EPSG:2193 (NZTM) - New Zealand
- Metres, not degrees
- Good for: Distance, area calculations

**Next week**: Deep dive into CRS

---

## Geometry Types Preview

```python
from shapely.geometry import Point, LineString, Polygon

# Point (e.g., sensor location)
sensor = Point(174.7633, -36.8485)

# LineString (e.g., street)
street = LineString([(174.76, -36.84), (174.77, -36.85)])

# Polygon (e.g., SA2 boundary)
zone = Polygon([
    (174.76, -36.84),
    (174.77, -36.84),
    (174.77, -36.85),
    (174.76, -36.85)
])
```

---

## GeoPandas: Spatial DataFrames

```python
import geopandas as gpd

# Read geospatial file
sa2 = gpd.read_file('auckland_sa2.gpkg')

# Just like pandas, but with geometry!
print(sa2.head())
```

```
  SA2_code    SA2_name  population                     geometry
0      001         CBD       45678  POLYGON ((174.76 -36.84, ...))
1      002   Newmarket       32145  POLYGON ((174.78 -36.87, ...))
```

**Next week**: Hands-on with GeoPandas!

---

## Preview: What You'll Do Next Week

**Week 5 - Geospatial Operations:**
1. Load Auckland SA2 boundaries
2. Perform spatial joins
3. Calculate areas and distances
4. Create choropleth maps
5. Spatial analysis for Assignment 1

**Plus**: Creating reusable functions

---

## Lab This Week

**Focus on Assignment 1:**

1. Finalise pedestrian data analysis
2. Create all required visualisations
3. Start writing blog post
4. Review Quarto formatting
5. Prepare for submission next week

**Assignment 1 due**: End of next week!

---

## Key Takeaways

### Visualisation

1. ✅ **Always visualise** - statistics hide patterns
2. ✅ **Choose plot type wisely** - match data to viz
3. ✅ **Seaborn for quick statistical graphics**
4. ✅ **Design matters** - clear, accessible, beautiful

### Coming Next Week

5. ✅ **Geospatial = location + data**
6. ✅ **CRS matters for calculations**
7. ✅ **GeoPandas = pandas + geometry**

---

## Assignment 1 Reminder

**Due**: End of Week 5 (in lab next Wednesday)

**Checklist:**
- [ ] Data cleaned and processed
- [ ] All required plots created
- [ ] Blog post written with narrative
- [ ] Quarto formatted
- [ ] GitHub Pages published
- [ ] Submitted to Canvas

**Get help in lab if stuck!**

---

## Questions?

**Before next week's lab:**
- Finish Assignment 1
- Read Week 5 materials on GeoPandas
- Install/test geopandas in Colab

**Next lecture**: Geospatial operations deep dive!

---

## Resources

**Visualisation:**
- Matplotlib gallery: matplotlib.org/gallery
- Seaborn gallery: seaborn.pydata.org/examples
- Fundamentals of Data Visualization (Claus Wilke) - free online

**Assignment 1:**
- Example blog posts on Canvas
- Quarto documentation
- GitHub Pages guide

**See you in lab!**
