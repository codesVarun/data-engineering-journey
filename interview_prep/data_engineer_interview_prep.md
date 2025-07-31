# Data Engineer Interview Questions and Answers

## Snowflake Related

### 1. How is data ingested in Snowflake?
- Snowpipe (auto-ingest)
- COPY command (bulk load)
- Snowflake Connector for Python/Spark
- External stage (S3, Azure Blob, GCS)

### 2. What is the stage area?
- Temporary location for storing files before loading into tables.
- Types: Internal Stage (`@mytable`), External Stage (e.g., S3 bucket).

### 3. How do we handle incremental load in Snowflake?
- Use watermarks or timestamps.
- Query new/updated records only.
- Use `MERGE INTO` for upserts.

### 4. Features of Snowflake?
- Auto-scaling, Auto-suspend
- Zero-copy cloning, Time Travel
- Secure data sharing
- Semi-structured data support (JSON, Avro, Parquet)
- Snowpipe for real-time ingestion

### 5. How are you scheduling the jobs?
- Snowflake Tasks
- Airflow, dbt Cloud
- Cron jobs or shell scripts

### 6. Performance Improvement Techniques?
- Clustering keys, partition pruning
- Result caching
- Query optimization (avoid `SELECT *`)
- Materialized views

### 7. How to get data insights?
- BI tools (Tableau, Power BI)
- SQL aggregations
- `INFORMATION_SCHEMA`, `QUERY_HISTORY`

### 8. Features of Snowflake over Redshift?
- Separation of storage/compute
- Instant scaling, zero-copy cloning
- Time Travel, better semi-structured support
- Native Snowpipe

### 9. Query: Unique customers who placed orders
```sql
SELECT DISTINCT customer_id FROM orders;
```

### 10. Query: Customers who ordered more than 5 times
```sql
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

## Leadership & Team

### Do you have experience in leading a team?
Yes. Led a team of X engineers, managed deliverables, code reviews, and stakeholder communication.

## Unix & Shell Scripting

### I have 1000 tables to move in Unix. How?
- Use `scp`/`rsync`
- Automate via shell script
- Validate via row count, checksums

### Have you written shell scripts? Use case?
Yes. For:
- Ingestion to S3
- Data archiving
- Job scheduling
- Logging

## Scheduling & Automation

### How to schedule cloning of prod tables?
- Use Snowflake Tasks + `CREATE TABLE xyz CLONE abc;`
- Or Airflow/shell + cron

## Performance Tuning

### Snowflake query is slow. Fix?
- Query profile analysis
- Clustering keys, filters
- Caching, avoid `SELECT *`

### Spark job is slow. Fix?
- Partition tuning, broadcast joins
- Cache reused datasets
- Avoid shuffles

## Migration & Conversion

### Worked on migration project? Format?
Yes. CSV, JSON, Parquet (preferred)

### File format conversion: Shell or Python?
- Shell: `awk`, `sed`, `tr`
- Python: Pandas, PySpark

## Project Understanding

### Current project architecture?
Example:
- Source: Kafka/CSV/REST API
- Processing: Spark on EMR
- Storage: Snowflake
- Orchestration: Airflow
- BI: Power BI/Tableau

### Data format landing into AWS?
Parquet, JSON, Avro (structured or semi-structured)

### Roles and responsibilities?
- Ingestion, pipeline design
- Transformation logic
- Query optimization
- Monitoring

## Scenario-Based

### Recover data for last 3 days?
Use Snowflake Time Travel:
```sql
SELECT * FROM my_table AT(TIMESTAMP => '2025-07-28 00:00:00');
```
Or use `UNDROP TABLE`.

### Monitor important tables?
- `TABLE_STORAGE_METRICS`
- Snowflake Task + Alerts
- Row count, null checks

### Worked on Snowpark?
Yes/No. Snowpark enables Python/Scala/Java code execution in Snowflake, useful for:
- UDF logic
- DataFrame APIs
- In-Snowflake ML inference