# AWS Interview Preparation — S3 & Aurora (Data Engineer)

> A comprehensive guide covering AWS S3 and Amazon Aurora concepts, architecture, and best practices commonly asked in Data Engineering interviews.

---

## 📋 Topics Covered

- AWS S3 — Core Concepts
- S3 Storage Classes
- S3 Security & Access Control
- S3 Performance & Optimization
- S3 as a Data Lake
- S3 Event Notifications & Integrations
- Amazon Aurora — Core Concepts
- Aurora Architecture
- Aurora vs RDS vs Redshift
- Aurora in Data Platforms
- Common Interview Questions & Answers

---

## PART 1 — AWS S3

---

## 1. What is AWS S3?

**Amazon S3 (Simple Storage Service)** is a fully managed, scalable **object storage service** provided by AWS. It is designed to store and retrieve any amount of data from anywhere on the web.

S3 is one of the foundational services in AWS and is widely used as the backbone of **data lakes, backups, data pipelines, and static file hosting**.

### Key Characteristics

| Feature | Description |
|---|---|
| **Object storage** | Stores data as objects (file + metadata + unique key) |
| **Unlimited storage** | No cap on total data stored |
| **High durability** | 99.999999999% (11 nines) durability |
| **High availability** | 99.99% availability SLA |
| **Global access** | Accessible over HTTP/HTTPS from anywhere |
| **Fully managed** | No servers to provision or maintain |
| **Pay-as-you-go** | Charged per GB stored + requests made |

### S3 vs Traditional File Storage

| Feature | Traditional File Storage | AWS S3 |
|---|---|---|
| Structure | Hierarchical (folders) | Flat namespace (keys) |
| Scalability | Limited by hardware | Virtually unlimited |
| Access | Network file system | HTTP/HTTPS REST API |
| Management | User managed | Fully managed |
| Durability | Depends on setup | 11 nines durability |
| Cost model | Upfront hardware | Pay per use |

---

## 2. What are S3 Buckets?

An **S3 Bucket** is a container used to store objects in S3. Every object stored in S3 must reside inside a bucket.

### Bucket Characteristics

| Feature | Description |
|---|---|
| **Globally unique name** | Bucket names must be unique across all AWS accounts |
| **Region-specific** | Each bucket is created in a specific AWS region |
| **Flat structure** | No real folders — prefixes simulate directory structure |
| **Unlimited objects** | A bucket can hold an unlimited number of objects |
| **Max object size** | Single object can be up to 5 TB |

### S3 Object Structure

Every object in S3 consists of:

```
Bucket:    my-data-lake
Key:       raw/transactions/year=2024/month=01/transactions.parquet
Value:     (binary data — the actual file content)
Metadata:  Content-Type, Content-Length, custom tags, etc.
```

> The **key** is the full path of the object. S3 is flat — "folders" are just key prefixes.

### Creating a Bucket (AWS CLI)

```bash
# Create a bucket
aws s3 mb s3://my-data-lake-bucket --region us-east-1

# List all buckets
aws s3 ls

# Upload a file
aws s3 cp local_file.csv s3://my-data-lake-bucket/raw/local_file.csv

# Sync a folder
aws s3 sync ./local_folder s3://my-data-lake-bucket/raw/

# Delete an object
aws s3 rm s3://my-data-lake-bucket/raw/local_file.csv
```

### S3 Bucket Naming Rules

- 3 to 63 characters long
- Lowercase letters, numbers, and hyphens only
- Must start and end with a letter or number
- Cannot be formatted as an IP address (e.g., 192.168.1.1)

---

## 3. What are S3 Storage Classes?

S3 offers multiple **storage classes** optimized for different access patterns and cost requirements.

