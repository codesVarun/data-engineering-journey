# Data Vault 2.0 Interview Preparation (Data Engineer)

> A comprehensive guide covering Data Vault 2.0 concepts, architecture, components, and best practices commonly asked in Data Engineering interviews.

---

## 📋 Topics Covered

- What is Data Vault 2.0
- Core Components (Hub, Link, Satellite)
- Raw Vault vs Business Vault
- Data Vault Architecture
- Loading Patterns & Best Practices
- Point-In-Time (PIT) Tables
- Bridge Tables
- Data Vault vs Other Modeling Techniques
- Data Vault on Cloud & Modern Platforms
- Common Interview Questions & Answers

---

## 1. What is Data Vault?

Data Vault is a **detail-oriented, historical tracking, and uniquely linked set of normalized tables** that support one or more functional areas of business.

It was designed by **Dan Linstedt** in the 1990s and formalized as **Data Vault 2.0** to address modern cloud, big data, and agile requirements.

### Why Data Vault?

Traditional modeling approaches like Star Schema and NF struggle with:

- Frequent source system changes
- Auditing and traceability requirements
- Parallel data loading
- Integrating data from many source systems

Data Vault solves all of these.

### Key Design Principles

| Principle                  | Description                                               |
| -------------------------- | --------------------------------------------------------- |
| **Auditability**           | Every record tracks source system and load timestamp      |
| **Scalability**            | Parallel loading — no foreign key constraints during load |
| **Flexibility**            | New sources added without redesigning existing structures |
| **History tracking**       | Full history preserved — nothing is deleted               |
| **Separation of concerns** | Raw data kept separate from business rules                |

### Data Vault 2.0 vs Data Vault 1.0

| Feature              | Data Vault 1.0 | Data Vault 2.0                |
| -------------------- | -------------- | ----------------------------- |
| Cloud support        | Limited        | Native cloud support          |
| NoSQL support        | No             | Yes                           |
| Agile methodology    | Partial        | Fully embedded                |
| Big data integration | No             | Yes                           |
| Real-time loading    | Limited        | Supported                     |
| Business rules       | Mixed in       | Separated into Business Vault |

---

## 2. What are the Main Components of Data Vault?

