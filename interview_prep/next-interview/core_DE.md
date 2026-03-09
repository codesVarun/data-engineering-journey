# Data Engineering Architecture Interview Preparation

> A comprehensive guide covering core Data Engineering architecture concepts, patterns, and best practices commonly asked in Data Engineering interviews.

---

## 📋 Topics Covered

- Data Lake
- Data Warehouse
- Data Mart
- Data Lakehouse
- Batch vs Streaming Processing
- ETL vs ELT
- Lambda & Kappa Architecture
- Medallion Architecture
- Data Pipeline Design
- Orchestration
- Data Modeling Concepts
- Common Interview Questions & Answers

---

## 1. What is a Data Lake?

A **Data Lake** is a centralized repository that stores **raw, unprocessed data at any scale** — structured, semi-structured, and unstructured — in its native format until it is needed.

Unlike a data warehouse, a data lake stores data **without a predefined schema** (schema-on-read).

### Key Characteristics

| Feature | Description |
|---|---|
| **Schema-on-read** | Schema is applied when data is read, not when stored |
| **All data types** | Structured (CSV), semi-structured (JSON, XML), unstructured (images, logs) |
| **Raw storage** | Data stored as-is from source systems |
| **Low cost** | Uses cheap object storage (S3, ADLS, GCS) |
| **Scalable** | Can scale to petabytes |
| **Flexible** | Any tool can read from it |

### Data Lake Storage Layers

```
┌─────────────────────────────────────────────────┐
│                   DATA LAKE                     │
│                                                 │
│  ┌───────────┐  ┌───────────┐  ┌────────────┐  │
│  │   RAW     │  │ PROCESSED │  │  CURATED   │  │
│  │  Landing  │  │  Cleaned  │  │ Aggregated │  │
│  │  CSV/JSON │→ │  Parquet  │→ │  Parquet   │  │
│  │  As-is    │  │  Filtered │  │  BI-ready  │  │
│  └───────────┘  └───────────┘  └────────────┘  │
└─────────────────────────────────────────────────┘
```

### Data Lake vs Data Swamp

A poorly managed data lake becomes a **Data Swamp** — data that is:
- Undocumented and untracked
- Difficult to discover and trust
- Without access controls or governance

**Prevention:** Use a Data Catalog (AWS Glue, Apache Atlas) and enforce data governance.

### Common Technologies

| Layer | Technology |
|---|---|
| Storage | AWS S3, Azure ADLS, Google Cloud Storage |
| Processing | Apache Spark, AWS Glue, Databricks |
| Querying | Amazon Athena, Presto, Trino |
| Catalog | AWS Glue Catalog, Apache Atlas, Hive Metastore |
| Governance | AWS Lake Formation, Apache Ranger |

---

## 2. What is a Data Warehouse?

A **Data Warehouse (DWH)** is a centralized repository optimized for **analytical queries and reporting**. It stores **historical, structured, and processed data** organized for business intelligence.

Unlike a data lake, data in a warehouse is **cleaned, transformed, and modeled** before storage (schema-on-write).

### Key Characteristics

| Feature | Description |
|---|---|
| **Schema-on-write** | Data modeled and structured before loading |
| **Structured data** | Tabular, relational format |
| **Historical data** | Long-term storage of business history |
| **Optimized for reads** | Columnar storage, indexing, partitioning |
| **Single source of truth** | Consistent, trusted data for reporting |
| **OLAP workloads** | Designed for complex analytical queries |

### Data Warehouse Architecture

```
Source Systems (CRM, ERP, APIs)
          ↓
     Staging Area          ← Temporary landing zone
          ↓
   Data Warehouse          ← Cleaned, modeled, historical
   ┌────────────────┐
   │  Core / ODS    │      ← Integrated operational data
   │  Data Vault    │      ← Raw historical vault (optional)
   │  Data Marts    │      ← Subject-area specific views
   └────────────────┘
          ↓
    BI / Reporting Tools   ← Tableau, Power BI, Looker
```

### Common Data Warehouse Platforms

| Platform | Type | Best For |
|---|---|---|
| **Amazon Redshift** | Cloud | AWS ecosystem, large-scale analytics |
| **Snowflake** | Cloud | Multi-cloud, separation of compute/storage |
| **Google BigQuery** | Cloud | Serverless, Google ecosystem |
| **Azure Synapse** | Cloud | Microsoft ecosystem |
| **Databricks** | Cloud | Lakehouse, Spark-based |
| **Teradata** | On-premise/Cloud | Enterprise legacy workloads |