| Storage Class | Use Case | Availability | Retrieval Time | Cost |
|---|---|---|---|---|
| **S3 Standard** | Frequently accessed data | 99.99% | Milliseconds | Highest |
| **S3 Intelligent-Tiering** | Unknown or changing access patterns | 99.9% | Milliseconds | Auto-optimized |
| **S3 Standard-IA** | Infrequently accessed, rapid retrieval | 99.9% | Milliseconds | Lower storage |
| **S3 One Zone-IA** | Infrequent access, single AZ | 99.5% | Milliseconds | Lowest IA cost |
| **S3 Glacier Instant** | Archive, occasional access | 99.9% | Milliseconds | Very low |
| **S3 Glacier Flexible** | Long-term archive | 99.99% | Minutes to hours | Very low |
| **S3 Glacier Deep Archive** | Rarely accessed archive (7–10 years) | 99.99% | Up to 12 hours | Lowest |

### Lifecycle Policies

Lifecycle policies automatically **transition objects between storage classes** or **expire objects** after a defined period.

```json
{
  "Rules": [
    {
      "ID": "transition-to-glacier",
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30,  "StorageClass": "STANDARD_IA" },
        { "Days": 90,  "StorageClass": "GLACIER" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "Expiration": { "Days": 2555 }
    }
  ]
}
```

> **Common pattern for data lakes:** Hot data in Standard → 30 days to Standard-IA → 90 days to Glacier

---

## 4. S3 Security & Access Control

S3 provides multiple layers of security.

### 1. Bucket Policies

