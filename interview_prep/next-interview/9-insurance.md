# Insurance Domain Interview Preparation (Experienced Data Engineer)

> A comprehensive guide covering Insurance domain knowledge, data concepts, and real-world data engineering scenarios commonly asked when interviewing for Data Engineering roles in the Insurance industry.

---

## 📋 Topics Covered

- Insurance Fundamentals
- Core Insurance Entities & Data Models
- Policy Lifecycle & Data
- Claims Processing & Data
- Underwriting & Risk Data
- Reinsurance
- Regulatory & Compliance Data
- Insurance Data Warehouse Concepts
- Common Insurance Data Engineering Scenarios
- KPIs & Metrics in Insurance
- Common Interview Questions & Answers

---

## 1. What is Insurance — The Business Context

**Insurance** is a financial product where an individual or business (the **policyholder**) pays a **premium** to an insurance company (the **insurer**) in exchange for financial protection against defined risks or losses.

As a Data Engineer in insurance, your job is to build pipelines and systems that power **underwriting decisions, claims processing, regulatory reporting, fraud detection, and actuarial analysis**.

### Types of Insurance

| Type | Description | Examples |
|---|---|---|
| **Life Insurance** | Pays out on death or critical illness | Term life, whole life, annuities |
| **Health Insurance** | Covers medical expenses | Individual, group, dental, vision |
| **Property & Casualty (P&C)** | Covers physical assets and liability | Auto, home, commercial property |
| **General Insurance** | Non-life, non-health coverage | Travel, pet, liability |
| **Reinsurance** | Insurance for insurance companies | Treaty, facultative reinsurance |
| **Commercial Insurance** | Business risk coverage | Workers comp, D&O, cyber liability |

### Key Stakeholders in Insurance Data

| Stakeholder | Data Interest |
|---|---|
| **Actuaries** | Risk modeling, loss reserving, pricing |
| **Underwriters** | Policy risk scoring and acceptance |
| **Claims Adjusters** | Claims history, fraud signals, payouts |
| **Finance** | Premium income, loss ratios, reserving |
| **Compliance/Legal** | Regulatory reporting, audit trails |
| **Data Engineers** | Pipelines, data quality, integration |

---

## 2. What is a Policy?

A **policy** is a **legally binding contract** between the insurer and the policyholder that defines:
- What risks are covered
- The premium amount and payment schedule
- The coverage limits and exclusions
- The policy term (start and end date)
- Conditions and obligations of both parties

### Policy Lifecycle

```
Quote → Bind → Issue → In-Force → Renewal / Cancellation / Expiry
  ↓        ↓       ↓        ↓              ↓
Risk    Accepted  Policy   Active      End of contract
assessed         created  coverage       period
```

### Policy Data Model (Core Tables)

```sql
-- Core policy table
CREATE TABLE POLICY (
    POLICY_ID           VARCHAR(50)     PRIMARY KEY,
    POLICY_NUMBER       VARCHAR(50)     NOT NULL,
    PRODUCT_CODE        VARCHAR(20),            -- AUTO, HOME, LIFE, HEALTH
    POLICY_STATUS       VARCHAR(20),            -- ACTIVE, LAPSED, CANCELLED, EXPIRED
    EFFECTIVE_DATE      DATE            NOT NULL,
    EXPIRY_DATE         DATE            NOT NULL,
    ISSUE_DATE          DATE,
    CANCELLATION_DATE   DATE,
    POLICYHOLDER_ID     VARCHAR(50),
    UNDERWRITER_ID      VARCHAR(50),
    CHANNEL             VARCHAR(50),            -- AGENT, DIRECT, BROKER
    PREMIUM_AMOUNT      DECIMAL(18,2),
    SUM_INSURED         DECIMAL(18,2),
    CURRENCY_CODE       CHAR(3),
    CREATED_AT          TIMESTAMP,
    UPDATED_AT          TIMESTAMP
);
```

### Key Policy Attributes

| Attribute | Description |
|---|---|
| **Policy Number** | Unique human-readable identifier |
| **Product Code** | Type of insurance (AUTO, HOME, LIFE) |
| **Effective Date** | When coverage starts |
| **Expiry Date** | When coverage ends |
| **Sum Insured** | Maximum payout amount |
| **Premium** | Amount paid by policyholder |
| **Status** | Current state of the policy |
| **Channel** | How the policy was sold (agent, broker, direct) |