Data Vault has **three core structural components**:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│     HUB     │◄────────│    LINK     │────────►│     HUB     │
│ Business Key│         │Relationship │         │ Business Key│
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
┌──────▼──────┐         ┌──────▼──────┐         ┌──────▼──────┐
│  SATELLITE  │         │  SATELLITE  │         │  SATELLITE  │
│  Attributes │         │  Attributes │         │  Attributes │
└─────────────┘         └─────────────┘         └─────────────┘
```

| Component     | Purpose                                   | Contains                        |
| ------------- | ----------------------------------------- | ------------------------------- |
| **Hub**       | Stores unique business keys               | Business key + metadata         |
| **Link**      | Stores relationships between hubs         | Foreign keys to hubs + metadata |
| **Satellite** | Stores descriptive attributes and history | Attributes + timestamps         |

---

## 3. What is a Hub?

A **Hub** stores the **unique list of business keys** for a core business concept.

It represents the "what" of the business — a customer, a policy, a product.

### Hub Structure

| Column            | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `HUB_[ENTITY]_HK` | Hash key — surrogate key derived from business key     |
| `LOAD_DATE`       | Timestamp when record was first loaded                 |
| `RECORD_SOURCE`   | Source system that provided the record                 |
| `[BUSINESS_KEY]`  | The actual business key (e.g., policy_id, customer_id) |

### Example — Hub for Policy

```sql
CREATE TABLE HUB_POLICY (
    HUB_POLICY_HK       BINARY(16)      NOT NULL,  -- MD5/SHA hash of POLICY_ID
    LOAD_DATE           TIMESTAMP       NOT NULL,
    RECORD_SOURCE       VARCHAR(100)    NOT NULL,
    POLICY_ID           VARCHAR(50)     NOT NULL,
    CONSTRAINT PK_HUB_POLICY PRIMARY KEY (HUB_POLICY_HK)
);
```

### Hub Rules

- Contains **only the business key** — no descriptive attributes
- Each business key appears **only once** (deduplicated)
- Never updated — only inserts
- Hash key is derived from the business key using MD5 or SHA-256

### Hash Key Generation

```sql
-- Snowflake example
SELECT MD5(UPPER(TRIM(POLICY_ID))) AS HUB_POLICY_HK
FROM SOURCE_POLICIES;
```

---

## 4. What is a Link?

A **Link** stores **relationships and associations between two or more Hubs**.

It represents the "interaction" or "transaction" between business concepts.

### Link Structure

| Column           | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `LINK_[NAME]_HK` | Hash key of the link — derived from all connected hub keys |
| `LOAD_DATE`      | Timestamp when relationship was first loaded               |
| `RECORD_SOURCE`  | Source system                                              |
| `HUB_[A]_HK`     | Foreign key to Hub A                                       |
| `HUB_[B]_HK`     | Foreign key to Hub B                                       |

### Example — Link between Policy and Customer

```sql
CREATE TABLE LINK_POLICY_CUSTOMER (
    LINK_POLICY_CUSTOMER_HK     BINARY(16)   NOT NULL,
    LOAD_DATE                   TIMESTAMP    NOT NULL,
    RECORD_SOURCE               VARCHAR(100) NOT NULL,
    HUB_POLICY_HK               BINARY(16)   NOT NULL,
    HUB_CUSTOMER_HK             BINARY(16)   NOT NULL,
    CONSTRAINT PK_LINK_POLICY_CUSTOMER PRIMARY KEY (LINK_POLICY_CUSTOMER_HK)
);
```

### Link Rules

- Links are **immutable** — relationships are never deleted
- A link can connect **two or more hubs** (hierarchical links)
- The link hash key is derived from **all participating hub hash keys**
- No descriptive attributes stored in the link itself (those go in a Link Satellite)

### Types of Links

| Type                    | Description                    | Example                     |
| ----------------------- | ------------------------------ | --------------------------- |
| **Standard Link**       | Two-way relationship           | Policy ↔ Customer           |
| **Hierarchical Link**   | Self-referencing relationship  | Employee ↔ Manager          |
| **Same-As Link**        | Deduplication of business keys | CRM customer ↔ ERP customer |
| **Non-Historized Link** | Current-state only, no history | Real-time transaction link  |

---

## 5. What is a Satellite?

A **Satellite** stores all **descriptive attributes, context, and historical changes** for a Hub or Link.

It is the only component in Data Vault that stores historical records.

### Satellite Structure

| Column               | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `HUB/LINK_[NAME]_HK` | Foreign key to parent Hub or Link                      |
| `LOAD_DATE`          | Timestamp when this version was loaded                 |
| `LOAD_END_DATE`      | Timestamp when this version became inactive (nullable) |
| `RECORD_SOURCE`      | Source system                                          |
| `HASH_DIFF`          | Hash of all attributes — used to detect changes        |
| `[ATTRIBUTES]`       | Descriptive columns (name, address, status, etc.)      |

### Example — Satellite for Customer

```sql
CREATE TABLE SAT_CUSTOMER_DETAILS (
    HUB_CUSTOMER_HK     BINARY(16)      NOT NULL,
    LOAD_DATE           TIMESTAMP       NOT NULL,
    LOAD_END_DATE       TIMESTAMP,
    RECORD_SOURCE       VARCHAR(100)    NOT NULL,
    HASH_DIFF           BINARY(16)      NOT NULL,
    CUSTOMER_NAME       VARCHAR(200),
    EMAIL               VARCHAR(200),
    PHONE               VARCHAR(50),
    ADDRESS             VARCHAR(500),
    STATUS              VARCHAR(50),
    CONSTRAINT PK_SAT_CUSTOMER PRIMARY KEY (HUB_CUSTOMER_HK, LOAD_DATE)
);
```

### Satellite Rules

- New record inserted **every time an attribute changes**
- Old records are **never deleted or updated**
- `HASH_DIFF` avoids loading duplicate records (only load if attributes changed)
- One Hub or Link can have **multiple Satellites** (split by rate of change or source system)

### Splitting Satellites

Satellites should be split when:

- Attributes come from **different source systems**
- Attributes have **different rates of change** (e.g., slowly changing vs frequently changing)
- Attributes belong to **different subject areas**

```
HUB_CUSTOMER
    ├── SAT_CUSTOMER_CRM        (from CRM system)
    ├── SAT_CUSTOMER_ERP        (from ERP system)
    └── SAT_CUSTOMER_SOCIAL     (from social media)
