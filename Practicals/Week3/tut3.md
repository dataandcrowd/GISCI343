

## Creating New Columns of summary statistics from Existing Data in `df`

![](https://pandas.pydata.org/docs/_images/05_newcolumn_1.svg){fig-align=center}

* Required for performing calculations across columns.
* Essential for data manipulation.


---

### Example


```python
import pandas as pd

# Creating the dataset with student names
data = {
    'Student': ['Alice', 'Bob', 'Charlie'],
    'Maths': [9, 8, 7],
    'English': [4, 10, 6],
    'Science': [8, 7, 8],
    'History': [9, 6, 5]
}
df1 = pd.DataFrame(data)

# Calculating the total score for each student and adding it as a new column 'Total'
df1['Total'] = df1[['Maths', 'English', 
                    'Science', 'History']].sum(axis=1)
# Display the updated dataset
print(df1)
```

```
   Student  Maths  English  Science  History  Total
0    Alice      9        4        8        9     30
1      Bob      8       10        7        6     31
2  Charlie      7        6        8        5     26
```
