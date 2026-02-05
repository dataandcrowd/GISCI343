# Week 1 Lecture: Introduction to Geospatial Python Programming

## Course Information

**Instructor**: Hyesop Shin
**Email**: h.shin@auckland.ac.nz
**Lectures**: Tuesdays 14:00-16:00
**Labs**: Wednesdays (multiple sessions)

---

## Today's Journey

**Part 1: Why This Course Matters** (30 mins)
- Urban challenges and geospatial data
- What you'll build by Week 12
- Course structure and assessment

**Part 2: Python and Jupyter Setup** (45 mins)
- Why Python for GIS?
- Google Colab walkthrough
- Your first notebook

**Part 3: Programming Fundamentals** (30 mins)
- Variables and data types
- Your first geospatial hello world

**Part 4: Week 1 Lab Preview** (15 mins)

---

# Part 1: Why Geospatial Programming?

---

## The Auckland Challenge

![Auckland aerial view]

**Questions we can't answer with GIS software alone:**
- Where should we put 1000 new e-scooter parking zones?
- Which SA2 areas have the worst accessibility to green spaces?
- How do pedestrian flows change hour by hour?
- What if we implemented congestion charging?

**Answer**: We need to write code.

---

## From Questions to Code

**Traditional GIS** (QGIS, ArcGIS):
- Click → Select → Buffer → Join → Export
- Great for one-off analysis
- Hard to reproduce
- Can't handle millions of trips automatically

**Programming** (Python):
```python
for zone in auckland_sa2:
    accessibility = calculate_15min_amenities(zone)
    if accessibility < threshold:
        flag_for_intervention(zone)
```

**Result**: Reproducible, scalable, shareable

---

## What You'll Build

### Week 4: Your First Map
```python
import geopandas as gpd
sa2 = gpd.read_file('auckland_sa2.gpkg')
sa2.plot(column='population', legend=True)
```
![Choropleth map of Auckland]

---

### Week 8: Interactive Dashboard
![Shiny dashboard screenshot]

A web app where users can:
- Filter by date and location
- See maps update in real-time
- Download processed data

**All browser-based, no installation required**

---

### Week 12: Published Python Package

```bash
pip install your-urban-toolkit
```

```python
from your_package import calculate_walkability
score = calculate_walkability(streets, amenities)
```

**On PyPI, installable by anyone in the world!**

---

## Course Structure

### Three Main Parts

**Part 1: Python Fundamentals** (Weeks 1-2)
- Programming basics
- Data structures
- Control flow

**Part 2: Geospatial Analysis** (Weeks 3-5)
- Pandas and DataFrames
- GeoPandas and spatial operations
- Creating reusable functions

---

**Part 3: Interactive Dashboards** (Weeks 6-8)
- Shiny for Python
- Network analysis
- Web deployment

**Part 4: Package Development** (Weeks 9-12)
- Building Python packages
- Testing and documentation
- Publishing to PyPI

---

## Assessment Overview

| Assessment | Weight | Due Date |
|------------|--------|----------|
| **Assignment 1**: Pedestrian Blog Post | 20% | Week 4 |
| **Assignment 2**: Shiny Dashboard | 35% | Week 8 |
| **Assignment 3**: Python Package | 30% | Week 12 |
| **Poster Showcase** | 10% | Week 12 |
| **Weekly Labs** | 5% | Ongoing |

**Total**: 100%

---

## Assignment 1 Preview: Pedestrian Analysis

**Task**: Analyse Auckland pedestrian count data and write a blog post

**You'll learn:**
- Loading and cleaning real sensor data
- Temporal analysis (hourly, daily patterns)
- Creating visualizations
- Publishing with Quarto and GitHub Pages

**Due**: End of Week 4

---

## Assignment 2 Preview: Interactive Dashboard

**Task**: Build a Shiny app analyzing urban data

**You'll learn:**
- Reactive programming
- Interactive maps
- Network analysis
- Web deployment with shinylive

**Due**: Week 8 (Assignment 2 worth 35%)

---

## Assignment 3 Preview: Python Package

**Task**: Create and publish a reusable toolkit

