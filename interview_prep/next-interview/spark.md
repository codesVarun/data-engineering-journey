# Apache Spark Interview Preparation (Data Engineer)

> A comprehensive guide covering key Apache Spark concepts, architecture, and coding patterns commonly asked in Data Engineering interviews.

---

## 📋 Topics Covered

- Spark Architecture & Core Concepts
- RDDs, DataFrames & Datasets
- Spark Execution Model
- Transformations & Actions
- Joins & Shuffles
- Spark SQL & Catalyst Optimizer
- Partitioning & Bucketing
- Caching & Persistence
- Spark Streaming & Structured Streaming
- Performance Tuning & Optimization
- Spark on YARN / Cluster Managers
- Common Interview Scenarios

---

## 1. What is Apache Spark?

Apache Spark is an **open-source, distributed computing framework** designed for large-scale data processing. It was developed at UC Berkeley's AMPLab and later donated to the Apache Software Foundation.

Spark provides an interface for programming entire clusters with **implicit data parallelism and fault tolerance**.

### Key Features

| Feature | Description |
|---|---|
| In-memory processing | Data is processed in RAM — up to 100x faster than Hadoop MapReduce |
| Unified engine | Supports batch, streaming, ML, and graph processing |
| Lazy evaluation | Builds execution plan before running — enables optimization |
| Fault tolerance | Recovers lost data via lineage (DAG) |
| Language support | Python (PySpark), Scala, Java, R, SQL |
| Distributed | Runs across clusters of hundreds of machines |

### Spark vs Hadoop MapReduce

| Feature | Hadoop MapReduce | Apache Spark |
|---|---|---|
| Processing | Disk-based | In-memory |
| Speed | Slow (disk I/O) | Up to 100x faster |
| Ease of use | Verbose Java code | High-level APIs |
| Real-time support | No | Yes (Structured Streaming) |
| Iterative workloads | Poor | Excellent |

---

## 2. Spark Architecture

Spark follows a **Master-Worker (Driver-Executor)** architecture.

```
┌─────────────────────────────────────────────┐
│               DRIVER PROGRAM                │
│  SparkContext / SparkSession                │
│  DAG Scheduler → Task Scheduler             │
└────────────────────┬────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │    CLUSTER MANAGER    │
         │ (YARN / Mesos / K8s)  │
         └──────┬────────┬───────┘
                │        │
        ┌───────▼──┐  ┌──▼───────┐
        │ EXECUTOR │  │ EXECUTOR │
        │ (Worker) │  │ (Worker) │
        │ Task Task│  │ Task Task│
        └──────────┘  └──────────┘
```

### Driver

The **Driver** is the main process that:
- Hosts the `SparkSession` / `SparkContext`
- Converts user code into a DAG (Directed Acyclic Graph)
- Schedules tasks across executors
- Coordinates job execution
- Collects results

### Executors

**Executors** are worker processes that:
- Run on worker nodes in the cluster
- Execute tasks assigned by the driver
- Store data in memory or disk for caching
- Report status back to the driver

### Cluster Manager

Manages resource allocation across the cluster. Supported options:
- **Standalone** — Spark's built-in cluster manager
- **Apache YARN** — Hadoop's resource manager
- **Apache Mesos** — General-purpose cluster manager
- **Kubernetes** — Container-based orchestration

---

## 3. What are RDDs?

**RDD (Resilient Distributed Dataset)** is the fundamental data structure of Spark.

An RDD is an **immutable, distributed collection of objects** that can be processed in parallel across a cluster.

### RDD Properties

| Property | Description |
|---|---|
| **Resilient** | Fault-tolerant — can recompute lost partitions via lineage |
| **Distributed** | Data is split across multiple nodes |
| **Dataset** | A collection of partitioned data |
| **Immutable** | Cannot be modified once created |
| **Lazy** | Transformations are not executed until an action is called |

### Creating an RDD

```python
from pyspark import SparkContext

sc = SparkContext("local", "MyApp")

# From a list
rdd = sc.parallelize([1, 2, 3, 4, 5])

# From a file
rdd = sc.textFile("hdfs://path/to/file.txt")
```