```

---

## 6. What is the Raw Vault?

The **Raw Vault** stores data **exactly as received from source systems** — no transformations, no business rules applied.

### Characteristics

| Feature            | Description                              |
| ------------------ | ---------------------------------------- |
| No transformations | Data loaded as-is from source            |
| Full history       | Every version of every record is kept    |
| Audit trail        | Full traceability back to source         |
| Source-aligned     | Structure mirrors source system concepts |
| Insert-only        | No updates or deletes                    |

### Raw Vault Loading Pattern

```
Source Systems
      ↓
  Staging Area   (temporary, truncated each load)
      ↓
  Raw Vault      (permanent, insert-only, no business rules)
      ↓
Business Vault   (transformations, business rules applied)
      ↓
Information Mart (Star Schema / flat tables for consumption)
```

---

## 7. What is the Business Vault?

The **Business Vault** contains data that has had **business rules, transformations, and computations** applied to it.

It sits between the Raw Vault and the Information Mart.

### Examples of Business Vault Objects

| Object             | Description                                      |
| ------------------ | ------------------------------------------------ |
| Computed Satellite | Derived calculations (e.g., age from birth date) |
| Business rule Hub  | Unified business keys from multiple sources      |
| Same-As Link       | Resolved duplicate entities                      |
| Exploration Link   | Relationships derived from business logic        |

### Raw Vault vs Business Vault

| Feature          | Raw Vault           | Business Vault              |
| ---------------- | ------------------- | --------------------------- |
| Source data      | Exact copy          | Transformed                 |
| Business rules   | None                | Applied                     |
| Purpose          | Audit, traceability | Analytics, reporting        |
| Naming           | Source-aligned      | Business-aligned            |
| Change frequency | Rarely changes      | Changes with business rules |

---

## 8. What are Hash Keys and Why Are They Used?

A **Hash Key (HK)** is a surrogate key in Data Vault, generated by applying a **hash function (MD5 or SHA-256)** to the business key.

### Why Hash Keys?

| Reason                 | Explanation                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| **Parallel loading**   | Hash can be computed independently — no sequence generator needed        |
| **Cross-system joins** | Same business key produces same hash across systems                      |
| **Performance**        | Fixed-length binary key is faster for joins than variable-length strings |
| **Deterministic**      | Same input always produces same hash — no lookup required                |

### Hash Key Generation Rules

```sql
-- Normalize before hashing: UPPER, TRIM, handle NULLs
SELECT MD5(UPPER(TRIM(COALESCE(POLICY_ID, 'NULL')))) AS HUB_POLICY_HK
FROM STAGING_POLICIES;
```

### MD5 vs SHA-256

| Feature        | MD5                | SHA-256             |
| -------------- | ------------------ | ------------------- |
| Output size    | 128-bit (16 bytes) | 256-bit (2 bytes)   |
| Collision risk | Higher             | Lower               |
| Performance    | Faster             | Slightly slower     |
| Recommended    | Legacy systems     | New implementations |

> **Data Vault 2.0 recommends SHA-256** for new implementations.

---

## 9. What is a Point-In-Time (PIT) Table?

A **PIT (Point-In-Time) table** is a performance optimization structure that stores the **latest Satellite hash keys and load dates** for a given Hub at each point in time.

### Problem It Solves

When a Hub has multiple Satellites, joining them all to get a snapshot at a specific time requires complex queries with multiple `MAX(LOAD_DATE)` subqueries — very slow.

### PIT Table Structure

```sql
CREATE TABLE PIT_CUSTOMER (
    HUB_CUSTOMER_HK             BINARY(16)   NOT NULL,
    SNAPSHOT_DATE               DATE         NOT NULL,
    SAT_CUSTOMER_DETAILS_HK     BINARY(16),
    SAT_CUSTOMER_DETAILS_LDTS   TIMESTAMP,
    SAT_CUSTOMER_CRM_HK         BINARY(16),
    SAT_CUSTOMER_CRM_LDTS       TIMESTAMP,
    CONSTRAINT PK_PIT_CUSTOMER PRIMARY KEY (HUB_CUSTOMER_HK, SNAPSHOT_DATE)
);
```

### Benefits

- Dramatically improves query performance on multi-satellite hubs
- Pre-computes the "latest as-of" satellite records
- Simplifies downstream query logic

---

## 10. What is a Bridge Table?

A **Bridge Table** is a performance optimization structure that **pre-joins multiple Links and Hubs** into a flat structure.

### Problem It Solves

Traversing multiple links and hubs to answer a business question requires many joins — expensive at query time.

### Bridge Table Example

```sql
CREATE TABLE BRIDGE_POLICY_CUSTOMER_AGENT (
    HUB_POLICY_HK       BINARY(16),
    HUB_CUSTOMER_HK     BINARY(16),
    HUB_AGENT_HK        BINARY(16),
    SNAPSHOT_DATE       DATE,
    LINK_POLICY_CUSTOMER_HK  BINARY(16),
    LINK_POLICY_AGENT_HK     BINARY(16)
);
```

### PIT vs Bridge Table

| Feature  | PIT Table                    | Bridge Table             |
| -------- | ---------------------------- | ------------------------ |
| Purpose  | Multi-satellite snapshots    | Multi-hub/link traversal |
| Scope    | Single Hub                   | Multiple Hubs and Links  |
| Use case | Historical attribute queries | Relationship queries     |

---

## 11. Data Vault vs Star Schema vs NF3

| Feature           | NF3                   | Star Schema      | Data Vault                |
| ----------------- | --------------------- | ---------------- | ------------------------- |
| Purpose           | OLTP / operational    | OLAP / reporting | Enterprise DWH            |
| History tracking  | Limited               | SCD types        | Full history always       |
| Flexibility       | Low                   | Medium           | High                      |
| Auditability      | Low                   | Low              | High                      |
| Query performance | Slow for analytics    | Fast             | Medium (needs PIT/Bridge) |
| Source changes    | Difficult             | Moderate         | Easy                      |
| Business rules    | Embedded              | Embedded         | Separated                 |
| Parallel loading  | No                    | No               | Yes                       |
| Best for          | Transactional systems | Data marts       | Enterprise data warehouse |

---

## 12. Data Vault Loading Best Practices

### 1. Always Use Staging Layer

```
Source → Staging (truncate & reload) → Raw Vault (insert-only)
```

### 2. Hash Key Consistency

Always normalize before hashing — uppercase, trim whitespace, handle NULLs:

```sql
MD5(UPPER(TRIM(COALESCE(BUSINESS_KEY, 'NULL'))))
```

### 3. Use HASH_DIFF in Satellites

Avoid loading duplicate records by comparing hash of all attributes:

```sql
SELECT *
FROM STAGING s
LEFT JOIN SAT_CUSTOMER c
    ON s.HUB_CUSTOMER_HK = c.HUB_CUSTOMER_HK
    AND c.LOAD_END_DATE IS NULL