### Policy Status Transitions

```
QUOTE
  ↓
BOUND        ← Risk accepted, awaiting formal issue
  ↓
IN-FORCE     ← Active, premium being collected
  ↓
├── LAPSED       ← Premium not paid
├── CANCELLED    ← Terminated early (insurer or policyholder)
├── EXPIRED      ← Reached natural end date
└── RENEWED      ← Extended for another term
```

---

## 3. What is Coverage?

**Coverage** defines the specific **risks, perils, and conditions** that the insurance policy will pay for, along with the limits and exclusions.

### Coverage Types by Line of Business

| Line of Business | Coverage Types |
|---|---|
| **Auto Insurance** | Bodily injury liability, property damage, collision, comprehensive, PIP |
| **Home Insurance** | Dwelling, personal property, liability, loss of use, medical payments |
| **Life Insurance** | Death benefit, terminal illness, accidental death |
| **Health Insurance** | Hospitalization, outpatient, prescription drugs, preventive care |
| **Commercial** | General liability, professional liability, product liability |

### Coverage Data Model

```sql
CREATE TABLE POLICY_COVERAGE (
    COVERAGE_ID         VARCHAR(50)     PRIMARY KEY,
    POLICY_ID           VARCHAR(50)     NOT NULL,
    COVERAGE_TYPE       VARCHAR(100),           -- COLLISION, COMPREHENSIVE, LIABILITY
    COVERAGE_LIMIT      DECIMAL(18,2),          -- Maximum payout for this coverage
    DEDUCTIBLE_AMOUNT   DECIMAL(18,2),          -- Amount policyholder pays first
    PREMIUM_SPLIT       DECIMAL(18,2),          -- Premium allocated to this coverage
    EFFECTIVE_DATE      DATE,
    EXPIRY_DATE         DATE,
    IS_ACTIVE           BOOLEAN,
    FOREIGN KEY (POLICY_ID) REFERENCES POLICY(POLICY_ID)
);
```

### Key Coverage Terms

| Term | Description |
|---|---|
| **Deductible** | Amount the policyholder pays out-of-pocket before insurance pays |
| **Premium** | Regular payment made to maintain coverage |
| **Coverage Limit** | Maximum amount insurer will pay for a claim |
| **Exclusion** | Specific risks or events NOT covered by the policy |
| **Endorsement** | An addition or amendment to the base policy |
| **Rider** | Optional add-on coverage purchased separately |
| **Co-insurance** | Shared payment between insurer and policyholder |
| **Sub-limit** | Lower limit for a specific category within the main limit |

---

## 4. What is a Claim?

A **claim** is a formal request submitted by the policyholder to the insurance company for payment or services under the terms of the policy after a covered loss or event occurs.

### Claims Lifecycle

```
Loss Event Occurs
       ↓
First Notice of Loss (FNOL)     ← Policyholder notifies insurer
       ↓
Claim Registration              ← Claim ID assigned, initial data captured
       ↓
Investigation & Assessment      ← Adjuster reviews, documents collected
       ↓
Coverage Verification           ← Confirm policy was active, event is covered
       ↓
Damage Evaluation               ← Estimate repair/replacement cost
       ↓
Settlement Decision             ← Approve, partial pay, or deny
       ↓
Payment                         ← Funds disbursed to claimant
       ↓
Claim Closure                   ← Claim marked as closed
```

### Claims Data Model

```sql
CREATE TABLE CLAIM (
    CLAIM_ID            VARCHAR(50)     PRIMARY KEY,
    CLAIM_NUMBER        VARCHAR(50)     NOT NULL UNIQUE,
    POLICY_ID           VARCHAR(50)     NOT NULL,
    COVERAGE_ID         VARCHAR(50),
    CLAIMANT_ID         VARCHAR(50),
    LOSS_DATE           DATE            NOT NULL,   -- When the event occurred
    REPORT_DATE         DATE,                       -- When claim was filed
    CLAIM_TYPE          VARCHAR(50),                -- AUTO, PROPERTY, LIABILITY
    CLAIM_STATUS        VARCHAR(30),                -- OPEN, PENDING, CLOSED, DENIED
    LOSS_DESCRIPTION    TEXT,
    CLAIMED_AMOUNT      DECIMAL(18,2),              -- Amount requested
    APPROVED_AMOUNT     DECIMAL(18,2),              -- Amount approved
    PAID_AMOUNT         DECIMAL(18,2),              -- Amount actually paid
    RESERVE_AMOUNT      DECIMAL(18,2),              -- Estimated total liability
    DEDUCTIBLE_APPLIED  DECIMAL(18,2),
    ADJUSTER_ID         VARCHAR(50),
    FRAUD_FLAG          BOOLEAN         DEFAULT FALSE,
    CREATED_AT          TIMESTAMP,
    CLOSED_AT           TIMESTAMP,
    FOREIGN KEY (POLICY_ID) REFERENCES POLICY(POLICY_ID)
);
```