### RDD Lineage (DAG)

Every transformation on an RDD creates a new RDD with a record of how it was derived. This chain is called the **lineage graph** and is used for fault recovery.

```
textFile → filter → map → reduceByKey → collect
   (RDD1)   (RDD2)  (RDD3)   (RDD4)     (Action)
```

---

## 4. RDD vs DataFrame vs Dataset

These are the three main abstractions in Spark.

| Feature | RDD | DataFrame | Dataset |
|---|---|---|---|
| API level | Low-level | High-level | High-level |
| Type safety | Yes (compile-time) | No | Yes (compile-time) |
| Schema | No | Yes | Yes |
| Optimization | Manual | Catalyst optimizer | Catalyst optimizer |
| Serialization | Java serialization | Tungsten encoder | Tungsten encoder |
| Language support | All | All | Scala, Java only |
| Performance | Slower | Faster | Faster |
| Use case | Fine-grained control | Analytics / SQL | Type-safe + optimized |

### DataFrame Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MyApp").getOrCreate()

# Create DataFrame from CSV
df = spark.read.csv("transactions.csv", header=True, inferSchema=True)

df.show(5)
df.printSchema()
```

### When to Use What

- **RDD** — When you need fine-grained control, custom serialization, or working with unstructured data
- **DataFrame** — For structured/semi-structured data analytics and SQL operations
- **Dataset** — When you need type safety with high performance (Scala/Java only)

---

## 5. Transformations vs Actions

Spark operations are divided into **Transformations** and **Actions**.

### Transformations

Transformations are **lazy** — they define a new RDD/DataFrame but do not execute immediately. Spark builds a DAG and only executes when an action is called.

#### Narrow Transformations
No data shuffle required — each input partition maps to one output partition.

| Transformation | Description | Example |
|---|---|---|
| `map()` | Apply function to each element | `rdd.map(lambda x: x * 2)` |
| `filter()` | Keep elements matching condition | `rdd.filter(lambda x: x > 5)` |
| `flatMap()` | Map then flatten results | `rdd.flatMap(lambda x: x.split(" "))` |
| `select()` | Select columns in DataFrame | `df.select("name", "age")` |
| `withColumn()` | Add or update a column | `df.withColumn("tax", df.amount * 0.1)` |

#### Wide Transformations
Require **shuffling data** across partitions/nodes — expensive operation.

| Transformation | Description | Example |
|---|---|---|
| `groupByKey()` | Group values by key | `rdd.groupByKey()` |
| `reduceByKey()` | Aggregate values by key | `rdd.reduceByKey(lambda a, b: a + b)` |
| `join()` | Join two datasets | `df1.join(df2, "id")` |
| `distinct()` | Remove duplicates | `df.distinct()` |
| `repartition()` | Redistribute data across partitions | `df.repartition(10)` |

### Actions

Actions **trigger execution** of the DAG and return results to the driver or write to storage.

| Action | Description | Example |
|---|---|---|
| `collect()` | Return all data to driver | `rdd.collect()` |
| `count()` | Count number of elements | `df.count()` |
| `show()` | Display top rows | `df.show(10)` |
| `take(n)` | Return first n elements | `rdd.take(5)` |
| `first()` | Return first element | `rdd.first()` |
| `write()` | Write data to storage | `df.write.parquet("output/")` |
| `saveAsTextFile()` | Save RDD to text file | `rdd.saveAsTextFile("output/")` |

### Example — Transformation + Action

```python
# Read data
df = spark.read.csv("sales.csv", header=True, inferSchema=True)

# Transformations (lazy — not executed yet)
filtered_df = df.filter(df.amount > 1000)
grouped_df = filtered_df.groupBy("region").sum("amount")

# Action (triggers execution)
grouped_df.show()
```

---

## 6. What is Lazy Evaluation?

Lazy evaluation means Spark **does not execute transformations immediately** when they are called. Instead, it builds a logical plan (DAG) and only executes when an action is triggered.

### Benefits of Lazy Evaluation

- **Optimization** — Spark can optimize the entire DAG before execution
- **Efficiency** — Avoids unnecessary computation
- **Fault recovery** — DAG enables recomputation of lost partitions

### Example

```python
# None of these lines execute immediately
rdd = sc.parallelize(range(1, 1000000))
rdd2 = rdd.filter(lambda x: x % 2 == 0)
rdd3 = rdd2.map(lambda x: x * 10)

