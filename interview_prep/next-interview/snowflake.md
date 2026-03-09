# Snowflake Interview Preparation (Data Engineer)

> A comprehensive guide covering key Snowflake concepts commonly asked in Data Engineering interviews.

---

## 📋 Topics Covered

- Snowflake Architecture
- Virtual Warehouses
- Micro-partitions
- Data Ingestion
- Change Data Capture
- Performance Optimization
- Snowflake Features

---

## 1. What is Snowflake?

Snowflake is a **cloud-native data warehouse platform** designed for storing, processing, and analyzing large volumes of structured and semi-structured data.

Unlike traditional databases, Snowflake is built specifically for the cloud and **separates compute resources from storage resources**.

### Key Features

| Feature | Description |
|---|---|
| Cloud-native architecture | Built from the ground up for the cloud |
| Compute/storage separation | Scale each layer independently |
| Automatic scaling | Elastic resources based on demand |
| Semi-structured support | Handles JSON, Avro, Parquet, and more |
| High concurrency | Multiple workloads without interference |
| Built-in security | Encryption, governance, and access control |

Snowflake runs on major cloud providers: **AWS**, **Azure**, and **Google Cloud**.

---

## 2. Snowflake Architecture

Snowflake's architecture has three main layers:

### Layer 1 — Storage Layer

Stores all data in **compressed columnar format**.

- Automatic micro-partitioning
- Data compression
- Encryption at rest
- Backed by cloud object storage (e.g., AWS S3)

---

### Layer 2 — Compute Layer

Consists of **Virtual Warehouses** that execute queries.

- Query execution
- Data processing
- Aggregations, joins, and transformations
- Multiple warehouses run simultaneously without impacting each other

---

### Layer 3 — Cloud Services Layer

Manages all system-level operations:

- Authentication
- Metadata management
- Query optimization
- Infrastructure management
- Transaction management

---

## 3. What are Virtual Warehouses?

Virtual warehouses are **compute clusters** used to execute queries in Snowflake.

They provide the processing power required for:

- SQL queries
- Data loading
- Transformations
- Data aggregation

Each warehouse operates **independently** from others.

### Warehouse Sizes

| Size | Use Case |
|---|---|
| X-Small | Dev/testing, lightweight queries |
| Small | Low-volume workloads |
| Medium | Standard analytics |
| Large | Heavy workloads |
| X-Large | Complex joins, large aggregations |
| 2X-Large+ | Massive parallel processing |

### Key Characteristics

- Compute is separate from storage
- Multiple warehouses can run simultaneously
- Can be scaled up or down on demand
- Auto-suspend when idle to save cost

### Example

```sql
CREATE WAREHOUSE analytics_wh
WITH WAREHOUSE_SIZE = 'MEDIUM'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;
```

> **`AUTO_SUSPEND`** — pauses warehouse after 5 minutes of inactivity  
> **`AUTO_RESUME`** — automatically restarts warehouse when a query arrives

---

## 4. What are Micro-partitions?

Snowflake automatically divides tables into **micro-partitions** — small storage units that typically contain **50–500 MB of compressed data**.

### Metadata Stored Per Partition

- Minimum and maximum column values
- Number of distinct values
- Data statistics

This metadata enables **partition pruning** — Snowflake skips irrelevant partitions during queries.

### Example

Given a `transactions` table filtered by date:

```sql
SELECT *
FROM transactions
WHERE transaction_date = '2024-01-01';
```

Snowflake scans **only partitions containing that date** instead of the full table — significantly improving performance.

---

## 5. What is Time Travel?

Time Travel allows users to **access historical versions of data** — querying data as it existed at a previous point in time.

### Use Cases

- Recover accidentally deleted data
- Audit historical changes
- Restore modified records

### Example

```sql
SELECT *
FROM transactions
AT (TIMESTAMP => '2024-01-01 10:00:00');
```

### Retention Periods