### Claim Status Flow

```
OPEN → UNDER_INVESTIGATION → PENDING_PAYMENT → PAID → CLOSED
                                             → DENIED → CLOSED
                                             → WITHDRAWN → CLOSED
```

### Key Claims Metrics

| Metric | Formula | Description |
|---|---|---|
| **Loss Ratio** | Incurred Losses / Earned Premium | Core profitability metric |
| **Claims Frequency** | Number of Claims / Exposure Units | How often claims occur |
| **Average Claim Severity** | Total Paid / Number of Claims | Average cost per claim |
| **Claims Settlement Rate** | Closed Claims / Total Claims | Operational efficiency |
| **IBNR** | Estimated — statistical modeling | Incurred But Not Reported claims |

---

## 5. What is Underwriting?

**Underwriting** is the process by which an insurer **evaluates the risk** of insuring a person or asset and determines whether to offer coverage, at what price, and under what conditions.

It is the core function that determines insurance profitability.

### Underwriting Process

```
Application Submitted
        ↓
Risk Data Collection
(credit score, claims history, property data, medical records)
        ↓
Risk Assessment & Scoring
        ↓
Decision: Accept / Decline / Refer
        ↓
        ├── Accept → Calculate premium → Issue policy
        ├── Modify → Accept with exclusions or higher deductible
        └── Decline → Reject application
```

### Underwriting Data Sources

| Source | Data Used |
|---|---|
| **Application form** | Personal details, coverage requested |
| **Claims history** | Prior losses — key risk indicator |
| **Credit score** | Correlated with risk in auto/home |
| **Motor Vehicle Records (MVR)** | Driving history for auto insurance |
| **Property inspection** | Condition, location, construction type |
| **Medical records** | Health status for life/health insurance |
| **External data providers** | LexisNexis, ISO, CLUE reports |

### Underwriting Data Model

```sql
CREATE TABLE UNDERWRITING_SUBMISSION (
    SUBMISSION_ID       VARCHAR(50)     PRIMARY KEY,
    POLICY_ID           VARCHAR(50),
    APPLICANT_ID        VARCHAR(50),
    SUBMISSION_DATE     DATE,
    PRODUCT_CODE        VARCHAR(20),
    RISK_SCORE          DECIMAL(5,2),           -- Calculated risk score
    CREDIT_SCORE        INTEGER,
    PRIOR_CLAIMS_COUNT  INTEGER,
    PRIOR_CLAIMS_AMOUNT DECIMAL(18,2),
    UW_DECISION         VARCHAR(20),            -- ACCEPTED, DECLINED, REFERRED
    DECISION_DATE       DATE,
    UNDERWRITER_ID      VARCHAR(50),
    DECLINE_REASON      VARCHAR(500),
    RATED_PREMIUM       DECIMAL(18,2),          -- Premium after risk rating
    BASE_PREMIUM        DECIMAL(18,2),          -- Standard premium before adjustments
    SURCHARGES          DECIMAL(18,2),          -- Additional charges for high risk
    DISCOUNTS           DECIMAL(18,2)           -- Applied discounts
);
```

### Risk Factors by Line of Business

| Line of Business | Key Risk Factors |
|---|---|
| **Auto** | Age, driving record, vehicle type, location, annual mileage |
| **Home** | Location, construction type, age of property, flood zone, crime rate |
| **Life** | Age, health history, smoking status, occupation, BMI |
| **Commercial** | Industry type, revenue, number of employees, loss history |

---

## 6. What is a Premium?

A **premium** is the **amount paid by the policyholder** to the insurer in exchange for insurance coverage.

### Premium Components

```
Base Premium
    + Risk Surcharges    (high-risk factors)
    - Discounts          (multi-policy, no-claims, loyalty)
    + Taxes & Fees       (government levies, broker fees)
    = Final Premium
```