# THIS triggers execution of the entire chain
result = rdd3.collect()
```

---

## 7. What is a DAG in Spark?

A **DAG (Directed Acyclic Graph)** is a sequence of computations performed on data in Spark.

- Each node represents an RDD or DataFrame
- Each edge represents a transformation
- The graph is acyclic — no cycles

### DAG Execution Flow

```
Job → Stages → Tasks
```

- **Job** — A full computation triggered by one action
- **Stage** — A group of transformations that can run without shuffling
- **Task** — A unit of work sent to one executor (one per partition)

### Stage Boundaries

Stage boundaries are created at **wide transformations** (shuffle operations):

```
Stage 1: map → filter        (narrow — no shuffle)
         ↓ SHUFFLE
Stage 2: groupByKey → count  (wide — requires shuffle)
```

### Viewing the DAG

You can view the DAG in **Spark UI** at `http://driver-host:4040`.

---

## 8. Partitioning in Spark

Partitioning is how Spark **divides data** across nodes in a cluster.

### Why Partitioning Matters

- Controls parallelism
- Affects performance of shuffles and joins
- Wrong partitioning leads to data skew

### Default Partitioning

Spark uses `spark.default.parallelism` (default: number of CPU cores) to determine initial partition count.

### Repartition vs Coalesce

| Feature | `repartition(n)` | `coalesce(n)` |
|---|---|---|
| Direction | Increase or decrease | Decrease only |
| Shuffle | Full shuffle | Minimal shuffle |
| Data distribution | Even | May be uneven |
| Use case | Increase parallelism | Reduce partitions before write |
| Cost | Expensive | Cheaper |

```python
# Repartition — full shuffle, even distribution
df = df.repartition(20)

# Coalesce — reduce partitions with minimal shuffle
df = df.coalesce(5)

# Check number of partitions
print(df.rdd.getNumPartitions())
```

### Partition by Column

```python
# Partition by a column (useful before joins or aggregations)
df = df.repartition(10, "region")
```

---

## 9. Joins in Spark

Spark supports multiple join types and strategies.

### Join Types

```python
# Inner join
df1.join(df2, "id", "inner")

# Left join
df1.join(df2, "id", "left")

# Right join
df1.join(df2, "id", "right")

# Full outer join
df1.join(df2, "id", "outer")

# Cross join
df1.crossJoin(df2)
```

### Join Strategies

| Strategy | When Used | Description |
|---|---|---|
| **Broadcast Join** | One table is small | Small table is broadcast to all executors — no shuffle |
| **Sort-Merge Join** | Both tables are large | Both sides are sorted and merged — involves shuffle |
| **Shuffle Hash Join** | Medium-sized tables | Hash-based join after shuffle |

### Broadcast Join (Most Important for Optimization)

```python
from pyspark.sql.functions import broadcast

# Force broadcast join
result = large_df.join(broadcast(small_df), "id")
```

> **Rule of thumb:** Broadcast tables smaller than `spark.sql.autoBroadcastJoinThreshold` (default: 10MB).

### Avoiding Data Skew in Joins

```python
# Add salt to skewed key
from pyspark.sql.functions import concat, lit, floor, rand

# Salting technique for skewed joins
df_skewed = df_skewed.withColumn("salted_key", 
    concat(df_skewed.key, lit("_"), (floor(rand() * 10)).cast("string")))
```

---

## 10. Spark SQL & Catalyst Optimizer

**Spark SQL** allows querying structured data using SQL syntax.

```python
# Register DataFrame as temp view
df.createOrReplaceTempView("transactions")

# Run SQL query
result = spark.sql("""
    SELECT region, SUM(amount) AS total_sales
    FROM transactions
    WHERE sale_date >= '2024-01-01'
    GROUP BY region
    ORDER BY total_sales DESC
""")

result.show()
```