**You'll learn:**
- Package structure
- Testing with pytest
- Documentation
- Publishing to PyPI

**Due**: Week 12 (30% + 10% poster)

---

# Part 2: Python and Jupyter Setup

---

## Why Python for GIS?

### Three Reasons

**1. Open Source and Free**
- No license fees
- Works on any platform
- Code is transparent

**2. Massive Ecosystem**
- `geopandas`: Spatial DataFrames
- `osmnx`: Street networks
- `folium`: Interactive maps
- `shiny`: Web dashboards

**3. Reproducibility**
```python
# Anyone can run this and get same results
data = load_auckland_data()
analysis = calculate_metrics(data)
create_map(analysis)
```

---

## The Python Scientific Stack

```
┌─────────────────────────────┐
│  Your Geospatial Code       │
├─────────────────────────────┤
│  geopandas | osmnx | r5py   │ ← Spatial libraries
├─────────────────────────────┤
│  pandas | numpy | matplotlib│ ← Data science
├─────────────────────────────┤
│  Python 3.10+               │ ← Language
└─────────────────────────────┘
```

**We'll learn from bottom to top**

---

## Google Colab: Your Coding Environment

**Why Colab?**
- ✅ No installation needed
- ✅ Pre-installed packages
- ✅ Free GPU/TPU (for advanced work)
- ✅ Save to Google Drive
- ✅ Share notebooks easily

**How to access:**
1. Visit colab.research.google.com
2. Sign in with @aucklanduni.ac.nz
3. New Notebook → Start coding!

---

## Jupyter Notebook Basics

![Jupyter interface screenshot]

**Two types of cells:**

**Code Cells** (grey background):
```python
# Press Shift+Enter to run
print("Hello Auckland!")
```

**Markdown Cells** (white background):
```markdown
# Heading
This is *formatted* text
```

---

## Colab Walkthrough (DEMO)

**Let's create our first notebook together:**

1. Go to colab.research.google.com
2. File → New Notebook
3. Rename: "Week1_Introduction"
4. First code cell:
   ```python
   print("Hello from Auckland!")
   ```
5. Run with Shift+Enter

**You'll follow along in Week 1 lab**

---

## Installing Packages in Colab

**Most packages pre-installed:**
```python
import pandas as pd
import matplotlib.pyplot as plt
# These just work!
```

**For geospatial packages:**
```python
# Run once at start of notebook
!pip install geopandas
import geopandas as gpd
```

**We'll use this pattern throughout the course**

---

# Part 3: Programming Fundamentals

---

## Your First Program

```python
# This is a comment
print("Hello, Auckland!")
```

**Output:**
```
Hello, Auckland!
```

**Three concepts:**
1. Comments start with `#`
2. `print()` displays output
3. Text goes in quotes

---

## Variables: Storing Information

**Think of variables as labeled boxes:**

```python
# Store a number
population = 1_700_000

# Store text (a string)
city = "Auckland"

# Store a calculation
density = population / 1180  # Population per km²

# Display results
print(f"{city} has {population:,} people")
print(f"Density: {density:.1f} people per km²")
```

**Output:**
```
Auckland has 1,700,000 people
Density: 1440.7 people per km²
```

---

## Data Types Matter

```python
# Integer (whole number)
sa2_count = 104

# Float (decimal)
avg_income = 52_750.50

# String (text)
region = "Auckland"

# Boolean (True/False)
is_urban = True

# Check type
print(type(population))  # <class 'int'>
print(type(density))     # <class 'float'>
```

**Why care?**
- Can't add "Auckland" + 100
- But can add 50 + 100

---

## Lists: Multiple Values

```python
# List of suburbs
suburbs = ["Newmarket", "Ponsonby", "Parnell", "Grey Lynn"]

# Access by index (starts at 0!)
print(suburbs[0])  # "Newmarket"
print(suburbs[2])  # "Parnell"

# Add to list
suburbs.append("Mt Eden")

# How many items?
print(len(suburbs))  # 5
```

**Lists are fundamental to data processing**

---

## Your First Geospatial Hello World