---

## 3. What is a Data Mart?

A **Data Mart** is a **subject-specific subset** of a data warehouse designed for a particular business unit or functional area.

It contains pre-aggregated, filtered data relevant to a specific team — making queries faster and simpler for end users.

### Types of Data Marts

| Type | Description | Example |
|---|---|---|
| **Dependent** | Sourced directly from the central data warehouse | Finance mart from enterprise DWH |
| **Independent** | Standalone, sourced directly from operational systems | Small team's own sales mart |
| **Hybrid** | Combination of both approaches | Marketing mart from DWH + external data |

### Data Mart Examples

```
Enterprise Data Warehouse
        ├── Finance Data Mart       (revenue, costs, budgets)
        ├── Sales Data Mart         (opportunities, deals, quotas)
        ├── Marketing Data Mart     (campaigns, leads, conversions)
        ├── HR Data Mart            (headcount, payroll, attrition)
        └── Operations Data Mart    (inventory, logistics, supply chain)
```

### Data Lake vs Data Warehouse vs Data Mart

| Feature | Data Lake | Data Warehouse | Data Mart |
|---|---|---|---|
| Data type | Raw, all types | Structured, processed | Structured, aggregated |
| Schema | Schema-on-read | Schema-on-write | Schema-on-write |
| Users | Data engineers, data scientists | Analysts, engineers | Business users, analysts |
| Scope | Enterprise-wide | Enterprise-wide | Department-specific |
| Size | Petabytes | Terabytes | Gigabytes to Terabytes |
| Query speed | Slower | Fast | Fastest |
| Cost | Low (object storage) | Medium–High | Medium |
| Flexibility | Very high | Medium | Low |

---

## 4. What is a Data Lakehouse?

A **Data Lakehouse** is a modern architecture that **combines the best of data lakes and data warehouses** — storing raw data cheaply in object storage while providing ACID transactions, schema enforcement, and fast query performance.

### Problem It Solves

| Data Lake Problems | Data Warehouse Problems |
|---|---|
| No ACID transactions | Expensive storage |
| No schema enforcement | Doesn't support unstructured data |
| Slow query performance | Rigid schema — hard to change |
| No data quality guarantees | Limited ML/AI support |

### Lakehouse Architecture

```
┌─────────────────────────────────────────────┐
│              DATA LAKEHOUSE                 │
│                                             │
│  Object Storage (S3 / ADLS / GCS)          │
│  +                                          │
│  Open Table Format (Delta / Iceberg / Hudi) │
│  = ACID + Schema + Performance              │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Bronze  │→ │  Silver  │→ │   Gold   │  │
│  │  Raw     │  │ Cleaned  │  │Aggregated│  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

### Open Table Formats

| Format | Creator | Key Feature |
|---|---|---|
| **Delta Lake** | Databricks | ACID, time travel, schema evolution |
| **Apache Iceberg** | Netflix/Apple | Hidden partitioning, snapshot isolation |
| **Apache Hudi** | Uber | Upserts, incremental processing |

### Lakehouse Platforms

- **Databricks** — Built on Delta Lake
- **Snowflake** — Iceberg support + native lakehouse features
- **AWS** — S3 + Glue + Iceberg + Athena
- **Google BigLake** — BigQuery + Cloud Storage

---

## 5. What is the Difference Between Batch and Streaming Processing?

### Batch Processing

**Batch processing** collects data over a period of time and processes it all at once in a scheduled job.

```
Data accumulates → Trigger at scheduled time → Process entire batch → Load results
     (hours/days)       (nightly, hourly)          (minutes/hours)