WHERE s.HASH_DIFF <> c.HASH_DIFF
   OR c.HUB_CUSTOMER_HK IS NULL;
```

### 4. Insert-Only Loading

Never update or delete records in Hubs, Links, or Satellites. New versions are inserted with a new `LOAD_DATE`.

### 5. Parallel Loading

Hubs, Links, and Satellites can all be loaded **independently and in parallel** — a major advantage of Data Vault.

```
Source Staging
   ├──► Load Hub A      (parallel)
   ├──► Load Hub B      (parallel)
   ├──► Load Link A-B   (after hubs)
   └──► Load Satellites (after hubs/links)
```

---

## 13. Data Vault on Modern Cloud Platforms

Data Vault 2.0 is well-suited for cloud platforms like **Snowflake**, **Databricks**, and **BigQuery**.

### Data Vault on Snowflake

```sql
-- Efficient hash key using Snowflake's MD5 function
SELECT MD5(UPPER(TRIM(POLICY_ID))) AS HUB_POLICY_HK,
       CURRENT_TIMESTAMP()         AS LOAD_DATE,
       'CRM_SYSTEM'                AS RECORD_SOURCE,
       POLICY_ID
FROM STAGING_POLICIES
WHERE HUB_POLICY_HK NOT IN (SELECT HUB_POLICY_HK FROM HUB_POLICY);
```

### Automation Tools

| Tool             | Description                                           |
| ---------------- | ----------------------------------------------------- |
| **dbt**          | Popular for automating Data Vault loading with macros |
| **AutoVault**    | Purpose-built Data Vault automation                   |
| **WhereScape**   | Enterprise Data Vault automation platform             |
| **Datavaultdbt** | dbt package specifically for Data Vault 2.0 patterns  |

### dbt Example — Hub Load

```sql
-- models/raw_vault/hub_policy.sql
{{ config(materialized='incremental', unique_key='HUB_POLICY_HK') }}

