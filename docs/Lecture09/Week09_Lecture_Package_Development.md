# Week 9 Lecture: Python Package Development

## Today's Journey (2 hours)

**Part 1: Urban Analytics Context - Micromobility** (45 mins)
- E-scooters and urban transport
- Data challenges and opportunities
- Network effects and policy

**Part 2: Python Package Fundamentals** (60 mins)
- Why package your code?
- Package architecture
- The `src/` layout
- `pyproject.toml` configuration

**Part 3: Building Your First Package** (15 mins)
- Live demo with `geohello`
- Week 9 lab preview

---

# Part 1: Cities, Networks, and Micromobility

---

## The Urban Mobility Revolution

![E-scooter on street]

**2018**: First e-scooter sharing launches
**2024**: 200+ cities, millions of daily trips
**Auckland**: Lime, Beam, Neuron (thousands of scooters)

**Question**: How do we analyze this data?

---

## Micromobility: What and Why?

**Definition**: Light, low-speed vehicles
- E-scooters
- Bikes and e-bikes
- E-skateboards

**Why it matters:**
- 🚲 Last-mile connectivity
- 🌱 Zero emissions
- 🚇 Complements public transport
- 🏙️ Reduces car dependence

---

## The Auckland Context

**Current state:**
- ~3,000 e-scooters operating
- 50,000+ trips per week
- Concentrated in CBD and inner suburbs
- Integration with AT public transport

**Challenges:**
- Pavement clutter
- Safety concerns
- Equity (where are they available?)
- Policy and regulation

---

## E-Scooter Trip Data

**Every trip generates data:**

```python
{
    'trip_id': 'abc123',
    'start_time': '2024-05-11 17:30:00',
    'end_time': '2024-05-11 17:45:00',
    'start_location': Point(174.7633, -36.8485),
    'end_location': Point(174.7712, -36.8556),
    'distance_m': 1247,
    'duration_sec': 892,
    'user_id': 'anonymized',
    'provider': 'Lime'
}
```

**Millions of trips → Rich dataset for analysis**

---

## Origin-Destination Patterns

**Where do people ride?**

![OD flow map showing trips between locations]

**Insights:**
- CBD → Inner suburbs (commute)
- Train stations → destinations (first/last mile)
- Universities → commercial areas (students)
- Waterfront → attractions (tourism)

**Policy question**: Where should we add infrastructure?

---

## Temporal Patterns

**When do people ride?**

![Heatmap: Hour × Day showing usage patterns]

**Patterns:**
- **Weekday peaks**: 7-9am (to work), 5-7pm (from work)
- **Weekend peaks**: 10am-4pm (leisure)
- **Weather effects**: Rain → usage drops 60%
- **Seasonal**: Summer > Winter

**Policy question**: When should we rebalance scooters?

---

## Geofencing: Spatial Boundaries

**Problem**: E-scooters everywhere!
- Blocking footpaths
- In waterways (!?)
- Dangerous parking

**Solution**: Geofencing

```python
# Define no-parking zone (e.g., waterfront)
no_parking_zone = Polygon([...])

# Check each trip end point
if trip.end_location.within(no_parking_zone):
    fine_user()
    alert_provider()
```

**Policy tool**: Control where scooters can be parked

---

## Geofencing Zones in Auckland

![Map showing different geofencing zones]

**Zone types:**
- ✅ **Parking zones** (designated areas)
- ⚠️ **Slow zones** (speed limit 10 km/h)
- 🚫 **No-ride zones** (waterfront, reserves)
- 🚫 **No-parking zones** (narrow footpaths)

**Challenge**: Enforcement and compliance

---

## Network Analysis: Connectivity

**E-scooters use street networks:**

![Street network with e-scooter trips overlaid]

**Questions:**
- Which streets are most used?
- Where are the bottlenecks?
- How connected is the network?
- Where should we improve infrastructure?

**Tools**: OSMnx, networkX, betweenness centrality

---

## Network Centrality

**Betweenness centrality**: How many shortest paths pass through a node?

![Network with high-centrality nodes highlighted]

**High centrality** = important for connectivity
- Major intersections
- Transport hubs
- Shopping districts

**Application**: Prioritize these for e-scooter infrastructure

---

## Integration with Public Transport

**The "last mile problem":**

```
Home → [Walk 15 min] → Bus → [Walk 10 min] → Work
```

**With e-scooters:**

```
Home → [E-scooter 5 min] → Bus → [E-scooter 3 min] → Work
```

**Data analysis needed:**
- Where are PT stops underserved?
- What's the catchment with e-scooters?
- How many trips connect to PT?

