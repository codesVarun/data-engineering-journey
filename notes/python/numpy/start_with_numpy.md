# Getting Started with NumPy

## What is NumPy?

NumPy (Numerical Python) is the fundamental package for scientific computing in Python. It provides support for large, multi-dimensional arrays and matrices, along with mathematical functions to operate on these arrays.

## Installation

```bash
pip install numpy
```

## Basic Import

```python
import numpy as np
```

## Why NumPy?

1. **Performance**: Operations are implemented in C, making them much faster than pure Python
2. **Memory Efficiency**: Arrays use less memory than Python lists
3. **Vectorization**: Apply operations to entire arrays without writing loops
4. **Foundation**: Base for pandas, matplotlib, scikit-learn, and other libraries
5. **Broadcasting**: Perform operations on arrays of different shapes

## NumPy Arrays (ndarray)

### Creating Arrays

```python
# From Python list
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)              # [1 2 3 4 5]
print(type(arr1))        # <class 'numpy.ndarray'>

# 2D array
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]]

# From tuple
arr_tuple = np.array((1, 2, 3, 4))
```

### Array Creation Functions

```python
# Create arrays with specific values
zeros = np.zeros(5)              # [0. 0. 0. 0. 0.]
ones = np.ones((2, 3))           # 2x3 array of ones
full = np.full((2, 3), 7)        # 2x3 array filled with 7

# Create ranges
range_arr = np.arange(0, 10, 2)  # [0 2 4 6 8]
linspace = np.linspace(0, 1, 5)  # [0.   0.25 0.5  0.75 1.  ]

# Random arrays
random_arr = np.random.random(5)          # Random floats [0, 1)
random_int = np.random.randint(1, 10, 5)  # Random integers
```

## Array Attributes

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)      # (2, 3) - dimensions
print(arr.size)       # 6 - total number of elements
print(arr.ndim)       # 2 - number of dimensions
print(arr.dtype)      # int64 - data type
print(arr.itemsize)   # 8 - size of each element in bytes
```

## Data Types

```python
# Specify data type
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1, 2, 3], dtype=np.float64)
str_arr = np.array(['a', 'b', 'c'], dtype=np.str_)

# Convert data types
arr = np.array([1.7, 2.8, 3.9])
int_arr = arr.astype(np.int32)    # [1 2 3]
```

## Array Indexing and Slicing

### 1D Arrays
```python
arr = np.array([1, 2, 3, 4, 5])

# Basic indexing
print(arr[0])        # 1 (first element)
print(arr[-1])       # 5 (last element)

# Slicing
print(arr[1:4])      # [2 3 4]
print(arr[:3])       # [1 2 3]
print(arr[2:])       # [3 4 5]
print(arr[::2])      # [1 3 5] (every 2nd element)
```

### 2D Arrays
```python
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Element access
print(arr2d[0, 1])   # 2 (row 0, column 1)
print(arr2d[1][2])   # 6 (alternative syntax)

# Row and column access
print(arr2d[0])      # [1 2 3] (first row)
print(arr2d[:, 1])   # [2 5 8] (second column)

# Subarray
print(arr2d[0:2, 1:3])
# [[2 3]
#  [5 6]]
```

## Boolean Indexing

```python
arr = np.array([1, 2, 3, 4, 5])

# Boolean condition
mask = arr > 3
print(mask)          # [False False False  True  True]
print(arr[mask])     # [4 5]

# Direct filtering
filtered = arr[arr > 3]    # [4 5]

# Multiple conditions
result = arr[(arr > 2) & (arr < 5)]  # [3 4]
```

## Mathematical Operations

### Element-wise Operations
```python
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])

# Basic operations
print(arr1 + arr2)   # [6 8 10 12]
print(arr1 * arr2)   # [5 12 21 32]
print(arr1 ** 2)     # [1 4 9 16]

# With scalars
print(arr1 + 10)     # [11 12 13 14]
print(arr1 * 2)      # [2 4 6 8]
```

### Mathematical Functions
```python
arr = np.array([1, 4, 9, 16])

# Common functions
print(np.sqrt(arr))    # [1. 2. 3. 4.]
print(np.log(arr))     # Natural logarithm
print(np.exp(arr))     # Exponential
print(np.sin(arr))     # Sine

# Statistical functions
print(np.mean(arr))    # 7.5
print(np.median(arr))  # 6.5
print(np.std(arr))     # Standard deviation
print(np.sum(arr))     # 30
print(np.max(arr))     # 16
print(np.min(arr))     # 1
```

## Array Manipulation

### Reshaping
```python
arr = np.array([1, 2, 3, 4, 5, 6])

# Reshape to 2D
reshaped = arr.reshape(2, 3)
# [[1 2 3]
#  [4 5 6]]

# Flatten back to 1D
flattened = reshaped.flatten()  # [1 2 3 4 5 6]
```

### Concatenation and Splitting
```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Concatenate
combined = np.concatenate([arr1, arr2])  # [1 2 3 4 5 6]

# Stack
stacked = np.stack([arr1, arr2])
# [[1 2 3]
#  [4 5 6]]

# Split
arr = np.array([1, 2, 3, 4, 5, 6])
split_result = np.split(arr, 3)  # [array([1, 2]), array([3, 4]), array([5, 6])]
```

## NumPy and Pandas Integration

NumPy is the foundation of pandas. Understanding this relationship helps in data engineering:

```python
import pandas as pd
import numpy as np

# Pandas uses NumPy arrays internally
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df.values)     # Returns NumPy array
print(type(df.values))  # <class 'numpy.ndarray'>

# NumPy functions work with pandas
df['C'] = np.sqrt(df['A'])  # Apply NumPy function to pandas column
```

## Common Use Cases in Data Engineering

### 1. Data Validation
```python
# Check for missing values (NaN)
data = np.array([1, 2, np.nan, 4, 5])
print(np.isnan(data))      # [False False  True False False]
print(np.any(np.isnan(data)))  # True
```

### 2. Data Transformation
```python
# Normalize data (common in ETL)
data = np.array([10, 20, 30, 40, 50])
normalized = (data - np.mean(data)) / np.std(data)
```

### 3. Aggregations
```python
# Multi-dimensional aggregations
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(np.sum(data, axis=0))    # [12 15 18] (sum along columns)
print(np.sum(data, axis=1))    # [6 15 24] (sum along rows)
```

## Performance Benefits

```python
import time

# Python list approach
python_list = list(range(1000000))
start = time.time()
result_list = [x * 2 for x in python_list]
list_time = time.time() - start

# NumPy approach
numpy_array = np.arange(1000000)
start = time.time()
result_array = numpy_array * 2
numpy_time = time.time() - start

print(f"List time: {list_time:.4f}s")
print(f"NumPy time: {numpy_time:.4f}s")
print(f"NumPy is {list_time/numpy_time:.1f}x faster")
```

## Key Concepts to Remember

1. **Vectorization**: Operations on entire arrays without explicit loops
2. **Broadcasting**: Operations between arrays of different shapes
3. **Memory Layout**: NumPy arrays are stored in contiguous memory
4. **Data Types**: Homogeneous data types for efficiency
5. **Views vs Copies**: Understanding when operations create new arrays

## Next Steps

1. Practice array operations and indexing
2. Learn about broadcasting rules
3. Explore advanced indexing techniques
4. Understand memory management and views
5. Study integration with other scientific Python libraries

NumPy forms the foundation for effective data manipulation in your ETL pipelines!