### Catalyst Optimizer

The **Catalyst Optimizer** is Spark SQL's query optimization engine.

```
SQL Query / DataFrame API
         ↓
  Unresolved Logical Plan
         ↓
   Resolved Logical Plan  ← (Analysis: schema validation)
         ↓
  Optimized Logical Plan  ← (Optimization: predicate pushdown, constant folding)
         ↓
    Physical Plans         ← (Multiple plans generated)
         ↓
  Best Physical Plan       ← (Cost-based selection)
         ↓
      Execution
```

### Key Optimizations by Catalyst

- **Predicate Pushdown** — Filter data as early as possible (even at the source)
- **Constant Folding** — Pre-evaluate constant expressions
- **Column Pruning** — Read only required columns
- **Join Reordering** — Reorder joins for efficiency

---

## 11. Caching & Persistence

Caching stores intermediate results in memory so they don't need to be recomputed.

### Cache vs Persist

| Feature | `cache()` | `persist()` |
|---|---|---|
| Storage level | MEMORY_AND_DISK | Configurable |
| Flexibility | Fixed | Choose storage level |

### Storage Levels

| Level | Description |
|---|---|
| `MEMORY_ONLY` | Store in RAM only — recompute if not enough memory |
| `MEMORY_AND_DISK` | Spill to disk if RAM is full |
| `DISK_ONLY` | Store only on disk |
| `MEMORY_ONLY_SER` | Serialized in RAM — less space, more CPU |
| `OFF_HEAP` | Store in off-heap memory |

```python
from pyspark import StorageLevel

# Cache (default: MEMORY_AND_DISK)
df.cache()

# Persist with specific storage level
df.persist(StorageLevel.MEMORY_AND_DISK)

# Unpersist when done
df.unpersist()
```

### When to Cache

- DataFrames used **multiple times** in the same application
- After expensive transformations (joins, aggregations)
- Iterative algorithms (ML training loops)

---

## 12. Shuffling in Spark

A **shuffle** is the process of redistributing data across partitions — typically across network and disk.

### Operations That Cause Shuffles

- `groupByKey()`, `reduceByKey()`
- `join()`, `cogroup()`
- `repartition()`
- `distinct()`
- `sortBy()`, `orderBy()`

### Why Shuffles Are Expensive

- Data is written to disk
- Data is transferred over the network
- Causes stage boundaries in DAG

### Minimizing Shuffles

```python
# BAD — groupByKey sends all values to one partition
rdd.groupByKey().mapValues(sum)

# GOOD — reduceByKey combines locally before shuffling
rdd.reduceByKey(lambda a, b: a + b)
```

> **`reduceByKey` is always preferred over `groupByKey`** for aggregations.

---

## 13. Bucketing & Partitioning (File-Level)

### File Partitioning

Organizes files into directory hierarchies based on column values.

```python
# Write partitioned by date
df.write \
  .partitionBy("year", "month") \
  .parquet("output/transactions/")
```

Output structure:
```
output/transactions/
├── year=2024/
│   ├── month=01/
│   └── month=02/
└── year=2025/
    └── month=01/
```

### Bucketing

Organizes data within partitions into a fixed number of buckets using a hash of a column.

```python
df.write \
  .bucketBy(10, "customer_id") \
  .sortBy("customer_id") \
  .saveAsTable("bucketed_transactions")
```

### Partitioning vs Bucketing

| Feature | Partitioning | Bucketing |
|---|---|---|
| Column type | Low cardinality (date, region) | High cardinality (ID, user) |
| File structure | Directories | Fixed number of files |
| Join optimization | Partition pruning | Eliminates shuffle in joins |
| Use case | Filter-heavy queries | Join-heavy queries |

---

## 14. Structured Streaming

Structured Streaming is Spark's **real-time stream processing** engine built on top of Spark SQL.

It treats a live stream as an **unbounded table** — new data is appended as new rows.

### Key Concepts

| Concept | Description |
|---|---|
| **Trigger** | How often to process new data |
| **Watermark** | Handles late-arriving data |
| **Output Mode** | How results are written (append, complete, update) |
| **Checkpoint** | Saves state for fault recovery |