---

## Accessibility Analysis

**Question**: How many destinations can you reach in 15 minutes?

**Traditional** (walking only):
- Average: 8 destinations

**With e-scooters**:
- Average: 23 destinations (+188%!)

**Method**: r5py routing with multi-modal options

---

## Policy Challenges

**Safety:**
- Helmet usage
- Speed limits
- Footpath vs. road
- Crash data analysis

**Equity:**
- Where are scooters available?
- Who uses them? (demographics)
- Pricing and accessibility
- Digital divide

**Environment:**
- Are they replacing cars or transit?
- Lifecycle emissions
- Rebalancing vehicle emissions

---

## Data-Driven Policy: Case Study

**Glasgow Low Emission Zone (LEZ) Study**

**Question**: What's the health impact of restricting vehicles?

**Method:**
1. Simulate traffic with SUMO
2. Model emissions (NOx, PM2.5)
3. Estimate health outcomes
4. Compare scenarios (LEZ vs. no LEZ)

**Result**: Data informs policy decisions

**Your packages can enable this analysis!**

---

## Reusable Tools for Micromobility

**Common analysis needs:**

- **Trip processing**: Clean, validate, aggregate
- **Geofencing**: Check compliance, generate reports
- **OD analysis**: Flow matrices, visualization
- **Network metrics**: Centrality, connectivity
- **Visualization**: Maps, charts, dashboards

**Solution**: Package these functions!

---

## Example: Micromobility Analysis Toolkit

```python
from micromobility import (
    process_trips,
    check_geofencing,
    calculate_od_flows,
    network_centrality
)

# Load data
trips = process_trips('scooter_data.csv')

# Check compliance
violations = check_geofencing(trips, parking_zones)

# Analyze flows
flows = calculate_od_flows(trips, sa2_boundaries)

# Network analysis
centrality = network_centrality(street_network, trips)
```

**This is what you'll build for Assignment 3!**

---

## Why Package Your Micromobility Code?

**Without a package:**
- Copy-paste code between projects
- Fix bugs in multiple places
- Hard to share with colleagues
- No standard workflows

**With a package:**
```bash
pip install auckland-micromobility
```
- Install once, use everywhere
- Fix bugs in one place
- Easy to share
- Reproducible analysis

---

# Part 2: Python Package Fundamentals

---

## From Scripts to Packages

**Evolution of your code:**

**Week 2**: Scripts
```python
# analysis.py
print("Hello Auckland")
```

**Week 5**: Functions
```python
# utils.py
def calculate_density(gdf):
    return gdf.area / gdf.population
```

**Week 9**: Packages
```bash
pip install your-package
```
```python
from your_package import calculate_density
```

---

## What is a Python Package?

**Module**: A single Python file
```python
# data.py
def load_sa2():
    pass
```

**Package**: A directory of modules
```
my_package/
├── __init__.py      # Makes it a package!
├── data.py
├── metrics.py
└── viz.py
```

**Distribution**: The installable bundle
```
my_package-1.0.0-py3-none-any.whl
```

---

## Package Terminology

**Library**: Code you import (geopandas, pandas)

**Application**: Code you run (qgis, jupyter)

**We're building libraries** for this course.

---

## Why Package Your Code?

### 1. Reusability

**Without package:**
```bash
project1/ has calculate_density()
project2/ has calculate_density() (copy-pasted)
project3/ has calculate_density() (copy-pasted again)

# Bug found? Fix in 3 places! 😱
```

**With package:**
```bash
pip install urban-toolkit

# All projects use same code
# Bug found? Fix once, update everywhere! ✅
```

---

## Why Package Your Code? (continued)

### 2. Reproducibility

```python
# In your research paper
pip install auckland-gis==1.2.0

from auckland_gis import calculate_accessibility
result = calculate_accessibility(...)
```

**Anyone can:**
- Install exact version
- Reproduce your analysis
- Verify your results

---

## Why Package Your Code? (continued)

### 3. Collaboration

**Sharing code:**
- ❌ Send zip file, hope it works
- ❌ "Install these 15 packages first"
- ❌ "Clone repo, edit paths..."

**With package:**
- ✅ `pip install team-toolkit`
- ✅ Done!

---

## Why Package Your Code? (continued)

### 4. Career Development

**Employability:**
- "I built and published Python packages"
- Demonstrates real-world skills
- Public portfolio on PyPI

**Community:**
- Contributing to open source
- Building professional network
- Potential impact beyond your work

---

## The `src/` Layout (Best Practice)

