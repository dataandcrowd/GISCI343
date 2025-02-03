---
title: 'Practical 7: Simple OOP'

---

# Practical 7: Simple OOP

If you can remember your second practical using the NZ Census 2023 dataset...(see the attached markdown file). For this exercise, we will do the exact same procedure, but simplifying some of the activities so that we don't end in a havoc.

**The overall picture**

1. Class Initialisation (`__init__`): Sets up the class with file paths and attributes for storing dataframes.
2. Import Data: Loads the total population and ethnicity data from CSV files into pandas dataframes.
3. Filter Population over 100,000
4. Plot a bar chart showing the total population for each region over 100K.

## Run the Entire OOP First

```python
import pandas as pd
import matplotlib.pyplot as plt

class CensusDataAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.census_data = None

    def import_data(self):
        # Read the CSV file into a dataframe
        self.census_data = pd.read_csv(self.file_path)
        print("Data imported successfully.")
        print("Data Preview:\n", self.census_data.head())

    def filter_population(self, threshold=100000):
        # Check if the required column names exist in the dataframe
        if 'Population' in self.census_data.columns and 'Regional council area' in self.census_data.columns:
            self.census_data = self.census_data[self.census_data['Population'] > threshold]
            print(f"Data filtered to include regions with population greater than {threshold}.")
            print(self.census_data)
        else:
            print("Error: Columns 'Population' and 'Regional council area' are not found in the dataset.")

    def plot_distribution(self):
        if self.census_data is not None and not self.census_data.empty: # Just in case any error occurs
            # Sort the data by 'Population' in descending order
            sorted_data = self.census_data.sort_values(by='Population', ascending=False)
            # Plot the distribution of population by region in descending order
            sorted_data.plot(kind='bar', x='Regional council area', y='Population', figsize=(12, 6),
                             title='Population Distribution by Region (Population > 100,000)')
            plt.xlabel('Regional Council Area')
            plt.ylabel('Population')
            plt.xticks(rotation=45)
            plt.ticklabel_format(style='plain', axis='y')  # Remove scientific notation from the y-axis
            plt.show()
            print("Population distribution plotted successfully in descending order.")
        else:
            print("Error: No data available for plotting. Please check the filtering step.")
```


## Run the objects, on your marks, set, Go

```python
# File path to the uploaded CSV file
file_path = "data/pop23_total.csv"

# Create an instance of the CensusDataAnalysis class
census_analysis = CensusDataAnalysis(file_path)

# Step 1: Import the data
census_analysis.import_data()

# Step 2: Filter the population to include only regions with population > 100,000
census_analysis.filter_population(threshold=100000)

# Step 3: Plot the population distribution by region in descending order
census_analysis.plot_distribution()
```


Well done!