```python
# Coordinates of Auckland Sky Tower
latitude = -36.8485
longitude = 174.7633

# Create a message
message = f"Auckland Sky Tower is at ({latitude}, {longitude})"
print(message)

# Calculate distance from origin (simplified)
distance = (latitude**2 + longitude**2)**0.5
print(f"Distance from (0,0): {distance:.2f} degrees")
```

**Output:**
```
Auckland Sky Tower is at (-36.8485, 174.7633)
Distance from (0,0): 178.61 degrees
```

---

## Preview: What's Coming in Week 2

```python
# Loops (repeating actions)
for suburb in suburbs:
    print(f"Analyzing {suburb}...")

# Conditionals (making decisions)
if population > 1_000_000:
    print("This is a major city")

# Functions (reusable code)
def calculate_density(pop, area):
    return pop / area
```

**We'll build these foundations next week**

---

# Part 4: Week 1 Lab Preview

---

## Lab Activities (2 hours)

**Part 1: Setup** (30 mins)
- Create Google Colab account
- Tour of Jupyter interface
- Create first notebook

**Part 2: Python Basics** (60 mins)
- Variables and data types
- Simple calculations
- Working with lists
- Print formatted output

**Part 3: Auckland Example** (30 mins)
- Store SA2 names in a list
- Calculate simple statistics
- Create formatted output

---

## Week 1 Lab Deliverable

**Task**: Submit a screenshot showing your first Python program

**Requirements:**
- Screenshot of Colab notebook
- Working code that:
  - Stores Auckland data in variables
  - Performs a calculation
  - Prints formatted output

**Due**: End of lab or Friday 5pm

**Worth**: Part of 5% lab participation

---

## What to Prepare

**Before Week 1 Lab:**
1. ✅ Create Google account (or use UoA email)
2. ✅ Test access to colab.research.google.com
3. ✅ Have this week's lecture slides open

**Optional but helpful:**
- Install Python locally (we'll cover this later)
- Explore Colab's example notebooks

---

## Getting Help

**During lectures:**
- Ask questions anytime
- No question is "stupid"

**During labs:**
- Teaching assistants available
- Help each other (encouraged!)
- Post on discussion forum

**Outside class:**
- Ed discussion forum
- Office hours (TBA)
- Course materials on Canvas

---

## Key Takeaways

### What You Learned Today

1. ✅ **Why we code**: Automate, reproduce, scale
2. ✅ **Course structure**: 4 parts, 3 assignments
3. ✅ **Google Colab**: Our coding environment
4. ✅ **Python basics**: Variables, types, print

### What's Next

**Week 2**: Programming fundamentals
- Control flow (if/else)
- Loops (for, while)
- Functions
- More data structures

---

## Homework (Optional)

**To get ahead:**

1. **Explore Python basics**:
   - Try the code examples from today
   - Experiment with different values
   - What happens if you change things?

2. **Think about Assignment 1**:
   - What would you want to analyze about pedestrians?
   - What questions interest you?

3. **Explore Auckland open data**:
   - data.govt.nz
   - What datasets look interesting?

---

## Looking Forward

**Journey Map:**

```
Week 1: Hello World
  ↓
Week 4: First Map (Assignment 1)
  ↓
Week 8: Web Dashboard (Assignment 2)
  ↓
Week 12: Published Package (Assignment 3)
```

**You're starting a journey from "What's a variable?" to "I published a Python package!"**

---

## Questions?

**Remember:**
- Lectures: Tuesdays 14:00-16:00
- Labs: Wednesdays (check your schedule)
- First lab: This week!

**Next week:**
- Programming fundamentals deep dive
- Working with real data
- Building toward Assignment 1

---

## See You in Lab!

**Week 1 Lab**: Wednesday
- Bring laptop
- Google Colab account ready
- Lecture slides open

**Get excited!** You're about to become a geospatial programmer.

---

## Additional Resources

**Learning Python:**
- Python.org tutorials
- Real Python (realpython.com)
- Colab tutorials (in Colab interface)

**Geospatial Resources:**
- Python-GIS book (our main text)
- GeoPandas documentation
- OSMnx examples

**All links on Canvas**