### Example — Read from Kafka

```python
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .load()

# Parse JSON value
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

schema = StructType() \
    .add("id", StringType()) \
    .add("amount", DoubleType())

parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
              .select("data.*")

# Aggregate
agg_df = parsed_df.groupBy("id").sum("amount")

# Write output
query = agg_df.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
```

### Output Modes

| Mode | Description |
|---|---|
| `append` | Only new rows are written |
| `complete` | Full result table is rewritten each trigger |
| `update` | Only changed rows are written |

### Watermarking (Handling Late Data)

```python
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes"), "region") \
  .sum("amount")
```

---

## 15. Performance Tuning & Optimization

### 1. Use DataFrames/Datasets over RDDs
DataFrames leverage the Catalyst optimizer and Tungsten execution engine.

### 2. Broadcast Small Tables
```python
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(lookup_df), "id")
```

### 3. Avoid `collect()` on Large Data
`collect()` pulls all data to the driver — can cause OOM errors.
```python
# BAD
data = df.collect()

# GOOD — use show(), take(), or write to storage
df.show(20)
df.write.parquet("output/")
```

### 4. Use `reduceByKey` instead of `groupByKey`
```python
# BAD
rdd.groupByKey().mapValues(sum)

# GOOD
rdd.reduceByKey(lambda a, b: a + b)
```

### 5. Cache Strategically
```python
# Cache only what is reused
expensive_df = df.join(other_df, "id").filter(...).cache()
```

### 6. Tune Parallelism
```python
spark.conf.set("spark.sql.shuffle.partitions", "200")  # default
# For smaller datasets, reduce this
spark.conf.set("spark.sql.shuffle.partitions", "50")
```

### 7. Use Columnar File Formats
Prefer **Parquet** or **ORC** over CSV/JSON for analytics:
```python
df.write.parquet("output/")         # Columnar, compressed
df.write.orc("output/")             # Alternative columnar format
```

### 8. Predicate Pushdown
Write filters early in your query chain:
```python
# GOOD — filter before join
df.filter(df.date >= "2024-01-01").join(other_df, "id")
```

### 9. Avoid Data Skew
Identify skewed partitions and use salting:
```python
# Check partition sizes
df.rdd.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
```

### 10. Tune Memory Settings
```python
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.driver.memory", "2g")
spark.conf.set("spark.memory.fraction", "0.8")
```

---

## 16. Spark Configuration & Deployment

### SparkSession Setup

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyDataPipeline") \
    .master("yarn") \
    .config("spark.executor.instances", "10") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "100") \
    .enableHiveSupport() \
    .getOrCreate()
```

### Submitting a Spark Job

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 10 \
  --executor-cores 4 \
  --executor-memory 8g \
  --driver-memory 4g \
  --conf spark.sql.shuffle.partitions=100 \
  my_spark_job.py
```

### Deploy Modes

| Mode | Driver Location | Use Case |
|---|---|---|
| `client` | Local machine submitting job | Interactive / debugging |
| `cluster` | One of the worker nodes | Production workloads |

---

## 17. Common Interview Scenarios & Answers

### Q: How do you handle data skew in Spark?

**Answer:**
1. **Identify skew** — Use Spark UI to find tasks taking much longer than others
2. **Salting** — Add a random salt to the skewed key before join, then remove it
3. **Broadcast join** — If one side is small, broadcast it
4. **Repartition** — Repartition by a different column

```python
# Salting example
import pyspark.sql.functions as F

n_salt = 10
df_large = df_large.withColumn("salt", (F.rand() * n_salt).cast("int"))
df_large = df_large.withColumn("salted_key", F.concat(F.col("key"), F.lit("_"), F.col("salt")))

df_small = df_small.withColumn("salt", F.explode(F.array([F.lit(i) for i in range(n_salt)])))
df_small = df_small.withColumn("salted_key", F.concat(F.col("key"), F.lit("_"), F.col("salt")))

result = df_large.join(df_small, "salted_key").drop("salt", "salted_key")
```

---

