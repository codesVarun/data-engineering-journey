# PySpark Basics

## 1. What is PySpark?

PySpark is the **Python API for Apache Spark**, an open-source distributed computing framework designed for big data processing and analytics. It allows developers and data engineers to use Python to write Spark applications, leveraging Spark's scalability and fault tolerance.

* Built on top of **Apache Spark**.
* Provides access to Spark's core functionalities such as **RDDs, DataFrames, Spark SQL, MLlib, and Structured Streaming**.
* Bridges the gap between the Python ecosystem (NumPy, Pandas, Scikit-learn) and big data frameworks.

---

## 2. Why Use PySpark?

* **Scalability**: Can process terabytes to petabytes of data across multiple nodes in a cluster.
* **Performance**: Much faster than traditional data tools (like Pandas) for very large datasets due to in-memory processing.
* **Unified Engine**: Single framework for batch, streaming, SQL, and machine learning.
* **Fault Tolerance**: Automatically recovers lost computations using **RDD lineage**.
* **Integration**: Works with Hadoop, Hive, HDFS, S3, Kafka, JDBC databases, and more.

---

## 3. PySpark Architecture Overview

PySpark is built on Apache Spark’s architecture:

* **Driver Program**: Runs the main application and converts user code into tasks.
* **Cluster Manager**: Allocates resources across the cluster (YARN, Mesos, Kubernetes, or Spark Standalone).
* **Executors**: Run tasks assigned by the driver on worker nodes.
* **Tasks**: Smallest unit of work sent to executors.

---

## 4. PySpark Core Concepts

### a) RDD (Resilient Distributed Dataset)

* Low-level abstraction for distributed data.
* Immutable, fault-tolerant collection of objects partitioned across nodes.
* Supports **transformations** (`map`, `filter`) and **actions** (`count`, `collect`).
* Example:

```python
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
squares = rdd.map(lambda x: x * x)
print(squares.collect())
```

### b) DataFrame

* High-level abstraction built on RDDs.
* Tabular data structure with rows and named columns (like Pandas DataFrame but distributed).
* Supports SQL queries and DataFrame API.
* Example:

```python
data = [(1, "Alice", 29), (2, "Bob", 31)]
df = spark.createDataFrame(data, ["id", "name", "age"])
df.show()
```

### c) Spark SQL

* Run SQL queries directly on DataFrames.
* Uses Catalyst Optimizer for performance.
* Example:

```python
df.createOrReplaceTempView("people")
sqlDF = spark.sql("SELECT name, age FROM people WHERE age > 30")
sqlDF.show()
```

### d) Spark MLlib

* Machine Learning library in Spark.
* Provides scalable implementations of ML algorithms (classification, regression, clustering).

### e) Spark Structured Streaming

* Framework for processing **real-time data streams**.
* Handles data from Kafka, socket, files, etc.
* Example:

```python
streamingDF = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()
streamingDF.writeStream.format("console").start().awaitTermination()
```

---

## 5. Where PySpark Fits in Data Engineering

* **Ingestion**: Reads raw data from Kafka, S3, HDFS, JDBC sources.
* **Transformation & Cleansing**: Joins, aggregations, filtering, window functions.
* **Enrichment**: Combines multiple datasets, prepares features.
* **Loading**: Writes into data lakes (S3, ADLS) or warehouses (Snowflake, Redshift).
* **Streaming Pipelines**: Real-time ETL with Structured Streaming.

---

## 6. Common PySpark Operations

### Creating DataFrames

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("PySparkBasics").getOrCreate()

data = [("Varun", "Data Engineer", 28), ("Amit", "Analyst", 25)]
columns = ["name", "role", "age"]

df = spark.createDataFrame(data, columns)
df.show()
```

### Transformations

```python
# Select specific columns
df.select("name", "age").show()

# Filter rows
df.filter(df.age > 26).show()

# Add new column
df.withColumn("age_plus_1", df.age + 1).show()

# Group by aggregation
df.groupBy("role").avg("age").show()
```

### Actions

```python
print(df.count())
print(df.collect())
```

---

## 7. Key Optimization Techniques

* Use **DataFrame API** over RDD for performance (Catalyst optimizer, Tungsten engine).
* Minimize **shuffling** (use broadcast joins when possible).
* Cache/persist reused DataFrames.
* Partitioning based on data volume and query patterns.
* Avoid wide transformations (like groupBy) if unnecessary.

---

## 8. PySpark Interview Questions

1. Difference between RDD, DataFrame, Dataset?
2. What is lazy evaluation in Spark?
3. What are transformations and actions?
4. How does Spark achieve fault tolerance?
5. How do you optimize Spark jobs?
6. Explain narrow vs wide transformations.
7. What is shuffling and why is it expensive?
8. Difference between Spark SQL and DataFrame API.
9. How does Spark handle schema evolution?
10. How do you handle skewed data in Spark?

---

## 9. Summary

PySpark is a **powerful distributed data processing framework** for data engineers. It provides scalability, fault tolerance, and integrations with modern data systems. It sits at the **processing and transformation layer** of the data stack, making it an essential skill for any Data Engineer.