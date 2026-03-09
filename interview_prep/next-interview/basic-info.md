# Data Engineer – Next Interview Preparation

This document contains all the topics, concepts, and project explanations I need to master before my next Data Engineering interview.

The preparation focuses on:
- SQL
- Snowflake
- PySpark
- Data Vault 2.0
- AWS Services
- Data Engineering Architecture
- Insurance Domain Knowledge
- DataOps (GitHub + Jenkins)
- Behavioral Questions

---

# 1. Current Project (Enterprise Insurance Data Platform)

## Domain
Insurance (Policy, Coverage, Transaction)

## Data Warehouse
Snowflake

## Architecture
Data Vault 2.0

## Data Volume
Hundreds of millions of records  
Example: 300M+ policy and transaction records from 2020–2026.

---

## High Level Architecture

Source Systems  
↓  
Data Lake (likely AWS S3)  
↓  
Snowflake Data Warehouse  
↓  
Raw Vault (Data Vault 2.0)  
↓  
Business Vault  
↓  
Data Mart / Reporting

---

## My Responsibilities

- Convert business transformation logic from **STTM documents** into optimized SQL queries.
- Implement transformations in **Snowflake SQL**.
- Work with **Data Vault 2.0 architecture** including Raw Vault and Business Vault.
- Commit SQL scripts to **GitHub**.
- Deploy pipelines using **Jenkins CI/CD pipelines**.
- Configure batch data loading jobs in **Aurora metadata database**.
- Execute data loading jobs for different subject areas (Policy, Coverage, Transaction).
- Monitor job execution and troubleshoot failures using **DBeaver**.
- Test pipelines across multiple environments:  
  DEV → QA → UAT → PROD.

---

## Data Loading Workflow

1. Functional team provides **STTM transformation logic**.
2. Data engineers convert logic into **Snowflake SQL transformations**.
3. SQL code committed to **GitHub repository**.
4. **Jenkins pipeline** deploys SQL code to Snowflake.
5. Job configuration stored in **Aurora metadata database**.
6. Jobs triggered to load data:

Data Lake → Raw Vault  
Raw Vault → Business Vault

7. Data validation and job monitoring performed through database tools.

---

# 2. SQL (Critical Interview Skill)

## Core SQL
- Joins (Inner, Left, Right, Full)
- Aggregations
- Subqueries
- CTE (Common Table Expressions)

## Advanced SQL
- Window Functions
- Ranking functions:
  - ROW_NUMBER
  - RANK
  - DENSE_RANK
- Running totals
- Deduplication logic
- Top N per group queries
- Conditional aggregation

## Data Engineering SQL Problems
- Latest record per key
- Incremental loading
- Change detection
- SCD Type 1 / Type 2
- Handling duplicates

## Performance Concepts
- Query execution plan
- Partition pruning
- Clustering
- Reducing scans

---

# 3. Snowflake

## Core Concepts
- Virtual Warehouses
- Micro-partitions
- Query optimization
- Clustering keys

## Snowflake Features
- Time Travel
- Zero Copy Cloning
- Streams
- Tasks
- Snowpipe
- Data sharing

## Snowflake Performance
- Warehouse sizing
- Query pruning
- Clustering strategies
- Handling large tables

---

# 4. PySpark / Spark

## Core Concepts
- RDD vs DataFrame
- Lazy evaluation
- DAG execution

## Transformations
- Narrow vs Wide transformations
- Shuffle operations

## Performance Optimization
- Partitioning
- Repartition vs Coalesce
- Broadcast joins
- Handling data skew

## Spark Internals
- Catalyst Optimizer
- Tungsten Engine
- Execution plan analysis

---

# 5. Data Vault 2.0 (Important)

## Core Components

### Hub
Stores business keys.

Example:
Policy ID

### Link
Represents relationships between hubs.

Example:
Policy ↔ Customer

### Satellite
Stores descriptive attributes and history.

Example:
Policy attributes, transaction details.

---

## Advantages of Data Vault

- Highly scalable
- Supports historical tracking
- Parallel loading
- Flexible schema evolution

---

## Data Vault Layers

Raw Vault  
Business Vault  
Data Mart

---

# 6. AWS Components

## AWS S3

Object storage used as Data Lake.

Key Concepts:
- Buckets
- Objects
- Data storage for raw datasets
- Integration with analytics platforms

---

## AWS Aurora

Used as **metadata store** for:

- Job configurations
- Job IDs
- Execution logic
- Framework control tables

Aurora is **not used for data warehouse workloads**.

---

# 7. DataOps (GitHub + Jenkins)

## GitHub

Used for:
- Version control
- Code collaboration
- Managing SQL scripts

Concepts:
- Branching
- Pull Requests
- Code reviews

---

## Jenkins

Used for:
- CI/CD automation
- Deploying SQL scripts to Snowflake
- Managing build pipelines
- Environment promotion

Example pipeline flow:

GitHub → Jenkins → Snowflake deployment

---

# 8. Insurance Domain Knowledge

## Key Entities

### Policy
Contract between insurer and policyholder.

### Coverage
Defines risks covered by policy.

### Transaction
Financial activity related to policy.

Examples:
- Premium payments
- Adjustments
- Endorsements

---

## Additional Insurance Concepts

- Underwriting
- Claims processing
- Premium calculation
- Risk assessment

---

# 9. Architecture Questions (Common in Interviews)

Examples:

Explain your project architecture.

Difference between:
- Data Lake
- Data Warehouse
- Data Mart

When to use:
- Data Vault
- Star Schema
- Medallion Architecture

Explain batch vs streaming pipelines.

---

# 10. Behavioral Questions

Examples:

Tell me about your project.

What challenges did you face?

How do you debug a failed pipeline?

How do you handle production issues?

Describe a time you optimized a query or pipeline.

---

# 11. Practice Areas

Before interviews ensure confidence in:

- SQL window functions
- Query optimization
- Data modeling
- Spark fundamentals
- Snowflake internals
- Explaining project architecture

---

# Goal

Become confident explaining:

1. My project architecture
2. SQL problem solving
3. Data engineering system design
4. Domain understanding
5. Cloud data platform concepts