### Q: What is the difference between `map` and `flatMap`?

**Answer:**
- `map` — Applies a function to each element and returns **one output per input**
- `flatMap` — Applies a function to each element and **flattens the result**

```python
rdd = sc.parallelize(["hello world", "foo bar"])

# map — returns list of lists
rdd.map(lambda x: x.split(" ")).collect()
# [['hello', 'world'], ['foo', 'bar']]

# flatMap — returns flat list
rdd.flatMap(lambda x: x.split(" ")).collect()
# ['hello', 'world', 'foo', 'bar']
```

---

### Q: What happens when you call `cache()` on a DataFrame?

**Answer:**
- Spark marks the DataFrame for caching but **does not cache it immediately** (lazy)
- The data is cached the **first time an action is executed** on it
- Subsequent actions on the same DataFrame reuse cached data
- Always call `unpersist()` when done to free memory

---

### Q: Explain the difference between `repartition` and `coalesce`.

**Answer:**
- `repartition(n)` — Full shuffle, can increase or decrease partitions, ensures even distribution
- `coalesce(n)` — Minimal shuffle, can only decrease partitions, may result in uneven distribution but is faster

> Use `coalesce` before writing output files. Use `repartition` when you need even distribution for parallel processing.

---

### Q: How does fault tolerance work in Spark?

**Answer:**
Spark achieves fault tolerance through **RDD lineage (DAG)**:
1. Every RDD tracks its parent RDDs and the transformation applied
2. If a partition is lost (executor failure), Spark **recomputes only that partition** using the lineage
3. No need to replicate data across nodes
4. For Structured Streaming, fault tolerance is achieved via **checkpointing**

---

### Q: What is the Tungsten Execution Engine?

**Answer:**
Tungsten is Spark's **physical execution engine** introduced in Spark 1.4. It focuses on:
- **Memory management** — Off-heap memory management, avoiding JVM GC overhead
- **Cache-aware computation** — Data structures optimized for CPU cache
- **Code generation** — Generates bytecode at runtime for faster execution
- **Binary storage format** — Stores data in binary (not Java objects) to save memory

---

## 📌 Key Concepts Summary

| Concept | Description |
|---|---|
| **RDD** | Immutable, distributed, fault-tolerant data collection |
| **DataFrame** | Schema-based distributed table with SQL support |
| **DAG** | Execution plan built from transformations |
| **Lazy Evaluation** | Transformations execute only when action is called |
| **Shuffle** | Redistributing data across partitions — expensive |
| **Broadcast Join** | Sends small table to all executors — avoids shuffle |
| **Catalyst** | Query optimizer for Spark SQL and DataFrames |
| **Tungsten** | Low-level execution engine for memory and CPU efficiency |
| **Structured Streaming** | Real-time stream processing on unbounded tables |
| **Partitioning** | Dividing data across directories for efficient reads |
| **Bucketing** | Fixed-file data organization for join optimization |
| **Cache/Persist** | Store intermediate results to avoid recomputation |

---

## 🔧 Quick Reference — PySpark Cheat Sheet

```python
# Read data
df = spark.read.csv("file.csv", header=True, inferSchema=True)
df = spark.read.parquet("file.parquet")
df = spark.read.json("file.json")

# Basic operations
df.show(10)
df.printSchema()
df.count()
df.describe().show()

# Select & Filter
df.select("col1", "col2")
df.filter(df.age > 30)
df.where(df.region == "US")

# Aggregations
df.groupBy("region").agg({"amount": "sum", "id": "count"})

# Joins
df1.join(df2, "id", "inner")
df1.join(broadcast(df2), "id")

# Window functions
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, lag

w = Window.partitionBy("region").orderBy("amount")
df.withColumn("rank", rank().over(w))

# Write data
df.write.mode("overwrite").parquet("output/")
df.write.mode("append").partitionBy("date").parquet("output/")

# SQL
df.createOrReplaceTempView("my_table")
spark.sql("SELECT * FROM my_table WHERE amount > 100").show()
```

---

*Mastering these Spark concepts will prepare you for Data Engineering interviews at all levels — from junior to senior and staff engineer roles.*