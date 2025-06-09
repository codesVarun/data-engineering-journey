# Getting Started with Pandas

## What is Pandas?

Pandas is a powerful Python library for data manipulation and analysis. It provides data structures like DataFrames and Series that make working with structured data intuitive and efficient.

## Installation

```bash
pip install pandas
```

## Basic Import

```python
import pandas as pd
```

## Key Data Structures

### Series
A one-dimensional labeled array that can hold any data type.

```python
# Creating a Series
data = pd.Series([1, 2, 3, 4, 5])
print(data)

# Series with custom index
data = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
```

### DataFrame
A two-dimensional labeled data structure with columns of potentially different types.

```python
# Creating a DataFrame from dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Tokyo']
}
df = pd.DataFrame(data)
print(df)
```

## Why Pandas for Data Engineering?

1. **Data Cleaning**: Handle missing values, duplicates, and data type conversions
2. **Data Transformation**: Group, aggregate, merge, and reshape data
3. **Data Analysis**: Statistical operations and data exploration
4. **File I/O**: Read/write various formats (CSV, JSON, Excel, SQL databases)
5. **Integration**: Works seamlessly with other Python libraries (NumPy, Matplotlib, etc.)

## Common Use Cases in ETL Pipelines

- **Extract**: Reading data from APIs, files, databases
- **Transform**: Data cleaning, aggregation, and restructuring
- **Load**: Preparing data for database insertion or file export

## Key Features

- **Missing Data Handling**: Built-in methods for dealing with NaN values
- **Data Alignment**: Automatic alignment of data based on labels
- **Flexible Indexing**: Multiple ways to select and filter data
- **Group Operations**: Split-apply-combine operations
- **Time Series**: Powerful tools for working with dates and times

## Real-World Example from ETL Pipeline

In your COVID ETL pipeline, pandas is used to:
- Transform raw JSON data into structured DataFrames
- Handle missing values with error handling
- Convert timestamps using `pd.to_datetime()`
- Prepare data for database insertion

```python
# Example from your transform.py
base_record = {
    "continent": continent.get("continent", ""),
    "cases": continent.get("cases", 0),
    "updated": pd.to_datetime(continent.get("updated"), unit="ms", errors="coerce"),
    # ... other fields
}
df = pd.DataFrame(continent_records)
```

## Next Steps

1. Learn DataFrame operations (selection, filtering, grouping)
2. Understand data cleaning techniques
3. Practice with different data formats
4. Explore time series functionality
5. Learn about performance optimization