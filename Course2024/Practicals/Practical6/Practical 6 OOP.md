---
title: Practical 6 OOP with Findings
tags: [Templates, ' Talk']

---

## Object Oriented Programming - Applications in GIS
### Welcome to the sixth practical!
In this session, you'll explore a recently published research study from a scientific journal, and you will apply your knowledge of Object-Oriented Programming (OOP) to analyse real-world data.


### The study: Glasgow Low Emission Zone

![Picture1](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrLYutb-pa1yfXPzKL3Hd0IRld5aTFXAb1Jg&s)

**Shin et al (2024). Did the Implementation of Low Emission Zone in Glasgow Change the Traffic Flow and Air Quality?** The link to the study: [click here](https://findingspress.org/article/123382-did-the-implementation-of-low-emission-zone-in-glasgow-change-the-traffic-flow-and-air-quality)

:::success
A low-emission zone (LEZ) is a defined area where access by some polluting vehicles is restricted or deterred with the aim of improving air quality. This may favour vehicles such as bicycles, micromobility vehicles, (certain) alternative fuel vehicles, hybrid electric vehicles, plug-in hybrids, and zero-emission vehicles such as all-electric vehicles. (Source: Wiki)
:::


The study adresses two, very simple questions.

* How have traffic flows changed within Glasgow’s LEZ compared to the pre-LEZ period?
* Have NO<sub>2</sub> levels, a key pollutant from vehicles, changed within Glasgow’s LEZ since its enforcement?

![](https://s3.amazonaws.com/production.scholastica/public/attachments/51b54cf2-ebba-49d9-b299-6042e5b08f09/large/image1.jpeg)


Summary of the method: (not going to do everything for this practical)

* Collect traffic data from the city council API: `traffic.csv`
* Collect NO<sub>2</sub> from the UK’s Automatic Urban and Rural Network (AURN) using the openair R package: `no2.csv`
* Collect the weather data from the nearest met monitor
* Normalise the weather (i.e. removing meteorogical effect) of NO<sub>2</sub>
* Run some stats test
* Plot some results

The original R code for this analysis can be found here: [GitHub Page](https://dataandcrowd.github.io/GlasgowLEZ_Traffic/GlasgowLEZ.html)


## Your task
For this practical, we will not ask you to go through a thorough normalisation process. However, you will take a step to run a statistical analysis that can be very similar to this study.

When designing an OOP approach, you will create Python code in a separate script, focusing on the use of classes and methods.

### Step 1: Import Libraries
We will use four libraries in this exercise: `pandas` for data manipulation, `seaborn` and `matplotlib` for visualization, and `scipy` for statistical analysis.


```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
```

### Step 2: Explore the Data

```
traffic_df = pd.read_csv("traffic.csv")
```

Do you remember how to read the data overview? Yes, use `head`, `describe`, `info()` and take a peek at the data. 

Do the same with NO<sub>2</sub>.


### Step 3: Add `Class`
Now, let’s apply OOP principles to manage our data. Recall the four pillars of OOP: inheritance, encapsulation, polymorphism, and abstraction. Below is a simple class structure that uses inheritance and encapsulation.

Take a look at the class definition. Can you find the `__init__` functions and the methods? Do you also see the inheritance featured in the subclasses?

```python!
class Data:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def filter_by_date(self, start_date, end_date):
        self.data['dt_date'] = pd.to_datetime(self.data['dt_date'])
        self.data = self.data[(self.data['dt_date'] >= start_date) & 
                              (self.data['dt_date'] <= end_date)]

    def get_data(self):
        return self.data

class TrafficData(Data):
    def __init__(self, file_path):
        super().__init__(file_path)

# Subclass for NO2 Data
class NO2Data(Data):
    def __init__(self, file_path):
        super().__init__(file_path)
```
Hopefully, the code works by now!


### Step 4: Statistical Functions

Here, you will assign statistical methods to your class. Take a look at calculate_summary_stats and compare_means. What do they do?

Also, notice the use of the `seaborn` package for visualizations instead of `matplotlib`. It provides more concise syntax.

Regarding the Shapiro-Wilk normality test: if the test fails to reject the null hypothesis (H0), it means the data is normally distributed. In that case, you can perform a t-test. If the data is not normally distributed (reject H0), you need to use a non-parametric test like the Mann-Whitney U test.

```python
def calculate_summary_stats(data, group_column, value_column):
    summary_stats = data.groupby(group_column)[value_column].agg(['mean', 'std', 'count']).reset_index()
    return summary_stats

# Perform Shapiro-Wilk normality test 

def run_shapiro_test(data, group_column, value_column):
    group_2022 = data[data[group_column] == 2022][value_column]
    group_2023 = data[data[group_column] == 2023][value_column]

    print("Shapiro-Wilk Test for Normality:")

    # Shapiro-Wilk test for 2022 data
    stat_2022, p_value_2022 = stats.shapiro(group_2022)
    print(f"2022 {value_column}: stat = {stat_2022:.3f}, p-value = {p_value_2022:.3f}")
    if p_value_2022 > 0.05:
        print("2022 data looks normally distributed (fail to reject H0)")
    else:
        print("2022 data does not look normally distributed (reject H0)")

    # Shapiro-Wilk test for 2023 data
    stat_2023, p_value_2023 = stats.shapiro(group_2023)
    print(f"2023 {value_column}: stat = {stat_2023:.3f}, p-value = {p_value_2023:.3f}")
    if p_value_2023 > 0.05:
        print("2023 data looks normally distributed (fail to reject H0)")
    else:
        print("2023 data does not look normally distributed (reject H0)")


def compare_means(data, group_column, value_column):
    # Extract data for each group (2022 and 2023)
    group_2022 = data[data[group_column] == 2022][value_column]
    group_2023 = data[data[group_column] == 2023][value_column]

    # Perform t-test assuming normal distribution
    t_stat, t_p_value = stats.ttest_ind(group_2022, group_2023, equal_var=False)

    # Perform Mann-Whitney U test (for non-parametric comparison)
    u_stat, u_p_value = stats.mannwhitneyu(group_2022, group_2023)

    # Return both test results as a dictionary
    return {
        't-test': {'t-statistic': t_stat, 'p-value': t_p_value},
        'u-test': {'u-statistic': u_stat, 'p-value': u_p_value}
    }


# Function to create boxplots with summary statistics
def create_boxplot_with_stats(data, x_column, y_column, title):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=data[x_column], y=data[y_column])
    plt.title(title)
    plt.xticks(rotation=45)

    # Add mean values to the plot
    means = data.groupby(x_column)[y_column].mean().reset_index()
    for i, mean_value in enumerate(means[y_column]):
        plt.text(i, mean_value, f'{mean_value:.2f}', color='black', ha="center")

    plt.tight_layout()
    plt.show()
```


### Step 5: Load and Filter Data

```python
# Load Traffic Data
traffic = TrafficData("traffic.csv")
traffic.filter_by_date("2022-08-01", "2023-09-30")
filtered_traffic = traffic.get_data()

# Load NO2 Data
no2 = NO2Data("no2.csv")
no2.filter_by_date("2022-08-01", "2023-09-30")
filtered_no2 = no2.get_data()
filtered_no2 = filtered_no2.dropna(subset=['no2_daily'])
```

### Step 6: Run a normality test

```python
run_shapiro_test(filtered_no2, 'dt_year', 'no2_daily')
run_shapiro_test(filtered_traffic, 'dt_year', 'total_flow')
```


### Step 7: Run a statistical test

```python
# Perform test for Traffic Data (automatic choice of t-test or u-test)
traffic_test_results = compare_means(filtered_traffic, 'dt_year', 'total_flow')
print("Traffic Flow Comparison Results:")
#print(f"Test used: {traffic_test_results['test']}")
print(f"Statistic: {traffic_test_results['u-test']['u-statistic']:.3f}, P-value: {traffic_test_results['u-test']['p-value']:.3f}")

# Perform test for NO2 Data (automatic choice of t-test or u-test)
no2_test_results = compare_means(filtered_no2, 'dt_year', 'no2_daily')
print("\nNO2 Levels Comparison Results:")
#print(f"Test used: {no2_test_results['test']}")
print(f"Statistic: {no2_test_results['u-test']['u-statistic']:.3f}, P-value: {no2_test_results['u-test']['p-value']:.3f}")

```


### Step 8: Visualise the Results

```python
# Generate Boxplot for Traffic Data with Mean Values
create_boxplot_with_stats(filtered_traffic, 'dt_year', 'total_flow', 'Traffic Flow Comparison 2022 vs 2023')

# Generate Boxplot for NO2 Data with Mean Values
create_boxplot_with_stats(filtered_no2, 'dt_year', 'no2_daily', 'NO2 Levels Comparison 2022 vs 2023')

```

## Wrap up
Great job making it to the end! 

This practical allowed you to explore Object-Oriented Programming (OOP) principles through a real-world study on traffic flow and air quality. OOP provides an organised and reusable structure that makes complex code easier to manage. 

As you continue to develop your skills, you’ll see how OOP empowers you to build more efficient and scalable programs, especially when analysing large datasets.

👍👍👍👍👍👍👍👍👍👍👍