### Premium Types

| Type | Description |
|---|---|
| **Written Premium** | Total premium on policies written in a period |
| **Earned Premium** | Portion of written premium for the coverage period already passed |
| **Unearned Premium** | Portion of written premium for future coverage (liability) |
| **Net Premium** | Premium after reinsurance ceded |
| **Gross Premium** | Premium before any reinsurance |

### Premium Earning Calculation

```sql
-- Calculate earned premium for a policy
SELECT
    POLICY_ID,
    PREMIUM_AMOUNT,
    EFFECTIVE_DATE,
    EXPIRY_DATE,
    CURRENT_DATE AS AS_OF_DATE,
    DATEDIFF('day', EFFECTIVE_DATE, LEAST(CURRENT_DATE, EXPIRY_DATE)) AS DAYS_ELAPSED,
    DATEDIFF('day', EFFECTIVE_DATE, EXPIRY_DATE) AS TOTAL_DAYS,
    PREMIUM_AMOUNT *
        DATEDIFF('day', EFFECTIVE_DATE, LEAST(CURRENT_DATE, EXPIRY_DATE)) /
        DATEDIFF('day', EFFECTIVE_DATE, EXPIRY_DATE) AS EARNED_PREMIUM
FROM POLICY
WHERE POLICY_STATUS = 'ACTIVE';
```

---

## 7. What is Reinsurance?

**Reinsurance** is **insurance for insurance companies** — an insurer transfers a portion of its risk to another insurer (the reinsurer) to reduce its own exposure to large losses.

### Why Reinsurance Matters for Data Engineers

Reinsurance adds a **significant layer of data complexity**:
- Policies and claims must be split between retained and ceded portions
- Reinsurance treaties have complex rules for which risks are covered
- Financial reporting must separate gross, ceded, and net figures

### Types of Reinsurance

| Type | Description |
|---|---|
| **Treaty Reinsurance** | Automatic coverage for a portfolio of policies |
| **Facultative Reinsurance** | Case-by-case coverage for individual risks |
| **Proportional (Quota Share)** | Reinsurer takes a fixed % of premium and losses |
| **Non-Proportional (Excess of Loss)** | Reinsurer pays only when losses exceed a threshold |

### Reinsurance Data Model

```sql
CREATE TABLE REINSURANCE_TREATY (
    TREATY_ID           VARCHAR(50)     PRIMARY KEY,
    TREATY_NAME         VARCHAR(200),
    TREATY_TYPE         VARCHAR(50),            -- QUOTA_SHARE, EXCESS_OF_LOSS
    REINSURER_ID        VARCHAR(50),
    EFFECTIVE_DATE      DATE,
    EXPIRY_DATE         DATE,
    CESSION_PERCENTAGE  DECIMAL(5,2),           -- % ceded to reinsurer (quota share)
    RETENTION_LIMIT     DECIMAL(18,2),          -- Max insurer retains per event
    TREATY_LIMIT        DECIMAL(18,2)           -- Max reinsurer pays
);

CREATE TABLE CLAIM_REINSURANCE (
    CLAIM_ID            VARCHAR(50),
    TREATY_ID           VARCHAR(50),
    GROSS_LOSS          DECIMAL(18,2),
    RETAINED_LOSS       DECIMAL(18,2),          -- Insurer keeps this portion
    CEDED_LOSS          DECIMAL(18,2),          -- Reinsurer pays this portion
    RECOVERY_DATE       DATE,
    RECOVERY_STATUS     VARCHAR(20)
);
```

---

## 8. Regulatory & Compliance Data in Insurance

Insurance is one of the **most regulated industries** — data engineers must understand regulatory requirements that drive data pipeline and reporting needs.

### Key Regulatory Frameworks

| Regulation | Region | Requirement |
|---|---|---|
| **Solvency II** | EU | Capital adequacy, risk reporting |
| **IFRS 17** | Global | Insurance contract accounting standard |
| **GDPR** | EU | Personal data privacy and protection |
| **CCPA** | California | Consumer data privacy rights |
| **NAIC** | USA | State insurance regulatory reporting |
| **Lloyd's** | UK | London market reporting standards |

### IFRS 17 — Impact on Data Engineering