**Modern Python packages use `src/` layout:**

```
my-package/
├── src/
│   └── my_package/       # Your code here
│       ├── __init__.py
│       ├── data.py
│       └── metrics.py
├── tests/                # Tests here
│   └── test_data.py
├── pyproject.toml        # Configuration
└── README.md
```

---

## Why `src/` Layout?

**Old way** (flat layout):
```
my-package/
├── my_package/    # Code directly here
├── tests/
└── pyproject.toml
```

**Problem**: Tests might import from local directory instead of installed package!

**New way** (`src/` layout):
```
my-package/
├── src/
│   └── my_package/  # Code in src/
├── tests/
└── pyproject.toml
```

**Benefit**: Forces tests to use installed package = more reliable

---

## What Goes in `__init__.py`?

**Minimal** (just version):
```python
"""My Package for Urban Analytics."""

__version__ = "0.1.0"
```

**Better** (export main functions):
```python
"""My Package for Urban Analytics."""

__version__ = "0.1.0"

from .data import load_sa2
from .metrics import calculate_density

__all__ = ["load_sa2", "calculate_density"]
```

**Now users can:**
```python
from my_package import load_sa2  # Clean!
```

---

## Module Organization

**Organize by functionality, not type**

**❌ Don't do this:**
```
src/my_package/
├── functions.py
├── classes.py
└── utils.py
```

**✅ Do this:**
```
src/my_package/
├── data.py        # Data loading
├── metrics.py     # Calculations
├── network.py     # Network analysis
└── viz.py         # Visualization
```

---

## `pyproject.toml`: Package Configuration