```

**Characteristics:**
- High throughput
- Higher latency (minutes to hours)
- Simpler to implement and debug
- Cost-efficient for large volumes
- Suitable when real-time is not required

**Tools:** Apache Spark, AWS Glue, Hadoop MapReduce, dbt

### Streaming Processing

**Streaming processing** processes data **continuously** as it arrives — event by event or in micro-batches.

```
Event arrives → Processed immediately → Result available in seconds/milliseconds
```

**Characteristics:**
- Low latency (milliseconds to seconds)
- Continuous processing
- More complex (state management, late data, ordering)
- Higher infrastructure cost
- Suitable for real-time use cases

**Tools:** Apache Kafka, Apache Flink, Spark Structured Streaming, AWS Kinesis

### Batch vs Streaming Comparison

| Feature | Batch | Streaming |
|---|---|---|
| Latency | High (minutes–hours) | Low (ms–seconds) |
| Throughput | Very high | Medium–High |
| Complexity | Low | High |
| Cost | Lower | Higher |
| Data freshness | Stale | Near real-time |
| Use case | Reporting, ETL | Fraud detection, alerts |
| Error handling | Simple retry | Complex (exactly-once) |
| State management | Stateless | Stateful |

### Example Use Cases

| Use Case | Batch or Streaming |
|---|---|
| Nightly sales report | Batch |
| Fraud detection | Streaming |
| Monthly billing | Batch |
| Real-time dashboard | Streaming |
| Data warehouse load | Batch |
| IoT sensor monitoring | Streaming |
| Log aggregation | Both (Lambda Architecture) |

---

## 6. What is ETL vs ELT?

### ETL — Extract, Transform, Load

Data is **extracted** from source, **transformed** outside the destination (in a separate processing engine), then **loaded** into the target.

```
Source → [Extract] → Staging → [Transform] → [Load] → Data Warehouse
```

### ELT — Extract, Load, Transform

Data is **extracted** from source, **loaded** directly into the destination, then **transformed** inside the destination using its compute power.

```
Source → [Extract] → [Load] → Data Warehouse → [Transform inside DWH]
```

### ETL vs ELT Comparison

| Feature | ETL | ELT |
|---|---|---|
| Transform location | External engine | Inside destination |
| Raw data preserved | No | Yes |
| Flexibility | Lower | Higher |
| Cloud-native | No | Yes |
| Tools | Informatica, SSIS, Talend | dbt, Snowflake, BigQuery |
| Data volume | Smaller | Large scale |
| Latency | Higher | Lower |
| Best for | Legacy DWH, on-premise | Cloud DWH, modern stack |

### Modern ELT Stack Example

```
Source Systems
    ↓
Fivetran / Airbyte   (Extract + Load — raw data into warehouse)
    ↓
Snowflake / BigQuery (Raw data stored)
    ↓
dbt                  (Transform inside warehouse using SQL)
    ↓
BI Tools             (Tableau, Looker, Power BI)
```

---

## 7. What is Lambda Architecture?

**Lambda Architecture** is a data processing design pattern that handles both **batch and streaming** workloads simultaneously to balance latency, throughput, and fault tolerance.

### Three Layers

```
                    All Data
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
  BATCH LAYER                   SPEED LAYER
  (High latency,                (Low latency,
   accurate,                     approximate,
   reprocesses all data)         recent data only)
        ↓                             ↓
  SERVING LAYER ←──────────────────── ┘
  (Merges batch + speed results)
        ↓
     Query / BI
```

| Layer | Description | Tools |
|---|---|---|
| **Batch Layer** | Processes all historical data periodically | Spark, Hadoop |
| **Speed Layer** | Processes real-time data with low latency | Kafka Streams, Flink |
| **Serving Layer** | Merges batch and speed results for queries | Cassandra, HBase, Druid |

### Drawbacks of Lambda Architecture

- Maintaining **two separate codebases** (batch + streaming)
- Complex to debug and operate
- Data consistency issues between layers

---

## 8. What is Kappa Architecture?

**Kappa Architecture** simplifies Lambda by **eliminating the batch layer** — everything is processed as a stream.

Historical reprocessing is done by **replaying events** from the message queue (e.g., Kafka).

```
All Data → Message Queue (Kafka) → Stream Processor → Serving Layer → Query
                    ↑
          (Replay for reprocessing)
```

### Lambda vs Kappa

| Feature | Lambda | Kappa |
|---|---|---|
| Layers | Batch + Speed + Serving | Stream + Serving |
| Complexity | High | Lower |
| Reprocessing | Re-run batch jobs | Replay Kafka events |
| Code maintenance | Two codebases | One codebase |
| Best for | Mixed batch+stream needs | Streaming-first platforms |
| Tools | Spark + Kafka | Kafka + Flink |

---

## 9. What is Medallion Architecture?

**Medallion Architecture** (popularized by Databricks) organizes data into **three quality layers** — Bronze, Silver, and Gold.

```
Raw Sources → Bronze → Silver → Gold → BI / ML
```

### Layers Explained

| Layer | Also Called | Description | Data Quality |
|---|---|---|---|
| **Bronze** | Raw | Exact copy of source data | Low — raw, unvalidated |
| **Silver** | Cleaned | Filtered, deduplicated, standardized | Medium — trusted |
| **Gold** | Curated | Aggregated, business-level metrics | High — BI-ready |

### Bronze Layer

```python
# Load raw data as-is — no transformations
df_bronze = spark.read.json("s3://raw/events/")
df_bronze.write.format("delta").mode("append").save("s3://bronze/events/")
```

### Silver Layer

```python
# Clean and standardize
df_silver = df_bronze \
    .dropDuplicates(["event_id"]) \
    .filter(col("event_date").isNotNull()) \
    .withColumn("event_date", to_date(col("event_date")))