**IFRS 17** (effective January 2023) is the international accounting standard for insurance contracts. It requires insurers to:
- Group policies into **cohorts** by year of issue
- Calculate **Contractual Service Margin (CSM)** representing unearned profit
- Report at a granular policy group level
- Maintain full historical data for each cohort

This created massive demand for **granular, historical, auditable data pipelines** — a key data engineering challenge.

```sql
-- IFRS 17 cohort grouping example
SELECT
    PRODUCT_CODE,
    YEAR(EFFECTIVE_DATE)    AS COHORT_YEAR,
    QUARTER(EFFECTIVE_DATE) AS COHORT_QUARTER,
    RISK_BAND,              -- Profitable / Onerous grouping
    COUNT(POLICY_ID)        AS POLICY_COUNT,
    SUM(PREMIUM_AMOUNT)     AS TOTAL_PREMIUM,
    SUM(EXPECTED_CLAIM)     AS EXPECTED_LOSSES
FROM POLICY
GROUP BY PRODUCT_CODE, COHORT_YEAR, COHORT_QUARTER, RISK_BAND;
```

### Data Privacy in Insurance

Insurance handles highly sensitive **Personally Identifiable Information (PII)** and **Protected Health Information (PHI)**:

| Data Type | Examples | Protection Required |
|---|---|---|
| **PII** | Name, address, DOB, SSN, policy number | Encryption, masking, access control |
| **PHI** | Medical history, diagnoses, prescriptions | HIPAA compliance (US), GDPR (EU) |
| **Financial** | Bank details, credit scores, premium history | PCI-DSS, encryption |

```python
# Data masking example in PySpark
from pyspark.sql.functions import sha2, col, regexp_replace

df_masked = df \
    .withColumn("ssn_masked",   sha2(col("ssn"), 256)) \
    .withColumn("email_masked", regexp_replace(col("email"), r"(.).*@", "$1***@")) \
    .withColumn("phone_masked", regexp_replace(col("phone"), r"\d{6}(\d{4})", "******$1"))
```

---

## 9. Insurance Data Warehouse Design

### Typical Insurance Data Warehouse Schema

```
                    DIM_DATE
                       │
DIM_PRODUCT ──── FACT_PREMIUM ──── DIM_POLICYHOLDER
                       │
DIM_CHANNEL ───────────┘──────── DIM_AGENT
                       │
                  FACT_CLAIMS ──── DIM_CLAIM_TYPE
                       │
                  DIM_COVERAGE
```

### Core Fact Tables

| Fact Table | Granularity | Key Measures |
|---|---|---|
| **FACT_PREMIUM** | One row per policy per period | Written premium, earned premium, unearned premium |
| **FACT_CLAIMS** | One row per claim transaction | Claimed amount, paid amount, reserve amount |
| **FACT_POLICY_SNAPSHOT** | One row per policy per day | Policy count, sum insured, active coverage |
| **FACT_UNDERWRITING** | One row per submission | Risk score, accept/decline, rated premium |
| **FACT_REINSURANCE** | One row per claim + treaty | Gross loss, ceded loss, retained loss |

### Core Dimension Tables

| Dimension | Key Attributes |
|---|---|
| **DIM_POLICYHOLDER** | Name, DOB, address, customer segment, risk profile |
| **DIM_PRODUCT** | Product code, line of business, coverage type, product family |
| **DIM_AGENT / BROKER** | Agent ID, agency, region, license number |
| **DIM_DATE** | Date, week, month, quarter, year, fiscal period |
| **DIM_GEOGRAPHY** | State, region, territory, zip code, country |
| **DIM_RISK_OBJECT** | Vehicle VIN, property address, asset description |

---

## 10. Insurance KPIs & Metrics

These are the metrics data engineers are expected to know and build pipelines for:

### Profitability Metrics

| KPI | Formula | Description |
|---|---|---|
| **Loss Ratio** | Incurred Losses ÷ Earned Premium | Core measure of underwriting profitability |
| **Expense Ratio** | Operating Expenses ÷ Earned Premium | Cost efficiency |
| **Combined Ratio** | Loss Ratio + Expense Ratio | < 100% = profitable underwriting |
| **Investment Income Ratio** | Investment Income ÷ Earned Premium | Return on float |

