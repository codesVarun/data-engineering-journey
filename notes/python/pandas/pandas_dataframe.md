# Pandas DataFrame Deep Dive

## What is a DataFrame?

A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types. Think of it as a spreadsheet or SQL table in Python.

## Creating DataFrames

### From Dictionary
```python
import pandas as pd

# Simple dictionary
data = {
    'continent': ['Asia', 'Europe', 'North America'],
    'cases': [1000000, 800000, 600000],
    'deaths': [50000, 40000, 30000]
}
df = pd.DataFrame(data)
```

### From List of Dictionaries (Common in ETL)
```python
# Similar to your ETL pipeline approach
records = []
for item in api_data:
    record = {
        'continent': item.get('continent', ''),
        'cases': item.get('cases', 0),
        'updated': pd.to_datetime(item.get('updated'), unit='ms', errors='coerce')
    }
    records.append(record)

df = pd.DataFrame(records)
```

### Empty DataFrame
```python
# Create empty DataFrame with columns
df = pd.DataFrame(columns=['continent', 'cases', 'deaths'])
```

## DataFrame Attributes

```python
# Basic info about DataFrame
print(df.shape)        # (rows, columns)
print(df.columns)      # Column names
print(df.index)        # Row indices
print(df.dtypes)       # Data types of each column
print(df.info())       # Comprehensive info
print(df.describe())   # Statistical summary
```

## Data Selection and Indexing

### Column Selection
```python
# Single column (returns Series)
continent_data = df['continent']

# Multiple columns (returns DataFrame)
subset = df[['continent', 'cases']]

# Using dot notation (only for valid Python identifiers)
cases = df.cases
```

### Row Selection
```python
# First few rows
df.head()      # First 5 rows
df.head(3)     # First 3 rows

# Last few rows
df.tail()      # Last 5 rows

# Specific rows by index
df.iloc[0]     # First row
df.iloc[0:3]   # First 3 rows
df.iloc[-1]    # Last row
```

### Boolean Indexing (Filtering)
```python
# Filter rows based on condition
high_cases = df[df['cases'] > 500000]

# Multiple conditions
filtered = df[(df['cases'] > 100000) & (df['deaths'] < 50000)]

# Using isin() for multiple values
continents = df[df['continent'].isin(['Asia', 'Europe'])]
```

## Data Manipulation

### Adding Columns
```python
# Simple calculation
df['mortality_rate'] = df['deaths'] / df['cases'] * 100

# Conditional column
df['risk_level'] = df['cases'].apply(lambda x: 'High' if x > 500000 else 'Low')

# From function
def calculate_risk(row):
    if row['cases'] > 800000:
        return 'Very High'
    elif row['cases'] > 400000:
        return 'High'
    else:
        return 'Moderate'

df['risk_category'] = df.apply(calculate_risk, axis=1)
```

### Modifying Data
```python
# Update specific values
df.loc[df['continent'] == 'Asia', 'cases'] = 1200000

# Replace values
df['continent'] = df['continent'].replace('North America', 'N. America')

# Fill missing values
df['deaths'] = df['deaths'].fillna(0)
```

## Handling Missing Data

```python
# Check for missing values
print(df.isnull().sum())
print(df.isna().any())

# Drop rows with missing values
df_clean = df.dropna()

# Drop columns with missing values
df_clean = df.dropna(axis=1)

# Fill missing values
df['cases'] = df['cases'].fillna(0)                    # Fill with 0
df['continent'] = df['continent'].fillna('Unknown')    # Fill with string
df = df.fillna(method='forward')                       # Forward fill
```

## Data Types and Conversion

```python
# Check data types
print(df.dtypes)

# Convert data types
df['cases'] = df['cases'].astype('int64')
df['updated'] = pd.to_datetime(df['updated'])

# Handle errors in conversion (like in your ETL)
df['updated'] = pd.to_datetime(df['updated'], unit='ms', errors='coerce')
```

## DataFrame Operations from Your ETL Pipeline

### Working with Nested Data
```python
# Extract nested data (like continentInfo in your API)
df['lat'] = df['continentInfo'].apply(lambda x: x.get('lat', None) if pd.notna(x) else None)
df['long'] = df['continentInfo'].apply(lambda x: x.get('long', None) if pd.notna(x) else None)
```

### Adding Timestamps
```python
from datetime import datetime, timezone

# Add ETL timestamp (like in your pipeline)
etl_time = datetime.now(timezone.utc)
df['etl_timestamp'] = etl_time
```

### Preparing for Database Load
```python
# Convert DataFrame to list of tuples for database insertion
data_for_db = []
for _, row in df.iterrows():
    row_data = []
    for val in row.values:
        if pd.isna(val):
            row_data.append(None)  # Handle NaN values
        else:
            row_data.append(val)
    data_for_db.append(tuple(row_data))
```

## Grouping and Aggregation

```python
# Group by continent
grouped = df.groupby('continent')

# Aggregate functions
summary = df.groupby('continent').agg({
    'cases': 'sum',
    'deaths': 'mean',
    'population': 'max'
})

# Multiple aggregations on same column
agg_multiple = df.groupby('continent')['cases'].agg(['sum', 'mean', 'count'])
```

## Sorting and Ranking

```python
# Sort by single column
df_sorted = df.sort_values('cases', ascending=False)

# Sort by multiple columns
df_sorted = df.sort_values(['continent', 'cases'], ascending=[True, False])

# Reset index after sorting
df_sorted = df_sorted.reset_index(drop=True)
```

## Performance Tips for ETL

1. **Use vectorized operations** instead of loops
2. **Specify data types** when creating DataFrames
3. **Use categorical data** for repeated string values
4. **Chunk large datasets** when reading from files
5. **Use `pd.concat()`** instead of repeatedly appending to DataFrame

## Common ETL Patterns

### Pattern 1: Transform API Response
```python
def transform_api_data(raw_data):
    records = []
    for item in raw_data:
        record = {
            'id': item.get('id'),
            'value': item.get('value', 0),
            'timestamp': pd.to_datetime(item.get('timestamp'), errors='coerce')
        }
        records.append(record)
    
    return pd.DataFrame(records)
```

### Pattern 2: Data Validation
```python
def validate_dataframe(df):
    # Check for required columns
    required_cols = ['continent', 'cases', 'deaths']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Check for data quality
    if df['cases'].isna().any():
        print("Warning: Found missing values in cases column")
    
    return df
```

This covers the essential DataFrame operations you'll use in data engineering projects like your COVID ETL pipeline!