| Snowflake Edition | Retention Period |
|---|---|
| Standard | 1 day |
| Enterprise | Up to 90 days |

---

## 6. What is Zero-Copy Cloning?

Zero-copy cloning creates **instant copies** of databases, schemas, or tables **without duplicating the underlying data**.

Snowflake creates metadata references to the original data instead of physically copying it.

### Advantages

- Instant cloning
- No additional storage cost initially
- Ideal for development and testing environments

### Example

```sql
CREATE TABLE dev_transactions CLONE prod_transactions;
```

> Developers can safely run queries on the clone without affecting production data.

---

## 7. What are Streams?

Streams **track changes** made to tables — capturing data modifications for Change Data Capture (CDC).

### Changes Captured

- `INSERT`
- `UPDATE`
- `DELETE`

### Example

```sql
CREATE STREAM transactions_stream
ON TABLE transactions;
```

This stream captures all changes made to the `transactions` table.

> Streams are commonly used **with Tasks** to build automated data pipelines.

---

## 8. What are Tasks?

Tasks are **scheduled SQL jobs** used to automate workflows in Snowflake — similar to cron jobs.

### Common Use Cases

- Running ETL pipelines
- Data transformations
- Scheduled data processing

### Example

```sql
CREATE TASK daily_sales_task
WAREHOUSE = analytics_wh
SCHEDULE = 'USING CRON 0 2 * * * UTC'
AS
INSERT INTO daily_sales
SELECT *
FROM sales
WHERE sale_date = CURRENT_DATE;
```

> This task runs **every day at 2 AM UTC**.

---

## 9. What is Snowpipe?

Snowpipe is Snowflake's **continuous data ingestion service** that automatically loads new data into tables when files arrive in cloud storage.

### Supported Cloud Storage

- AWS S3
- Azure Blob Storage
- Google Cloud Storage

### Snowpipe Workflow

```
Data files land in cloud storage
        ↓
Snowpipe detects new files
        ↓
Data is automatically loaded into Snowflake tables
```

### Example

```sql
COPY INTO transactions
FROM @s3_stage
FILE_FORMAT = (TYPE = CSV);
```

> Snowpipe enables **near real-time** data ingestion.

---

## 10. How Does Snowflake Optimize Queries?

Snowflake uses several built-in optimization techniques:

### Micro-partition Pruning
Scans only relevant micro-partitions based on filter conditions.

### Columnar Storage
Stores data in column format — ideal for analytical queries that read specific columns.

### Result Caching
If the same query is re-executed, Snowflake returns results from cache instantly.

### Automatic Query Optimization
The query optimizer automatically determines the best execution plan.

### Clustering Keys
Organizes data in large tables to reduce scanning.

```sql
ALTER TABLE transactions
CLUSTER BY (policy_id, transaction_date);
```

---

## 11. Snowflake vs Traditional Databases

| Feature | Traditional DB | Snowflake |
|---|---|---|
| Architecture | Monolithic | Cloud-native |
| Scaling | Vertical (hardware) | Elastic (on-demand) |
| Compute & Storage | Tightly coupled | Fully separated |
| Concurrency | Limited | High concurrency |
| Infrastructure | User managed | Fully managed |
| Semi-structured data | Limited support | Native support |

### Traditional Database Examples
MySQL, PostgreSQL, Oracle

---

## 📌 Key Concepts Summary

| Concept | Purpose |
|---|---|
| **Virtual Warehouses** | Independent compute clusters for query execution |
| **Micro-partitions** | Compressed storage units enabling partition pruning |
| **Time Travel** | Access historical data snapshots |
| **Zero-Copy Cloning** | Instant table/schema/database copies |
| **Streams** | Track table changes for CDC pipelines |
| **Tasks** | Schedule and automate SQL workflows |
| **Snowpipe** | Continuous, event-driven data ingestion |
| **Clustering Keys** | Optimize large table query performance |

---

*Mastering these concepts will help you design scalable and efficient data pipelines on Snowflake.*