SELECT
    MD5(UPPER(TRIM(POLICY_ID)))  AS HUB_POLICY_HK,
    LOADED_AT                    AS LOAD_DATE,
    'CRM'                        AS RECORD_SOURCE,
    POLICY_ID
FROM {{ ref('stg_policies') }}

{% if is_incremental() %}
WHERE HUB_POLICY_HK NOT IN (SELECT HUB_POLICY_HK FROM {{ this }})
{% endif %}
```

---

## 14. Common Interview Questions & Answers

### Q: Why use Data Vault over Star Schema?

**Answer:**
Star Schema is great for reporting but struggles with:

- Frequent source system changes (schema changes break the model)
- Auditing (hard to trace where data came from)
- Multiple source system integration (conflicting keys)

Data Vault solves all three — it is more flexible, fully auditable, and handles multiple sources naturally. However, for final consumption (reports/dashboards), you still build a Star Schema **on top of** the Data Vault (as an Information Mart).

---

### Q: What is the difference between a Hub and a Dimension?

**Answer:**

| Feature       | Hub                                   | Dimension                  |
| ------------- | ------------------------------------- | -------------------------- |
| Contains      | Business key only                     | Business key + attributes  |
| History       | No history in Hub (goes to Satellite) | SCD types for history      |
| Source system | Single concept across systems         | Usually one source         |
| Attributes    | None                                  | All descriptive attributes |

A Hub is more granular — attributes are stored separately in Satellites, giving full flexibility.

---

### Q: Why are Hash Keys preferred over sequence-generated surrogate keys?

**Answer:**
Sequence-generated keys require a central sequence generator — this creates a **bottleneck** and prevents parallel loading. Hash keys are **computed independently** from the business key, so:

- Multiple systems can load simultaneously
- No central dependency
- Same business key always produces same hash — simplifies cross-system joins
- Hash keys can be pre-computed in the staging layer

---

### Q: What happens when a source system changes a business key?

**Answer:**
In Data Vault, you would use a **Same-As Link (SAL)** to map the old key to the new key. The Hub retains both keys, and the SAL captures the relationship. This preserves full history without any data loss.

---

### Q: How does Data Vault handle late-arriving data?

**Answer:**
Because Data Vault is **insert-only and time-stamped**, late-arriving data is simply inserted with its original event timestamp. The `LOAD_DATE` captures when the record was loaded into the vault, while a separate `EVENT_DATE` or `EFFECTIVE_DATE` column captures the business event time. This means late data integrates cleanly without disrupting existing records.

---

### Q: What is the Information Mart and how does it relate to Data Vault?

**Answer:**
The **Information Mart** (also called Data Mart) is the **consumption layer** built on top of the Business Vault. It is typically a **Star Schema or flat denormalized table** optimized for end-user reporting and BI tools. The Data Vault acts as the integration and history layer, while the Information Mart provides query performance for analysts.

```
Source Systems → Staging → Raw Vault → Business Vault → Information Mart → BI Tools
```

---

## 📌 Key Concepts Summary

| Concept              | Description                                         |
| -------------------- | --------------------------------------------------- |
| **Hub**              | Unique business keys — the "what" of business       |
| **Link**             | Relationships between hubs — the "interaction"      |
| **Satellite**        | Descriptive attributes and history — the "detail"   |
| **Raw Vault**        | Exact copy of source data — no transformations      |
| **Business Vault**   | Business rules and transformations applied          |
| **Hash Key**         | Deterministic surrogate key enabling parallel load  |
| **Hash Diff**        | Hash of attributes to detect changes in satellites  |
| **PIT Table**        | Performance structure for multi-satellite snapshots |
| **Bridge Table**     | Performance structure for multi-hub/link traversal  |
| **Same-As Link**     | Resolves duplicate or changed business keys         |
| **Information Mart** | Star Schema consumption layer for BI tools          |

---

_Data Vault 2.0 is the enterprise standard for auditable, scalable, and flexible data warehousing — mastering its patterns will set you apart in senior Data Engineer interviews._