```sql
-- Loss ratio by product and month
SELECT
    p.PRODUCT_CODE,
    DATE_TRUNC('month', c.LOSS_DATE)    AS LOSS_MONTH,
    SUM(c.PAID_AMOUNT)                  AS INCURRED_LOSSES,
    SUM(f.EARNED_PREMIUM)               AS EARNED_PREMIUM,
    SUM(c.PAID_AMOUNT) /
        NULLIF(SUM(f.EARNED_PREMIUM),0) AS LOSS_RATIO
FROM FACT_CLAIMS c
JOIN FACT_PREMIUM f  ON c.POLICY_ID = f.POLICY_ID
JOIN DIM_PRODUCT  p  ON f.PRODUCT_KEY = p.PRODUCT_KEY
GROUP BY p.PRODUCT_CODE, LOSS_MONTH
ORDER BY LOSS_MONTH DESC;
```

### Claims Metrics

| KPI | Description |
|---|---|
| **Claims Frequency** | Number of claims per 100 policies |
| **Average Claim Cost (Severity)** | Total paid ÷ number of claims |
| **Time to Settlement** | Average days from FNOL to payment |
| **Reopened Claims Rate** | % of closed claims reopened |
| **Fraud Detection Rate** | % of claims flagged for investigation |

### Premium Metrics

| KPI | Description |
|---|---|
| **Gross Written Premium (GWP)** | Total premium written before reinsurance |
| **Net Written Premium (NWP)** | GWP minus reinsurance ceded |
| **Policy Retention Rate** | % of policies renewed at expiry |
| **New Business Premium** | Premium from new policies in the period |

---

## 11. Common Insurance Data Engineering Scenarios

### Scenario 1: Building a Claims Pipeline

```
Source: Claims management system (RDBMS)
        ↓
Extract daily via CDC (Debezium / Fivetran)
        ↓
Land raw JSON in S3 / ADLS (Bronze layer)
        ↓
Validate:
  - Claim dates are logical (loss_date <= report_date)
  - Policy was active on the loss date
  - Claimed amount is non-negative
        ↓
Transform in Spark / dbt (Silver layer):
  - Standardize claim status codes across systems
  - Join to policy and coverage tables
  - Calculate reserve to paid ratio
        ↓
Aggregate (Gold layer):
  - Daily claims KPIs by product and region
  - Loss ratio calculations
        ↓
Load to Snowflake / Redshift for reporting
```

### Scenario 2: Policy Renewal Prediction Pipeline

```python
# Build a feature table for renewal prediction
renewal_features = spark.sql("""
    SELECT
        p.POLICY_ID,
        p.PRODUCT_CODE,
        p.PREMIUM_AMOUNT,
        DATEDIFF(p.EXPIRY_DATE, CURRENT_DATE)   AS DAYS_TO_EXPIRY,
        COUNT(c.CLAIM_ID)                        AS CLAIM_COUNT_3YR,
        SUM(c.PAID_AMOUNT)                       AS TOTAL_CLAIMS_3YR,
        p.PREMIUM_AMOUNT /
            NULLIF(SUM(c.PAID_AMOUNT), 0)        AS LOSS_RATIO,
        ph.TENURE_YEARS,
        ph.PRODUCT_COUNT                         AS POLICY_COUNT
    FROM POLICY p
    LEFT JOIN CLAIM c
        ON p.POLICY_ID = c.POLICY_ID
        AND c.LOSS_DATE >= DATEADD(year, -3, CURRENT_DATE)
    JOIN DIM_POLICYHOLDER ph ON p.POLICYHOLDER_ID = ph.POLICYHOLDER_ID
    WHERE DATEDIFF(p.EXPIRY_DATE, CURRENT_DATE) BETWEEN 0 AND 90
    GROUP BY ALL
""")
```

### Scenario 3: Fraud Detection Feature Engineering

