# Week 6 Lecture: Shiny for Python + WebGIS

## Today's Structure (2 hours total)

**Hour 1: Guest Lecture - Transport Accessibility** (60 mins)
- Guest: Alex Raichev (Transport modelling expert)
- Accessibility metrics and practice
- Real-world applications

**Hour 2: Shiny for Python Introduction** (60 mins)
- From static to interactive
- Shiny architecture
- Your first dashboard
- Assignment 2 overview

---

# Hour 1: Guest Lecture

---

## Welcome Alex Raichev

**Background:**
- Transport modelling expert
- Accessibility analysis
- Real-world urban planning applications

**Today's topics:**
- What is accessibility?
- How do we measure it?
- Applications in Auckland
- Career pathways in transport analytics

**Student instructions:**
- Take notes
- Prepare questions for Q&A
- Think about connections to Assignment 2

---

## [Guest Lecture: 55 minutes]

**Topic**: Transport Accessibility Analysis

**Key concepts to listen for:**
- Isochrones and travel time analysis
- Multi-modal accessibility
- Equity considerations
- Data requirements

---

## Q&A with Guest (5 minutes)

**Suggested questions:**
- How do you handle data quality issues?
- What tools do you use in practice?
- How can students prepare for this field?
- Real-world challenges you've faced?

---

# Hour 2: Shiny for Python

---

## From Static to Interactive

**Assignment 1** (what you built):
```python
# Static choropleth map
sa2.plot(column='density', legend=True)
plt.savefig('map.png')  # Fixed image
```