df_silver.write.format("delta").mode("overwrite").save("s3://silver/events/")
```

### Gold Layer

```python
# Aggregate for business consumption
df_gold = df_silver \
    .groupBy("region", "event_date") \
    .agg(count("event_id").alias("event_count"),
         sum("revenue").alias("total_revenue"))

df_gold.write.format("delta").mode("overwrite").save("s3://gold/daily_summary/")
```

---

## 10. What is Data Pipeline Design?

A **data pipeline** is a series of processes that move and transform data from source systems to destination systems.

### Pipeline Components

```
Ingestion → Validation → Transformation → Storage → Serving
```

| Component | Description | Tools |
|---|---|---|
| **Ingestion** | Extract data from sources | Kafka, Fivetran, Airbyte, custom APIs |
| **Validation** | Check data quality and schema | Great Expectations, dbt tests |
| **Transformation** | Clean, enrich, aggregate | Spark, dbt, Glue |
| **Storage** | Persist to destination | S3, Snowflake, Redshift, Delta Lake |
| **Serving** | Expose data to consumers | Athena, Redshift, REST APIs |
| **Orchestration** | Schedule and monitor jobs | Airflow, Prefect, Dagster |
| **Observability** | Monitor data quality and pipeline health | Monte Carlo, Datadog, custom |

### Idempotency in Pipelines

A pipeline is **idempotent** if running it multiple times produces the same result — critical for safe retries.

```python
# Idempotent write — overwrite partition instead of append
df.write \
  .mode("overwrite") \
  .partitionBy("date") \
  .parquet("s3://output/transactions/")
```

### Incremental vs Full Load

| Strategy | Description | Use Case |
|---|---|---|
| **Full load** | Reload entire dataset each run | Small tables, reference data |
| **Incremental** | Load only new/changed records | Large tables, transaction data |
| **CDC** | Capture only inserts/updates/deletes | Near real-time sync |

---

## 11. What is Pipeline Orchestration?

**Orchestration** is the scheduling, sequencing, and monitoring of data pipeline tasks and their dependencies.

### Apache Airflow

The most widely used orchestration tool — defines pipelines as **DAGs (Directed Acyclic Graphs)** in Python.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract(): pass
def transform(): pass
def load(): pass

with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 2 * * *",   # Daily at 2 AM
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="extract",   python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load",      python_callable=load)

    t1 >> t2 >> t3   # Define dependency order
```

### Orchestration Tools Comparison

| Tool | Language | Best For |
|---|---|---|
| **Apache Airflow** | Python | General-purpose, wide adoption |
| **Prefect** | Python | Modern, dynamic workflows |
| **Dagster** | Python | Data-aware, asset-based pipelines |
| **AWS Step Functions** | JSON/YAML | AWS-native serverless workflows |
| **dbt Cloud** | SQL | Transformation-only orchestration |
| **Azure Data Factory** | GUI + JSON | Azure-native ETL orchestration |

---

## 12. Data Modeling Concepts for DE Interviews

### Star Schema

Optimized for **analytical queries** — one central fact table surrounded by dimension tables.

```
         DIM_DATE
            │
DIM_REGION──FACT_SALES──DIM_PRODUCT
            │
        DIM_CUSTOMER
```

```sql
-- Typical star schema query
SELECT d.year, p.category, SUM(f.revenue) AS total_revenue
FROM FACT_SALES f
JOIN DIM_DATE    d ON f.date_key    = d.date_key
JOIN DIM_PRODUCT p ON f.product_key = p.product_key
GROUP BY d.year, p.category;
```

### Snowflake Schema

Extension of star schema where **dimension tables are normalized** into sub-dimensions.

- Reduces data redundancy
- More complex queries
- Less common in modern cloud DWH

### SCD — Slowly Changing Dimensions

Handles **historical changes** in dimension attributes.

| Type | Description | Example |
|---|---|---|
| **SCD Type 1** | Overwrite old value — no history | Fix a typo in a name |
| **SCD Type 2** | Add new row — full history preserved | Customer moves to new city |
| **SCD Type 3** | Add new column — limited history | Store previous + current value |