```sql
-- Build fraud signals for claims
SELECT
    c.CLAIM_ID,
    c.POLICY_ID,
    c.CLAIMED_AMOUNT,

    -- Signal 1: High claim soon after policy inception
    DATEDIFF('day', p.EFFECTIVE_DATE, c.LOSS_DATE) AS DAYS_SINCE_INCEPTION,

    -- Signal 2: Multiple claims on same policy
    COUNT(c2.CLAIM_ID) OVER (
        PARTITION BY c.POLICY_ID
        ORDER BY c.REPORT_DATE
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS CUMULATIVE_CLAIMS,

    -- Signal 3: Claim amount vs average for product
    c.CLAIMED_AMOUNT /
        AVG(c.CLAIMED_AMOUNT) OVER (PARTITION BY c.CLAIM_TYPE) AS AMOUNT_VS_AVERAGE,

    -- Signal 4: Same address multiple claims
    COUNT(c3.CLAIM_ID) OVER (
        PARTITION BY ph.ADDRESS_HASH
    ) AS CLAIMS_SAME_ADDRESS

FROM CLAIM c
JOIN POLICY p           ON c.POLICY_ID = p.POLICY_ID
JOIN DIM_POLICYHOLDER ph ON p.POLICYHOLDER_ID = ph.POLICYHOLDER_ID
LEFT JOIN CLAIM c2      ON c.POLICY_ID = c2.POLICY_ID
LEFT JOIN CLAIM c3      ON ph.ADDRESS_HASH = (
    SELECT ADDRESS_HASH FROM DIM_POLICYHOLDER
    WHERE POLICYHOLDER_ID = c3.POLICY_ID
);
```

---

## 12. Common Interview Questions & Answers

### Q: How is insurance data different from data in other industries?

**Answer:**
Insurance data has several unique characteristics:
- **Long data retention** — policies and claims need to be kept for 7–10+ years for regulatory and legal reasons
- **Complex relationships** — a single claim can touch policy, coverage, reinsurance, and multiple payment records
- **Actuarial accuracy** — even small data errors can affect reserve calculations and financial reporting
- **Regulatory sensitivity** — IFRS 17, Solvency II, and state regulations dictate exact data structures and audit trails
- **High PII/PHI sensitivity** — health, financial, and personal data require strict governance
- **Historical immutability** — once a claim is paid or a policy expires, those records cannot be altered — audit trail is critical

---

### Q: What is the difference between written premium and earned premium?

**Answer:**
- **Written premium** is the total premium for a policy when it is written (issued) — booked upfront at policy inception
- **Earned premium** is the portion of that premium that corresponds to the coverage period that has already passed

Example: A 12-month policy with $1,200 annual premium written on July 1st — by December 31st (6 months later), only $600 has been *earned*. The remaining $600 is **unearned premium** — a liability the insurer owes if the policy is cancelled.

```
Earned Premium = Written Premium × (Days Elapsed ÷ Total Policy Days)
```

---

### Q: What is IBNR and why is it important for data engineering?

**Answer:**
**IBNR (Incurred But Not Reported)** refers to insurance losses that have already occurred but have not yet been reported to the insurer as claims.

It is a **statistical reserve** estimated by actuaries using historical loss development patterns.

For data engineers, IBNR is important because:
- Pipelines must feed actuaries **clean, complete, historical claims data** — any gaps affect IBNR calculations
- Loss development triangles must be built from **accurate incremental paid data**
- IBNR figures directly impact the insurer's financial reserves and regulatory capital

```sql
-- Loss development triangle — data structure for IBNR calculation
SELECT
    YEAR(LOSS_DATE)                             AS ACCIDENT_YEAR,
    DATEDIFF('month', LOSS_DATE, REPORT_DATE)   AS DEVELOPMENT_MONTH,
    SUM(PAID_AMOUNT)                            AS CUMULATIVE_PAID
FROM CLAIM
GROUP BY ACCIDENT_YEAR, DEVELOPMENT_MONTH
ORDER BY ACCIDENT_YEAR, DEVELOPMENT_MONTH;
```

---

### Q: How do you handle policy endorsements in a data pipeline?

**Answer:**
An **endorsement** is a mid-term change to a policy — it creates a new version of the policy with different attributes (new vehicle added, address changed, coverage increased).

In a data pipeline, endorsements are handled using **SCD Type 2** patterns:

```sql
-- Policy version table to track endorsements
CREATE TABLE POLICY_VERSION (
    POLICY_VERSION_ID   VARCHAR(50)     PRIMARY KEY,
    POLICY_ID           VARCHAR(50)     NOT NULL,
    VERSION_NUMBER      INTEGER         NOT NULL,
    ENDORSEMENT_TYPE    VARCHAR(100),           -- ADD_VEHICLE, ADDRESS_CHANGE, COVERAGE_INCREASE
    EFFECTIVE_DATE      DATE            NOT NULL,
    END_DATE            DATE,                   -- NULL if current version
    IS_CURRENT          BOOLEAN,
    PREMIUM_AMOUNT      DECIMAL(18,2),
    SUM_INSURED         DECIMAL(18,2),
    CHANGE_REASON       VARCHAR(500)
);
```