**Assignment 2** (what you'll build):
```python
# Interactive dashboard
# Users can:
# - Select date range → Map updates
# - Choose metric → Colors change
# - Filter data → View refreshes
# All in real-time, in their browser!
```

---

## The Problem with Static Maps

![Static map screenshot]

**Users want to:**
- See different time periods
- Compare locations
- Filter by criteria
- Download data

**Solution:** Interactive web dashboards!

---

## Why Shiny?

**Traditional web dev** (HTML + JavaScript):
```javascript
// Complex!
document.getElementById('map').addEventListener('click', 
  function(e) {
    // 50 lines of code...
  }
);
```

**Shiny** (Python):
```python
# Simple!
@reactive.event(input.date_range)
def filtered_data():
    return data[data['date'].between(input.date_range())]
```

**Write Python, get web apps!**

---

## Shiny Mental Model

```
┌──────────────────────────────────┐
│  Browser (User Interface)         │
│  ┌────────────┐  ┌─────────────┐ │
│  │  Inputs    │  │   Outputs   │ │
│  │  [Slider]  │  │   [Map]     │ │
│  │  [Select]  │  │   [Plot]    │ │
│  └────────────┘  └─────────────┘ │
└──────────────────────────────────┘
         ↕                ↕
┌──────────────────────────────────┐
│  Python (Server Logic)            │
│  def calculate():                 │
│      # Your code here             │
│      return results               │
└──────────────────────────────────┘
```

**You write the middle layer in Python!**

---

## Shiny Architecture: Three Components

**1. UI (User Interface)**
```python
from shiny import ui

app_ui = ui.page_fluid(
    ui.h2("Auckland Dashboard"),
    ui.input_slider("hour", "Hour", 0, 23, 12),
    ui.output_plot("traffic_plot")
)
```

**2. Server (Logic)**
```python
def server(input, output, session):
    @output
    @render.plot
    def traffic_plot():
        data = filter_by_hour(input.hour())
        return create_plot(data)
```

**3. App (Connect them)**
```python
from shiny import App
app = App(app_ui, server)
```

---

## Your First Shiny App

```python
from shiny import App, ui, render

# UI: What users see
app_ui = ui.page_fluid(
    ui.h2("Pedestrian Counter"),
    ui.input_numeric("count", "Enter count:", value=100),
    ui.output_text_verbatim("result")
)

# Server: What happens
def server(input, output, session):
    @output
    @render.text
    def result():
        count = input.count()
        if count > 500:
            return f"{count} - HIGH TRAFFIC! 🚨"
        else:
            return f"{count} - Normal traffic ✓"

# Connect them
app = App(app_ui, server)
```

---

## Demo: Run the App

```python
# In Colab/terminal
from shiny import run_app
run_app(app)
```

**Browser opens:**
```
┌──────────────────────────────┐
│ Pedestrian Counter           │
├──────────────────────────────┤
│ Enter count: [___100___]     │
│                              │
│ 100 - Normal traffic ✓       │
└──────────────────────────────┘
```

**Change 100 → 600:**
```
600 - HIGH TRAFFIC! 🚨
```

**It's reactive - updates automatically!**

---

## Reactive Programming

**Key concept**: When inputs change, outputs automatically update

```python
input.hour()  # User moves slider
    ↓
filtered_data()  # Automatic recalculation
    ↓
traffic_plot()  # Automatic re-render
    ↓
Browser updates  # User sees new plot
```

**You don't manage the updates - Shiny does!**

---

## Input Widgets

**Numbers:**
```python
ui.input_numeric("count", "Count:", value=100)
ui.input_slider("hour", "Hour:", min=0, max=23, value=12)
```

**Text:**
```python
ui.input_text("sensor", "Sensor ID:", value="PED_001")
ui.input_text_area("notes", "Notes:", rows=3)
```

**Choices:**
```python
ui.input_select("day", "Day:", choices=["Mon", "Tue", "Wed"])
ui.input_radio_buttons("view", "View:", choices=["Map", "Chart"])
ui.input_checkbox("weekend", "Include weekends?", value=True)
```

---

## Input Widgets (continued)

**Dates:**
```python
ui.input_date("start", "Start date:")
ui.input_date_range("dates", "Date range:")
```

**Files:**
```python
ui.input_file("upload", "Upload CSV:")
```

**Action:**
```python
ui.input_action_button("go", "Calculate!", class_="btn-primary")
```

---

## Output Types

**Text:**
```python
ui.output_text("simple_text")
ui.output_text_verbatim("formatted_text")  # Fixed-width
```

**Plots:**
```python
ui.output_plot("matplotlib_plot")
```

**Tables:**
```python
ui.output_table("data_table")
ui.output_data_frame("interactive_table")
```

**UI elements:**
```python
ui.output_ui("dynamic_content")
```

---

## Example: Interactive Filter

```python
from shiny import App, ui, render
import pandas as pd

# Load data
pedestrian_data = pd.read_csv('auckland_pedestrians.csv')

app_ui = ui.page_fluid(
    ui.h2("Auckland Pedestrian Dashboard"),
    
    # Inputs
    ui.input_select(
        "sensor",
        "Select Sensor:",
        choices=pedestrian_data['sensor_id'].unique().tolist()
    ),
    ui.input_slider(
        "hour_range",
        "Hour Range:",
        min=0, max=23, value=[8, 18]
    ),
    
    # Outputs
    ui.output_plot("time_series"),
    ui.output_table("summary_stats")
)
```

---

## Example: Server Logic

```python
def server(input, output, session):
    
    @reactive.calc
    def filtered_data():
        # Filter by user selections
        data = pedestrian_data[
            (pedestrian_data['sensor_id'] == input.sensor()) &
            (pedestrian_data['hour'] >= input.hour_range()[0]) &
            (pedestrian_data['hour'] <= input.hour_range()[1])
        ]
        return data
    
    @output
    @render.plot
    def time_series():
        data = filtered_data()
        plt.figure(figsize=(10, 6))
        plt.plot(data['timestamp'], data['count'])
        plt.title(f"Pedestrian Counts: {input.sensor()}")
        return plt.gcf()
    
    @output
    @render.table
    def summary_stats():
        data = filtered_data()
        return data.describe()
```

---

## Reactive Calculations

**Problem**: Calculate once, use many times

```python
@reactive.calc
def expensive_calculation():
    # This runs only when inputs change
    data = load_and_process_data(input.date_range())
    return analyze(data)

@output
@render.plot
def plot1():
    results = expensive_calculation()  # Uses cached result
    return make_plot(results)

@output
@render.table
def table1():
    results = expensive_calculation()  # Same cached result
    return results
```

**Benefit**: Efficiency! Calculate once, display many ways.

---

## Adding Maps with ipyleaflet

```python
from ipyleaflet import Map, Marker, CircleMarker
from shinywidgets import output_widget, render_widget

app_ui = ui.page_fluid(
    ui.h2("Interactive Map"),
    ui.input_slider("threshold", "Min Count:", 0, 1000, 500),
    output_widget("map")
)

def server(input, output, session):
    @output
    @render_widget
    def map():
        # Create map
        m = Map(center=(-36.8485, 174.7633), zoom=13)
        
        # Add sensors above threshold
        sensors = get_sensors_above(input.threshold())
        for sensor in sensors:
            marker = CircleMarker(
                location=(sensor.lat, sensor.lon),
                radius=10,
                color='red'
            )
            m.add_layer(marker)
        
        return m
```

---

## Multi-Page Apps

```python
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Overview",
        ui.h2("Dashboard Overview"),
        ui.output_plot("summary_plot")
    ),
    ui.nav_panel(
        "Map View",
        ui.h2("Interactive Map"),
        output_widget("map")
    ),
    ui.nav_panel(
        "Data Table",
        ui.h2("Raw Data"),
        ui.output_data_frame("data_table")
    ),
    title="Auckland Pedestrian Dashboard"
)
```

---

## Layout Options

**Sidebar:**
```python
ui.page_sidebar(
    ui.sidebar(
        # Inputs here
        ui.input_slider(...),
        ui.input_select(...)
    ),
    # Main content here
    ui.output_plot("main_plot")
)
```

**Columns:**
```python
ui.layout_columns(
    ui.card(ui.output_plot("plot1")),
    ui.card(ui.output_plot("plot2")),
    col_widths=[6, 6]  # 50/50 split
)
```

---

## Cards for Organisation

```python
ui.card(
    ui.card_header("Traffic Statistics"),
    ui.output_table("stats"),
    ui.card_footer("Updated hourly")
)
```

**Benefits:**
- Visual grouping
- Organised layout
- Professional appearance

---

## Assignment 2 Overview

**Due**: Week 8 (8 May, 35% of grade)

**Requirements:**
- Multi-page Shiny dashboard (3+ pages)
- Interactive map with ipyleaflet
- Temporal/comparative analysis
- Network analysis (optional but encouraged)
- Deployed with shinylive (WASM)

**Topics you can choose:**
- Pedestrian flows
- Green space accessibility  
- E-scooter patterns
- Transport analysis
- 15-minute city assessment
- Air quality

---

## Assignment 2 Technical Requirements

**Must include:**

1. **Reactive inputs** (sliders, selects, date ranges)
2. **Interactive map** (ipyleaflet or folium)
3. **Multiple visualizations** (plots, tables, cards)
4. **Temporal analysis** (time series, patterns)
5. **Comparative analysis** (locations, periods)
6. **Clean, professional UI** (cards, layouts, styling)

**Optional but encouraged:**
- Network analysis with OSMnx
- Custom calculations with r5py
- Animation/temporal slider

---

## Shinylive: Deploy Without Servers

**Traditional web apps:**
```
User → Server (running Python) → Response
        ↑ (Costs money, needs maintenance)
```

**Shinylive (WASM):**
```
User → Browser (runs Python in WebAssembly) → Response
        ↑ (Free! No server needed!)
```

**Benefits:**
- Free hosting on GitHub Pages
- No server costs
- Works offline
- Fast (no server round-trips)

---

## How Shinylive Works

```python
# 1. Create normal Shiny app
app = App(app_ui, server)

# 2. Convert to shinylive
# (Automatic with export command)

# 3. Deploy to GitHub Pages
# Now anyone can use it in their browser!
```

**Your Assignment 2 must be deployed with shinylive**

---

## Example Assignment 2 Structure

```python
app_ui = ui.page_navbar(
    # Page 1: Overview
    ui.nav_panel(
        "Overview",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_date_range("dates", "Date range:"),
                ui.input_select("sensor", "Sensor:", choices=sensors)
            ),
            ui.card(
                ui.card_header("Time Series"),
                ui.output_plot("timeseries")
            ),
            ui.card(
                ui.card_header("Statistics"),
                ui.output_table("stats")
            )
        )
    ),
    
    # Page 2: Map
    ui.nav_panel(
        "Map View",
        ui.input_slider("hour", "Hour:", 0, 23, 12),
        output_widget("interactive_map")
    ),
    
    # Page 3: Analysis
    ui.nav_panel(
        "Analysis",
        ui.output_plot("heatmap"),
        ui.output_plot("comparison")
    ),
    
    title="Auckland Pedestrian Dashboard"
)
```

---

## Week 7 Preview: Network Analysis

**Next week** (ANZAC week - work session):

**Topics:**
- OSMnx for street networks
- Route analysis with r5py
- Network centrality measures
- Congestion analysis
- Integration into dashboards

**You'll build these skills for Assignment 2**

---

## Lab This Week

**Focus: Start Assignment 2**

**Activities:**
1. Install Shiny and dependencies
2. Create basic app structure
3. Add one interactive input
4. Add one output (plot or map)
5. Test reactivity
6. Plan your dashboard structure

**Bring:** Ideas for your dashboard topic!

---

## Getting Started Tips

**Start simple:**
```python
# Week 6: Basic app with one input, one output
# Week 7: Add map, multiple pages
# Week 8: Polish, test, deploy
```

**Don't try to build everything at once!**

**Iterate:**
1. Get something working
2. Add one feature
3. Test
4. Repeat

---

## Common Shiny Pitfalls

**❌ Forgetting `()` on inputs:**
```python
# Wrong
hour = input.hour  # This is a function, not a value!

# Right
hour = input.hour()  # Call it to get the value
```

**❌ Not using `@reactive.calc` for expensive ops:**
```python
# Inefficient - recalculates twice
@output
@render.plot
def plot1():
    data = load_and_process()  # Slow!
    return make_plot(data)

@output
@render.table
def table1():
    data = load_and_process()  # Slow again!
    return data
```

---

## Common Shiny Pitfalls (continued)

**✅ Use reactive calculations:**
```python
@reactive.calc
def processed_data():
    return load_and_process()  # Once!

@output
@render.plot
def plot1():
    return make_plot(processed_data())  # Reuses

@output
@render.table
def table1():
    return processed_data()  # Reuses
```

---

## Debugging Shiny Apps

**Use print statements:**
```python
@reactive.calc
def filtered_data():
    print(f"Filtering for sensor: {input.sensor()}")  # Debug
    data = filter_function()
    print(f"Found {len(data)} rows")  # Debug
    return data
```

**Check browser console:**
- Right-click → Inspect → Console
- Look for JavaScript errors

**Test components separately:**
```python
# Test your functions outside Shiny first
data = pd.read_csv('test.csv')
result = your_function(data)
print(result)  # Does it work?
```

---

## Resources for Assignment 2

**Shiny:**
- Official docs: shiny.posit.co/py
- Gallery: shinylive.io/py/examples
- Component reference: shiny.posit.co/py/components

**Examples:**
- Canvas: Example dashboards
- GitHub: Student examples from previous years

**Help:**
- Labs: TA support
- Ed discussion: Post questions
- Office hours: Thursday 2-4pm

---

## Key Takeaways

### Shiny Fundamentals

1. ✅ **Three parts**: UI + Server + App
2. ✅ **Reactive**: Outputs auto-update
3. ✅ **Python**: Write Python, get web apps
4. ✅ **Shinylive**: Deploy free with WASM

### Assignment 2

5. ✅ **Multi-page dashboard** required
6. ✅ **Interactive map** required
7. ✅ **Start simple**, iterate
8. ✅ **Due Week 8** (35% of grade)

---

## Next Week

**Week 7: Network Analysis + Dashboard Work Session**

**You'll learn:**
- OSMnx for street networks
- r5py for routing
- Network measures
- Congestion analysis
- Integration with Shiny

**Plus**: Protected lab time to work on Assignment 2

---

## Questions?

**Before next week:**
- Install Shiny: `pip install shiny shinylive shinywidgets`
- Test basic app from lecture notes
- Decide on Assignment 2 topic
- Review requirements on Canvas

**See you in lab Wednesday!**

---

## Homework

**Try this weekend:**

1. **Run the example apps** from lecture
2. **Modify one input** (change slider range, add option)
3. **Add one output** (new plot, table, or text)
4. **Post screenshot** on Ed discussion

**Get comfortable with Shiny before diving into Assignment 2!**

---

## Looking Ahead

**Week 7**: Network analysis + work session
**Week 8**: Advanced features + deployment
**Assignment 2 due**: End of Week 8

**Timeline:**
- Week 6 lab: Basic app structure
- Week 7 lab: Add maps and networks
- Week 8 lab: Polish and deploy

**Stay on track!**
