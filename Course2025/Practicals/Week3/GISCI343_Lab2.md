---
title: 'Lab 2: Census NZ 2023 using Python''s Pandas'

---

# GISCI343/GISCI744 Lab 2: Census NZ 2023 using Python's Pandas
2nd August, 2024

## Background info
Welcome to the second lab session, where you will learn more about more applications of data frames using New Zealands **Census 2023**. In New Zealand, the census is released every five years. This means the previous censuses were held in 2018, 2013, and so on. Currently, the website provides a comparison for the recent three censuses, so please bear this in mind. However, for today's lab session, your will take a look at the 2023 census only.

For more information, please follow the link: https://www.stats.govt.nz/2023-census/#data


## Install Python packages
Python contains a variety of packages.As of 6 May 2024, more than 530,000 Python packages are available ([Wiki](https://en.wikipedia.org/wiki/Python_Package_Index#:~:text=Some%20package%20managers%2C%20including%20pip,for%20packages%20and%20their%20dependencies.&text=As%20of%206%20May%202024,530%2C000%20Python%20packages%20are%20available.)). Among these packages, we use the `pandas` package as it is the most popular package in Python for data manipulation, cleaning, and exploration.


To use the functions in `pandas`, you must install the package via the terminal or cmd. You can type `pip install pandas` or `conda install pandas`.


## Importing dataframes

![](https://pandas.pydata.org/docs/_images/02_io_readwrite.svg)

As mentioned in the lecture, you can directly import CSV, XLSX, or other file formats (as shown in the figure) into your Python environment. For this excercise, you can load the `pop23.csv` into your environment.

```python
import pandas as pd
census = pd.read_csv('data/pop23_total.csv')
print(census)
```

Do you remember how we read the structure of the data?

The `info` methods and the `dtypes` attribute are useful for a first check. `head`/`tail` to check what the dataframe actually looks like.


```python
census.info() ## technical summary (e.g. dataframe, rows/columnns and their names)
census.dtypes ## generic summary
census.head()
census.tail()
```

* What is the dimension of the dataframe, i.e., how many columns and rows are there?
* What is the data type of each column, i.e., int, float, string?
* When you type head or tail of the dataframe, how many numbers show up by default? What happens if you input numbers between the round brackets?


Okay, can we now open another file called `pop23_ethnicity.csv`, and explore the structure of the data?



## Data cleaning

Did you notice something unusual with the ethnicity file? Yes, if you take a look at the `info()`, you will recognise that the data type are objects, not numbers. Objects are variables that contain data and functions that can be used to manipulate the data [(more info)](https://www.geeksforgeeks.org/python-object/).

Let's test some basic work.

```python
census_ethnicity["European"] + census_ethnicity["Asian"]
```

I guess it works, but for our peace in mind, we can convert the columns that contain numerical columns

How can we do this? Do you have a guess?

```python
column_headings = census_ethnicity.columns
column_headings_list = census_ethnicity.columns.tolist()
column_headings_list.remove('Regional council area')
census_ethnicity[column_headings_list] = census_ethnicity[column_headings_list].replace({',': ''}, regex=True).apply(pd.to_numeric)

print(census_ethnicity)
```

Tada!

Yes, you have just converted your columns to numerical values.
Please check the changes by typing `census_ethnicity.info()`.



We have now done some data cleaning and looked at the dataset, well done! Let's move on to our next step of data exploration!


## Data Exploration
Now that we have cleaned our data, let's dive deeper into understanding it through some exploration techniques.

To get a quick overview of the dataset, you can use the describe method which provides a summary of the central tendency, dispersion, and shape of a dataset’s distribution, excluding `NaN` values.

```python
summary_stats = census_ethnicity.describe()
print(summary_stats)
```

You can also play with the basic functions by using the `sum` function. 

```python
census_ethnicity['European'].sum(axis=0)
```

What is the difference of using `axis=0` and `axis=1`? Do you remember that I told you this from the lecture?


## Joining dataframes
To analyse the percentage of each ethnic group's population within the total population, we need to join the two dataframes: `census_ethnicity` and `census_total`.


```python
pop23 = pd.merge(census_ethnicity, census_total, on='XXXX', suffixes=('_ethnicity', '_total'))
print(pop23.head())
```

Can you guess what `XXXX` should be?

📍Thoughts: What if you want to merge the two dataframes with a different column name? How do you do that?


## Aggregating and Visualizing Population Data by Location

In this section, we will learn how to group, aggregate, and visualize population data by different locations using Census data. We will cover the following steps:

1. Aggregating Population Data by Island
2. Summing Population by Ethnic Groups
3. Plotting Population Data
4. Sorting and Plotting Data in Ascending Order
5. Adding Annotations to the Plots

### 1. Aggregating Population Data by Island

To group the data by the 'Island' column, you can use the `groupby` method in pandas. This method allows you to group data based on one or more columns and then perform aggregate operations on the grouped data.

Here are two ways to group the data by 'Island' and sum the population data:

```python
# One way to group by Island and sum all columns
grouped_by_island_all = census_data.groupby('Island').sum()
print(grouped_by_island_all)

# Another way to group by Island and sum only specific columns
grouped_by_island_specific = census_data.groupby('Island')[['European', 'Māori', 'Pacific peoples', 'Asian', 
                                                            'Middle Eastern/Latin American/African', 'Other ethnicity']].sum()
print(grouped_by_island_specific)
```

Explanation:

* `groupby('Island').sum()`: This code groups the entire DataFrame by the 'Island' column and then sums all numerical columns within each group.
* `groupby('Island')[columns].sum()`: This code groups the DataFrame by the 'Island' column and then sums only the specified columns within each group.


### 2. Summing Population by Ethnic Groups
To sum the population across all regions for each ethnic group, you can use the sum method on the selected columns.

```python
ethnic_group_sums = census_data[['European', 'Māori', 'Pacific peoples', 'Asian', 
                                 'Middle Eastern/Latin American/African', 'Other ethnicity']].sum()

print(ethnic_group_sums)
```

### 3. Plotting Population Data
You can visualise the summed population data using bar plots. Here are two examples: one for the total population of each ethnic group and one for the population data grouped by island.

Plotting the Sum of Each Ethnic Group

```python
ethnic_group_sums.plot(kind='bar', figsize=(10, 6), title='Sum of Ethnic Groups in New Zealand')
plt.xlabel('Ethnic Groups')
plt.ylabel('Population')
plt.xticks(rotation=45)
plt.show()
```

![image](https://hackmd.io/_uploads/S1ATVEPY0.png)

* switch to ascending order

```python
# Sort the sums in descending order
sorted_ethnic_group_sums = ethnic_group_sums.sort_values(ascending=False)

# Plotting the sum of each ethnic group
sorted_ethnic_group_sums.plot(kind='bar', figsize=(10, 6), title='Sum of Ethnic Groups in New Zealand')
plt.xlabel('Ethnic Groups')
plt.ylabel('Population')
plt.xticks(rotation=45)
plt.show()
```

![image](https://hackmd.io/_uploads/BJGhM5PtC.png)



Plotting the Sum of Ethnic Groups by Island

```python
# Group by Island and sum the ethnic groups
grouped_by_island = pop23.groupby('Island')[['European', 'Māori', 'Pacific peoples', 'Asian', 
                                                   'Middle Eastern/Latin American/African', 'Other ethnicity']].sum()


grouped_by_island_sorted = grouped_by_island.sort_values(ascending=False)



# Plotting the sum of ethnic groups by island
grouped_by_island_sorted.plot(kind='bar', stacked=False, figsize=(10, 6), title='Sum of Ethnic Groups by Island')
plt.xlabel('Island')
plt.ylabel('Population')
plt.xticks(rotation=0)
plt.show()

```

![image](https://hackmd.io/_uploads/S1p8E9Pt0.png)


### Alternative plots

Okay, so are you considering switching to a different type of plot? Have a look into your dataset and results and also visit the gallery here:

* Matplotlib Gallery: https://matplotlib.org/3.1.1/gallery/index.html



## Conclusion
Through this lab session, you gained hands-on experience in data manipulation, cleaning, and exploration using pandas with the Census 2023 NZ. You also learned how to effectively visualise data, which is a crucial skill in data analysis. By understanding the structure of Census data and applying various data manipulation techniques, you are now better equipped to handle real-world datasets and derive meaningful insights.



## Further thoughts
You can also think further about the following questions:

* Percentage by ethnic group
* How many are living in the North Island?
* What percentage of the total population of New Zealand does the population of Auckland account for?