**The heart of your package:**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "Urban analytics toolkit"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "geopandas>=0.14.0",
    "pandas>=2.0.0",
]
```

---

## `pyproject.toml` Sections

**Build system**: How to build
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Project metadata**: Name, version, dependencies
```toml
[project]
name = "my-package"
version = "0.1.0"
dependencies = ["geopandas>=0.14.0"]
```

**Optional dependencies**: For extras
```toml
[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=23.0"]
```

---

## Dependencies: What to Include?

**Runtime dependencies** (required to use package):
```toml
dependencies = [
    "geopandas>=0.14.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
]
```

**Development dependencies** (for package development):
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
]
```

---

## Package Naming Conventions

**PyPI name** (in `pyproject.toml`):
```toml
name = "auckland-gis"  # Hyphens OK
```

**Python package name** (directory):
```
src/auckland_gis/  # Underscores!
```

**Import name**:
```python
import auckland_gis  # Matches directory
```

**Rule**: PyPI uses hyphens, Python uses underscores

---

## Version Numbers: Semantic Versioning

**Format**: `MAJOR.MINOR.PATCH`

```
1.2.3
│ │ └─ Patch: Bug fixes
│ └─── Minor: New features (backwards compatible)
└───── Major: Breaking changes
```

**Examples:**
- `0.1.0` → `0.1.1`: Fixed a bug
- `0.1.1` → `0.2.0`: Added new function
- `0.2.0` → `1.0.0`: Changed API, breaking change

---

# Part 3: Building Your First Package

---

## Live Demo: `geohello` Package

**Let's build together!**

**Goal**: Create a simple geospatial greeting package

**Steps:**
1. Initialize with `uv`
2. Write simple function
3. Configure `pyproject.toml`
4. Build distributions
5. Test locally

---

## Step 1: Initialize

```bash
# Install uv (if not already)
pip install uv

# Create new package
uv init --lib geohello
cd geohello
```

**Created structure:**
```
geohello/
├── src/
│   └── geohello/
│       ├── __init__.py
│       └── py.typed
├── tests/
├── pyproject.toml
└── README.md
```

---

## Step 2: Write Function

**Edit `src/geohello/__init__.py`:**

```python
"""A simple geospatial greeting package."""

__version__ = "0.1.0"

def hello(place="Auckland"):
    """
    Generate a greeting for a place.
    
    Parameters
    ----------
    place : str, default "Auckland"
        Place name to greet
        
    Returns
    -------
    str
        Greeting message
        
    Examples
    --------
    >>> hello()
    'Hello from Auckland!'
    >>> hello("Tokyo")
    'Hello from Tokyo!'
    """
    return f"Hello from {place}!"
```

---

## Step 3: Configure Metadata

**Edit `pyproject.toml`:**

```toml
[project]
name = "geohello-yourname"  # Make unique!
version = "0.1.0"
description = "A simple geospatial greeting"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = []  # No dependencies for this simple example
```

---

## Step 4: Build Distributions

```bash
# Build package
uv build
```

**Output:**
```
📦 Building...
✓ Built dist/geohello_yourname-0.1.0-py3-none-any.whl
✓ Built dist/geohello_yourname-0.1.0.tar.gz
```

**Two files created:**
- `.whl`: Wheel (fast install)
- `.tar.gz`: Source distribution (backup)

---

## Step 5: Test Locally

```bash
# Test import
uv run python -c "from geohello import hello; print(hello())"

# Should print:
# Hello from Auckland!

# Test with argument
uv run python -c "from geohello import hello; print(hello('Paris'))"

# Should print:
# Hello from Paris!
```

**Success!** Your first package works!

---

## What We Just Built

```
geohello/
├── src/
│   └── geohello/
│       └── __init__.py    ← Our code
├── dist/
│   ├── *.whl             ← Built distributions
│   └── *.tar.gz
├── pyproject.toml         ← Configuration
└── README.md
```

**Next week**: Add tests, documentation, publish to TestPyPI

---

## Week 9 Lab: Build Your First Package

**Activity** (90 mins):

1. Create `geohello-yourname` package
2. Write greeting function
3. Configure metadata
4. Build distributions
5. Test locally
6. Verify it works

**Deliverable** (completion credit):
- Screenshot of successful build
- Screenshot of successful import
- Brief reflection (100-150 words)

---

## Assignment 3 Planning

**Use remaining lab time** (30 mins):

**Questions to consider:**
- What micromobility/urban analytics topic interests you?
- What reusable functions have you written?
- What would be useful to package?
- What builds on your assignments?

**Brainstorm**: Package scope and structure

---

## Assignment 3 Preview

**Due**: Week 12 (30% + 10% poster = 40%)

**Requirements:**
- Published to production PyPI
- Proper `src/` layout
- Test coverage >80%
- Comprehensive documentation
- Example notebooks
- Professional README

**Topics**: Accessibility, micromobility, networks, urban form

---

## Package Ideas

**Micromobility toolkit:**
```
src/escooter_analytics/
├── trips.py       # Trip processing
├── geofencing.py  # Zone validation
├── flows.py       # OD analysis
└── viz.py         # Visualizations
```

**Accessibility calculator:**
```
src/accessibility/
├── isochrones.py  # Travel time areas
├── transit.py     # PT integration
└── metrics.py     # Accessibility scores
```

---

## Looking Ahead

**Week 10**: Testing and Documentation
- Writing pytest tests
- NumPy-style docstrings
- Publishing to TestPyPI
- Week 10 assessment (5%)

**Week 11**: Production Quality
- CI/CD with GitHub Actions
- Publishing to real PyPI
- Poster design

**Week 12**: Showcase
- Final submission
- Poster presentation
- Celebrate!

---

## Key Takeaways

### Micromobility

1. ✅ **E-scooters generate rich data** for analysis
2. ✅ **Network effects** important for infrastructure
3. ✅ **Policy needs data-driven tools**

### Packages

4. ✅ **Reusability** is the main benefit
5. ✅ **`src/` layout** is best practice
6. ✅ **`pyproject.toml`** is your configuration hub
7. ✅ **uv** makes building easy

---

## Resources

**Package development:**
- Python Packaging Guide: packaging.python.org
- uv documentation: docs.astral.sh/uv
- PEP 621 (`pyproject.toml`): peps.python.org/pep-0621

**Micromobility:**
- NACTO Shared Micromobility Guidelines
- Auckland Transport data portal
- Example analyses on Canvas

---

## Questions?

**Before lab:**
- Install uv: `pip install uv`
- Read Chapter 4.1 (Package Fundamentals)
- Think about Assignment 3 topic

**In lab:**
- Build `geohello` package
- Get help if stuck
- Plan Assignment 3

**See you in lab!**

---

## Homework

**This week:**

1. **Build `geohello`** in lab
2. **Read Chapter 4.1-4.2**
3. **Think about Assignment 3**:
   - What topic?
   - What functions?
   - What's the scope?

**Post on Ed**:
- Share your package ideas
- Get feedback from classmates
- Help each other!

---

## Looking Forward: Your Package Journey

```
Week 9: Build first package (geohello)
  ↓
Week 10: Add tests, publish to TestPyPI (5%)
  ↓
Week 11: Polish, CI/CD, real PyPI
  ↓
Week 12: Present & celebrate! (30% + 10%)
```

**You're starting a journey from "What's a package?" to "I published on PyPI!"**

Let's build something great! 🚀