```sql
-- SCD Type 2 example
INSERT INTO DIM_CUSTOMER
SELECT
    customer_id,
    'New York'         AS city,
    CURRENT_DATE       AS effective_start,
    NULL               AS effective_end,
    TRUE               AS is_current
WHERE NOT EXISTS (
    SELECT 1 FROM DIM_CUSTOMER
    WHERE customer_id = :id AND is_current = TRUE AND city = 'New York'
);
```

---

## 13. Common Interview Questions & Answers

### Q: When would you choose a data lake over a data warehouse?

**Answer:**
Choose a **data lake** when:
- You need to store **unstructured or semi-structured data** (logs, images, JSON)
- Data consumers include **data scientists** who need raw data for ML
- You want **low-cost, flexible storage** and don't yet know all the use cases
- You need to **land data quickly** without defining a schema upfront

Choose a **data warehouse** when:
- All data is **structured and well-understood**
- Primary consumers are **business analysts** running SQL reports
- You need **fast, consistent query performance**
- Data quality and governance are critical

> In modern architectures, both are used together — data lake for raw storage, data warehouse for curated analytics.

---

### Q: What is the difference between OLTP and OLAP?

**Answer:**

| Feature | OLTP | OLAP |
|---|---|---|
| Purpose | Transactional operations | Analytical queries |
| Operations | INSERT, UPDATE, DELETE | SELECT, aggregations |
| Data volume | Small per query | Large scans |
| Schema | Normalized (3NF) | Denormalized (Star) |
| Response time | Milliseconds | Seconds to minutes |
| Examples | MySQL, PostgreSQL, Aurora | Redshift, Snowflake, BigQuery |

---

### Q: How do you handle late-arriving data in a pipeline?

**Answer:**
1. **Watermarking** (Structured Streaming) — define how late data can arrive before being dropped
2. **Reprocessing** — design pipelines to be rerunnable for a date range
3. **Upserts** — use Delta Lake / Iceberg MERGE to insert or update late records
4. **Event time vs processing time** — always use event time for business logic, processing time for monitoring

```python
# Watermark in Structured Streaming
df.withWatermark("event_time", "2 hours") \
  .groupBy(window("event_time", "1 hour")) \
  .count()
```

---

### Q: What makes a good data pipeline?

**Answer:**
A good data pipeline is:

- **Idempotent** — safe to rerun without duplicating data
- **Scalable** — handles growing data volumes without redesign
- **Fault-tolerant** — recovers from failures automatically
- **Observable** — logs, metrics, and alerts for monitoring
- **Incremental** — processes only new/changed data where possible
- **Testable** — unit and integration tests on transformations
- **Documented** — data lineage tracked, schemas documented

---

### Q: What is data lineage and why does it matter?

**Answer:**
**Data lineage** tracks the **origin, movement, and transformation** of data as it flows through a pipeline — from source to destination.

It matters because:
- **Debugging** — trace where incorrect data came from
- **Impact analysis** — understand what breaks if a source changes
- **Compliance** — prove data provenance for audits (GDPR, HIPAA)
- **Trust** — analysts trust data more when they can see where it came from

Tools: Apache Atlas, OpenLineage, dbt lineage graph, Marquez.

---

## 📌 Key Concepts Summary

| Concept | Description |
|---|---|
| **Data Lake** | Raw data storage — schema-on-read, all data types |
| **Data Warehouse** | Structured analytical storage — schema-on-write |
| **Data Mart** | Department-level subset of the data warehouse |
| **Data Lakehouse** | Combines lake flexibility with warehouse performance |
| **Batch Processing** | Periodic bulk data processing |
| **Streaming Processing** | Continuous real-time data processing |
| **ETL** | Transform before loading into destination |
| **ELT** | Load raw then transform inside destination |
| **Lambda Architecture** | Batch + streaming layers combined |
| **Kappa Architecture** | Streaming-only — replay for reprocessing |
| **Medallion Architecture** | Bronze → Silver → Gold quality layers |
| **Orchestration** | Schedule and manage pipeline dependencies |
| **SCD Type 2** | Track full history of dimension changes |
| **Idempotency** | Pipeline produces same result when run multiple times |
| **Data Lineage** | Track data origin and transformation history |

---

*These architecture fundamentals form the backbone of every Data Engineering interview — understanding the tradeoffs between each pattern is what separates strong candidates.*