Each endorsement inserts a new row with the new `EFFECTIVE_DATE` and the previous version's `END_DATE` is updated — preserving full history of all policy changes.

---

### Q: What is a loss ratio and how would you build a pipeline to calculate it?

**Answer:**
**Loss Ratio = Incurred Losses ÷ Earned Premium**

A loss ratio below 100% means underwriting is profitable. Above 100% means the insurer is paying out more in claims than it collects in premium.

Pipeline to calculate it:

```
1. Claims pipeline → aggregate paid + reserved amounts by product, region, period
2. Premium pipeline → calculate earned premium for the same period
3. Join on product + region + period
4. Calculate loss ratio
5. Load to reporting layer for actuarial and finance teams
```

```sql
SELECT
    d.YEAR,
    d.MONTH,
    pr.PRODUCT_CODE,
    g.REGION,
    SUM(c.PAID_AMOUNT + c.RESERVE_AMOUNT)   AS INCURRED_LOSSES,
    SUM(f.EARNED_PREMIUM)                   AS EARNED_PREMIUM,
    ROUND(
        SUM(c.PAID_AMOUNT + c.RESERVE_AMOUNT) /
        NULLIF(SUM(f.EARNED_PREMIUM), 0) * 100
    , 2)                                    AS LOSS_RATIO_PCT
FROM FACT_CLAIMS c
JOIN FACT_PREMIUM f      ON c.POLICY_ID = f.POLICY_ID AND c.PERIOD_KEY = f.PERIOD_KEY
JOIN DIM_DATE     d      ON f.DATE_KEY = d.DATE_KEY
JOIN DIM_PRODUCT  pr     ON f.PRODUCT_KEY = pr.PRODUCT_KEY
JOIN DIM_GEOGRAPHY g     ON f.GEO_KEY = g.GEO_KEY
GROUP BY d.YEAR, d.MONTH, pr.PRODUCT_CODE, g.REGION;
```

---

### Q: How would you detect anomalies in claims data?

**Answer:**
Common anomaly detection approaches in insurance claims:

```python
from pyspark.sql.functions import col, avg, stddev, abs as spark_abs

# Z-score based anomaly detection on claim amounts
stats = df_claims.groupBy("claim_type").agg(
    avg("claimed_amount").alias("mean_amount"),
    stddev("claimed_amount").alias("std_amount")
)

df_flagged = df_claims.join(stats, "claim_type") \
    .withColumn("z_score",
        spark_abs(col("claimed_amount") - col("mean_amount")) / col("std_amount")) \
    .withColumn("is_anomaly", col("z_score") > 3)

# Additional business rule flags
df_flagged = df_flagged \
    .withColumn("flag_new_policy",
        (col("days_since_inception") < 30).cast("int")) \
    .withColumn("flag_round_amount",
        (col("claimed_amount") % 1000 == 0).cast("int")) \
    .withColumn("flag_high_frequency",
        (col("claims_last_12m") > 3).cast("int"))
```

---

## 📌 Key Concepts Summary

| Concept | Description |
|---|---|
| **Policy** | Contract between insurer and policyholder defining coverage |
| **Coverage** | Specific risks and limits defined in the policy |
| **Claim** | Request for payment after a covered loss event |
| **Underwriting** | Process of evaluating and pricing risk before issuing a policy |
| **Premium** | Payment made by policyholder for insurance coverage |
| **Earned Premium** | Portion of premium for coverage period already elapsed |
| **IBNR** | Losses incurred but not yet reported as claims |
| **Loss Ratio** | Incurred losses ÷ Earned premium — core profitability metric |
| **Combined Ratio** | Loss ratio + expense ratio — < 100% means profitable |
| **Reinsurance** | Insurance purchased by insurers to transfer their own risk |
| **Endorsement** | Mid-term change or amendment to a policy |
| **SCD Type 2** | Track full history of policy/endorsement changes |
| **IFRS 17** | International accounting standard for insurance contracts |
| **FNOL** | First Notice of Loss — when policyholder first reports a claim |
| **Reserve** | Estimated future cost of a claim not yet fully settled |

---

*Deep domain knowledge combined with strong data engineering skills is rare and highly valued in insurance — understanding the business context behind the data is what sets experienced candidates apart.*