JSON-based policies attached to a bucket to control access.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::123456789:role/DataEngineerRole" },
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-data-lake-bucket/*"
    }
  ]
}
```

### 2. IAM Policies

Attached to IAM users, groups, or roles to grant S3 access.

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:ListBucket"],
  "Resource": [
    "arn:aws:s3:::my-data-lake-bucket",
    "arn:aws:s3:::my-data-lake-bucket/*"
  ]
}
```

### 3. S3 Block Public Access

A safety setting that blocks all public access to buckets and objects — **always enabled for data lakes**.

```bash
aws s3api put-public-access-block \
  --bucket my-data-lake-bucket \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### 4. Server-Side Encryption (SSE)

| Type | Description |
|---|---|
| **SSE-S3** | AWS manages keys automatically |
| **SSE-KMS** | AWS KMS manages keys — auditable, more control |
| **SSE-C** | Customer provides and manages their own keys |

```bash
# Upload with encryption
aws s3 cp file.csv s3://my-bucket/ --sse aws:kms --sse-kms-key-id <key-id>
```

### 5. VPC Endpoints

Allow S3 access from within a VPC **without going over the public internet** — important for secure data pipelines.

---

## 5. S3 Performance & Optimization

### Multipart Upload

For objects larger than **100 MB**, use multipart upload:
- Upload parts in parallel
- Resume failed uploads
- Required for objects over **5 GB**

```python
import boto3

s3 = boto3.client('s3')

s3.upload_file(
    Filename='large_file.parquet',
    Bucket='my-data-lake',
    Key='raw/large_file.parquet',
    Config=boto3.s3.transfer.TransferConfig(multipart_threshold=1024*25)
)
```

### S3 Transfer Acceleration

Routes uploads through AWS **CloudFront edge locations** — useful for uploading from geographically distant locations.

### Prefix Design for Performance

S3 scales based on **prefixes** — each prefix supports up to **3,500 PUT/COPY/POST/DELETE** and **5,500 GET/HEAD** requests per second.

```
# GOOD — different prefixes for parallel performance
s3://bucket/region=US/year=2024/
s3://bucket/region=EU/year=2024/
s3://bucket/region=APAC/year=2024/

# BAD — all objects under same prefix (bottleneck)
s3://bucket/data/data/data/
```

### S3 Select & Glacier Select

Query data directly inside S3 objects using SQL — avoids downloading entire files:

```python
response = s3.select_object_content(
    Bucket='my-data-lake',
    Key='raw/transactions.csv',
    ExpressionType='SQL',
    Expression="SELECT * FROM s3object WHERE amount > 1000",
    InputSerialization={'CSV': {'FileHeaderInfo': 'USE'}},
    OutputSerialization={'CSV': {}}
)
```

---

## 6. S3 as a Data Lake

S3 is the **most common foundation for cloud data lakes**, especially in AWS environments.

### Typical Data Lake Structure on S3

```
s3://my-data-lake/
├── raw/                        ← Exact copy of source data
│   ├── crm/
│   │   └── customers/year=2024/month=01/
│   └── erp/
│       └── orders/year=2024/month=01/
├── processed/                  ← Cleaned, transformed data
│   └── transactions/year=2024/
├── curated/                    ← Business-ready, aggregated data
│   └── daily_sales/
└── archive/                    ← Old data moved to Glacier
```

### File Formats for Data Lakes

| Format | Type | Best For |
|---|---|---|
| **Parquet** | Columnar | Analytics, Spark, Athena |
| **ORC** | Columnar | Hive, Presto |
| **Avro** | Row-based | Streaming, schema evolution |
| **Delta Lake** | Columnar + ACID | Databricks, transactional lakes |
| **Iceberg** | Columnar + ACID | AWS Athena, Spark |
| **CSV/JSON** | Row-based | Raw ingestion only |

> **Best practice:** Store raw data as-is (CSV/JSON), convert to Parquet for processed and curated layers.

### AWS Services That Integrate with S3

| Service | Purpose |
|---|---|
| **AWS Glue** | ETL and data catalog |
| **Amazon Athena** | Serverless SQL on S3 |
| **Amazon EMR** | Spark/Hadoop on S3 |
| **AWS Lambda** | Event-driven processing on S3 events |
| **Amazon Redshift Spectrum** | Query S3 data from Redshift |
| **AWS Lake Formation** | Govern and secure data lakes on S3 |
| **Snowflake** | External stages pointing to S3 |

---

## 7. S3 Event Notifications

S3 can trigger events when objects are created, deleted, or restored — enabling **event-driven data pipelines**.

### Supported Destinations

| Destination | Use Case |
|---|---|
| **AWS Lambda** | Trigger data processing on file arrival |
| **Amazon SQS** | Queue events for batch processing |
| **Amazon SNS** | Fan-out notifications to multiple consumers |
| **Amazon EventBridge** | Advanced routing and filtering |

### Example — Trigger Lambda on File Upload

```json
{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123:function:ProcessFile",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            { "Name": "prefix", "Value": "raw/" },
            { "Name": "suffix", "Value": ".parquet" }
          ]
        }
      }
    }
  ]
}
```

---

## PART 2 — Amazon Aurora

---

## 8. What is Amazon Aurora?

**Amazon Aurora** is a fully managed **relational database engine** built by AWS that is compatible with **MySQL and PostgreSQL**.

It combines the **performance and availability of commercial databases** (like Oracle) with the **simplicity and cost-effectiveness of open-source databases**.

### Key Characteristics

| Feature | Description |
|---|---|
| **MySQL compatible** | Drop-in replacement for MySQL 5.7 / 8.0 |
| **PostgreSQL compatible** | Drop-in replacement for PostgreSQL 13/14/15 |
| **5x faster than MySQL** | AWS claims up to 5x MySQL performance |
| **3x faster than PostgreSQL** | AWS claims up to 3x PostgreSQL performance |
| **Fully managed** | Automated backups, patching, failover |
| **High availability** | 6 copies of data across 3 Availability Zones |
| **Auto-scaling storage** | Grows automatically from 10 GB to 128 TB |

---

## 9. Aurora Architecture

Aurora's architecture is fundamentally different from standard RDS.

```
┌──────────────────────────────────────────────┐
│              AURORA CLUSTER                  │
│                                              │
│  ┌─────────────┐      ┌──────────────────┐  │
│  │   PRIMARY   │      │  READ REPLICAS   │  │
│  │  (Writer)   │      │  (up to 15)      │  │
│  └──────┬──────┘      └────────┬─────────┘  │
│         │                      │            │
│         └──────────┬───────────┘            │
│                    │                        │
│         ┌──────────▼───────────┐            │
│         │   SHARED STORAGE     │            │
│         │  6 copies across     │            │
│         │  3 Availability Zones│            │
│         │  Auto-scales to 128TB│            │
│         └──────────────────────┘            │
└──────────────────────────────────────────────┘
```

### Aurora Storage Layer

Unlike traditional RDS where each instance has its own storage:

- Aurora uses a **shared distributed storage layer**
- Data is replicated **6 times across 3 AZs automatically**
- Storage automatically grows in **10 GB increments**
- Reads and writes go through the shared storage — replicas are not replication lag-heavy

### Aurora Endpoints

| Endpoint | Description | Use Case |
|---|---|---|
| **Cluster endpoint** | Always points to the primary (writer) | INSERT, UPDATE, DELETE |
| **Reader endpoint** | Load-balances across all read replicas | SELECT queries |
| **Instance endpoint** | Direct connection to a specific instance | Debugging, maintenance |
| **Custom endpoint** | Points to a subset of instances | Workload isolation |

---

## 10. Aurora Features

### Auto-Scaling Read Replicas

Aurora can automatically add or remove read replicas based on CPU or connection metrics.

```json
{
  "MinCapacity": 1,
  "MaxCapacity": 15,
  "TargetValue": 70.0,
  "PredefinedMetricType": "RDSReaderAverageCPUUtilization"
}
```

### Aurora Serverless

**Aurora Serverless** automatically starts, scales, and shuts down based on application demand.

| Feature | Aurora Provisioned | Aurora Serverless v2 |
|---|---|---|
| Capacity | Fixed instance size | Scales in fractions of ACU |
| Billing | Per instance-hour | Per ACU-second |
| Cold start | No | Near-instant (v2) |
| Use case | Steady workloads | Variable / unpredictable workloads |

### Aurora Global Database

Spans **multiple AWS regions** — provides:
- Low-latency global reads
- Disaster recovery across regions
- RPO of seconds, RTO under 1 minute

### Automated Backups & Point-In-Time Recovery

```
Retention period: 1–35 days
Backup window:    Automated daily snapshots
PITR:             Restore to any second within retention period
```

---

## 11. Why is Aurora Used in Data Platforms?

Aurora is commonly used in data platforms for several roles:

### 1. Metadata Store

Stores metadata for data pipelines — job configs, table schemas, run history.

```sql
-- Example metadata table in Aurora
CREATE TABLE pipeline_runs (
    run_id          SERIAL PRIMARY KEY,
    pipeline_name   VARCHAR(200),
    start_time      TIMESTAMP,
    end_time        TIMESTAMP,
    status          VARCHAR(50),
    records_loaded  BIGINT,
    error_message   TEXT
);
```

### 2. Configuration Database

Stores dynamic configuration for ETL jobs — source credentials, transformation rules, schedules.

### 3. Operational Data Store (ODS)

Stores near-real-time operational data before it flows into the data warehouse.

### 4. Airflow Metadata Database

**Apache Airflow** uses a relational database as its backend — Aurora PostgreSQL is a common production choice.

```
Airflow → Aurora PostgreSQL (metadata DB)
       → stores DAG definitions, task states, logs
```

### 5. Glue Data Catalog Backend

AWS Glue can use Aurora as a **Hive Metastore** for storing table and schema metadata.

### 6. Application Database for Data Products

Powers APIs and web applications that serve data products built from the data warehouse.

---

## 12. Aurora vs RDS vs Redshift

| Feature | Amazon RDS | Amazon Aurora | Amazon Redshift |
|---|---|---|---|
| Type | Relational (OLTP) | Relational (OLTP) | Columnar (OLAP) |
| Compatibility | MySQL, PG, Oracle, MSSQL | MySQL, PostgreSQL | PostgreSQL-like SQL |
| Performance | Standard | 5x MySQL, 3x PG | Optimized for analytics |
| Storage | Instance-attached | Shared, distributed | Columnar, compressed |
| Scaling | Vertical | Read replicas + Serverless | Node-based clusters |
| Use case | Application DB | High-perf application DB | Data warehouse |
| Availability | Multi-AZ | 6 copies, 3 AZs | Multi-node clusters |
| Best for | Transactional apps | High-scale transactional | Analytical queries |

---

## 13. Common Interview Questions & Answers

### Q: What is the difference between S3 and EBS (Elastic Block Store)?

**Answer:**

| Feature | S3 | EBS |
|---|---|---|
| Type | Object storage | Block storage |
| Access | Over HTTP/HTTPS | Attached to EC2 instance |
| Use case | Data lakes, backups, static files | OS volumes, databases |
| Durability | 11 nines | 99.8–99.9% |
| Persistence | Independent of EC2 | Tied to instance lifecycle |
| Max size | Unlimited | 64 TB per volume |

---

### Q: How do you secure data in S3?

**Answer:** Multiple layers:
1. **Block Public Access** — prevent accidental public exposure
2. **Bucket Policies** — control which accounts/roles can access
3. **IAM Policies** — grant least-privilege to users and roles
4. **Server-Side Encryption (SSE-KMS)** — encrypt data at rest
5. **SSL/TLS** — encrypt data in transit
6. **VPC Endpoints** — keep traffic off the public internet
7. **S3 Access Logs** — audit who accessed what and when
8. **AWS Macie** — detect sensitive data stored in S3

---

### Q: What is S3 versioning and when would you use it?

**Answer:**
S3 versioning keeps **multiple versions of an object** in the same bucket. When enabled:
- Every overwrite creates a new version
- Deleted objects get a delete marker (not permanently deleted)
- Previous versions can be restored

Use cases: protect against accidental deletes, audit trails, compliance requirements.

```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled
```

---

### Q: What is the difference between Aurora and standard RDS?

**Answer:**
- Aurora uses a **shared distributed storage layer** replicated 6 times across 3 AZs — standard RDS uses instance-attached storage
- Aurora storage **auto-scales** up to 128 TB — RDS requires manual storage provisioning
- Aurora has **faster failover** (typically under 30 seconds) — RDS Multi-AZ failover takes 1–2 minutes
- Aurora supports up to **15 read replicas** — RDS supports up to 5
- Aurora is **more expensive** but significantly higher performance and availability

---

### Q: How would you design an S3-based data lake for a high-volume pipeline?

**Answer:**

```
s3://data-lake/
├── raw/          ← Landing zone, CSV/JSON, partitioned by source + date
├── processed/    ← Parquet, cleaned, partitioned by business date
└── curated/      ← Aggregated Parquet, optimized for BI queries

Key decisions:
1. Use Parquet with Snappy compression for processed/curated layers
2. Partition by date (year/month/day) for query pruning
3. Use S3 lifecycle policies to archive raw data after 90 days
4. Enable SSE-KMS encryption on all buckets
5. Use S3 event notifications → Lambda → trigger Glue/EMR for processing
6. Register tables in Glue Data Catalog for Athena/Redshift Spectrum access
```

---

### Q: When would you choose Aurora Serverless over Aurora Provisioned?

**Answer:**
Choose **Aurora Serverless** when:
- Traffic is **unpredictable or sporadic** (e.g., dev/test environments, reporting tools used occasionally)
- You want to **avoid paying for idle capacity**
- Workloads have significant peaks and valleys

Choose **Aurora Provisioned** when:
- Traffic is **steady and predictable**
- You need **maximum performance** (no cold start risk)
- Running **production OLTP workloads** with consistent high throughput

---

## 📌 Key Concepts Summary

| Concept | Description |
|---|---|
| **S3 Bucket** | Container for storing objects — globally unique name |
| **S3 Object** | Data unit — file + key + metadata |
| **Storage Classes** | Tiered storage options based on access frequency |
| **Lifecycle Policy** | Auto-transition or expire objects over time |
| **S3 Versioning** | Keep multiple versions of objects |
| **SSE-KMS** | Encryption at rest using AWS Key Management Service |
| **S3 Select** | SQL queries directly on S3 objects |
| **S3 Event Notifications** | Trigger Lambda/SQS/SNS on object events |
| **Aurora** | High-performance managed MySQL/PostgreSQL compatible DB |
| **Shared Storage** | Aurora's distributed storage — 6 copies across 3 AZs |
| **Aurora Serverless** | Auto-scaling Aurora for variable workloads |
| **Aurora Global DB** | Multi-region Aurora for global apps and DR |
| **Reader Endpoint** | Load-balanced endpoint across Aurora read replicas |

---

*Mastering S3 and Aurora is essential for any AWS Data Engineering role — they form the storage backbone of nearly every modern cloud data platform.*