# 🔑 12 SQL Patterns for Data Engineer Interviews

> These 12 patterns cover ~80% of SQL questions asked in Data Engineer interviews.
> Master these and you will be able to solve most problems by recognizing the pattern first.

---

## 1️⃣ Deduplication Pattern

### What it is

Remove duplicate rows and keep only one record per group — usually the first or the latest based on a timestamp.

### Core Query

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY key
               ORDER BY timestamp DESC  -- DESC = latest, ASC = earliest
           ) AS rn
    FROM table
) t
WHERE rn = 1;
```

### How it works

- `PARTITION BY key` — groups rows by the deduplication key (e.g., user_id, policy_id)
- `ORDER BY timestamp DESC` — ranks rows within each group, latest first
- `WHERE rn = 1` — keeps only the top-ranked (latest) row per group

### Example

**Input:**

| user_id | event    | timestamp           |
| ------- | -------- | ------------------- |
| U1      | login    | 2026-01-01 09:00:00 |
| U1      | login    | 2026-01-01 10:00:00 |
| U2      | purchase | 2026-01-02 08:00:00 |

**Output (latest per user):**

| user_id | event    | timestamp           |
| ------- | -------- | ------------------- |
| U1      | login    | 2026-01-01 10:00:00 |
| U2      | purchase | 2026-01-02 08:00:00 |

### When to use it

- CDC (Change Data Capture) pipelines — keep latest version of a record
- Remove duplicate events from streaming ingestion
- Get the most recent record per user/policy/account

### Key interview tip

> If you want the **first** record, use `ORDER BY timestamp ASC`. If you want the **latest**, use `DESC`. Always ask yourself: "Which end of the timeline do I need?"

---

## 2️⃣ Top-N Per Group Pattern

### What it is

Find the top N records within each category or group, ranked by some metric.

### Core Query

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY category
               ORDER BY metric DESC
           ) AS rn
    FROM table
) t
WHERE rn <= 3;  -- Change N here
```

### How it works

- `PARTITION BY category` — resets the ranking for each category
- `ORDER BY metric DESC` — ranks by the metric you care about (highest first)
- `WHERE rn <= N` — keeps only the top N rows per category

### Example

**Task:** Find top 3 products by sales per category.

```sql
SELECT *
FROM (
    SELECT
        category,
        product_name,
        total_sales,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_sales DESC
        ) AS rn
    FROM products
) t
WHERE rn <= 3;
```

**Output:**

| category    | product_name | total_sales | rn  |
| ----------- | ------------ | ----------- | --- |
| Electronics | Laptop       | 50000       | 1   |
| Electronics | Phone        | 45000       | 2   |
| Electronics | Tablet       | 30000       | 3   |
| Clothing    | Jacket       | 20000       | 1   |

### ROW_NUMBER vs RANK vs DENSE_RANK for Top-N

| Function     | Handles ties by...                | Use when...                          |
| ------------ | --------------------------------- | ------------------------------------ |
| `ROW_NUMBER` | Assigning unique rank always      | You want exactly N rows, no ties     |
| `RANK`       | Skipping ranks after ties (1,1,3) | Ties should share rank, gaps allowed |
| `DENSE_RANK` | No gaps after ties (1,1,2)        | Ties should share rank, no gaps      |

### When to use it

- Top 3 salespersons per region
- Top 5 most expensive claims per policy type
- Best performing products per category

---

## 3️⃣ Running Total / Running Balance Pattern

### What it is

Calculate a cumulative sum that grows row by row within a partition, ordered by time.

### Core Query

```sql
SELECT
    id,
    date,
    amount,
    SUM(amount) OVER (
        PARTITION BY id
        ORDER BY date
    ) AS running_total
FROM transactions;
```

### How it works

- `SUM(amount) OVER (...)` — a window function that sums across rows
- `PARTITION BY id` — resets the running total for each account/user
- `ORDER BY date` — ensures the sum accumulates in chronological order
- Each row's value = sum of all rows up to and including that row

### Example

**Input:**

| account_id | date       | amount |
| ---------- | ---------- | ------ |
| A1         | 2026-01-01 | 100    |
| A1         | 2026-01-05 | 200    |
| A1         | 2026-01-10 | -50    |

**Output:**

| account_id | date       | amount | running_total |
| ---------- | ---------- | ------ | ------------- |
| A1         | 2026-01-01 | 100    | 100           |
| A1         | 2026-01-05 | 200    | 300           |
| A1         | 2026-01-10 | -50    | 250           |

### Variations

```sql
-- Running count
COUNT(*) OVER (PARTITION BY id ORDER BY date)

-- Running average
AVG(amount) OVER (PARTITION BY id ORDER BY date)

-- Running max (peak value so far)
MAX(amount) OVER (PARTITION BY id ORDER BY date)
```

### When to use it

- Bank account balance over time
- Cumulative revenue/sales metrics
- Track policy premium payments over a period

---

## 4️⃣ Gap Between Rows Pattern

### What it is

Calculate the difference between a row and the previous row within a group — used to measure time gaps or value changes.

### Core Query

```sql
SELECT
    id,
    date,
    date - LAG(date) OVER (
        PARTITION BY id
        ORDER BY date
    ) AS gap_days
FROM table;
```

### How it works

- `LAG(date)` — returns the value of `date` from the previous row in the partition
- `date - LAG(date)` — computes the difference between current and previous date
- First row in each partition returns `NULL` (no previous row exists)

### Example

**Input:**

| policy_id | transaction_date |
| --------- | ---------------- |
| P1        | 2026-01-01       |
| P1        | 2026-01-10       |
| P1        | 2026-01-15       |

**Output:**

| policy_id | transaction_date | gap_days |
| --------- | ---------------- | -------- |
| P1        | 2026-01-01       | NULL     |
| P1        | 2026-01-10       | 9        |
| P1        | 2026-01-15       | 5        |

### Finding large gaps (inactivity detection)

```sql
SELECT *
FROM (
    SELECT
        id,
        date,
        date - LAG(date) OVER (PARTITION BY id ORDER BY date) AS gap_days
    FROM transactions
) t
WHERE gap_days > 30;  -- Users inactive for more than 30 days
```

### When to use it

- Detect customer inactivity / churn signals
- Measure time between insurance claims
- Identify unusual gaps in transaction activity

---

## 5️⃣ Consecutive Events Pattern

### What it is

Detect whether events happened on consecutive days (or time periods) — a streak of activity.

### Core Query

```sql
SELECT DISTINCT policy_id
FROM (
    SELECT
        policy_id,
        transaction_date,
        LAG(transaction_date, 1) OVER (PARTITION BY policy_id ORDER BY transaction_date) AS prev1,
        LAG(transaction_date, 2) OVER (PARTITION BY policy_id ORDER BY transaction_date) AS prev2
    FROM transactions
) t
WHERE transaction_date = prev1 + INTERVAL '1 day'
  AND prev1 = prev2 + INTERVAL '1 day';
```

### How it works

- `LAG(date, 1)` — the day before the current row
- `LAG(date, 2)` — two days before the current row
- The WHERE condition checks: is today exactly 1 day after yesterday, and is yesterday exactly 1 day after the day before?
- If both conditions are true → 3 consecutive days confirmed

### Example

**Input:**

| policy_id | transaction_date |
| --------- | ---------------- |
| 101       | 2026-01-01       |
| 101       | 2026-01-02       |
| 101       | 2026-01-03       |
| 102       | 2026-01-01       |
| 102       | 2026-01-05       |

**LAG values for policy 101:**

| date       | prev1      | prev2      | consecutive? |
| ---------- | ---------- | ---------- | ------------ |
| 2026-01-01 | NULL       | NULL       | ❌           |
| 2026-01-02 | 2026-01-01 | NULL       | ❌           |
| 2026-01-03 | 2026-01-02 | 2026-01-01 | ✅           |

**Output:** `101`

### When to use it

- Policies with transactions on 3+ consecutive days (fraud detection)
- Users who logged in every day for a week
- Detect repeated events in a short period

---

## 6️⃣ Gaps and Islands Pattern

### What it is

Group continuous sequences of rows (islands) and identify the breaks between them (gaps). The classic trick is subtracting a row number from the date — consecutive dates produce the same constant value.

### Core Query

```sql
SELECT
    id,
    MIN(date) AS island_start,
    MAX(date) AS island_end,
    COUNT(*) AS streak_length
FROM (
    SELECT
        id,
        date,
        date - CAST(ROW_NUMBER() OVER (PARTITION BY id ORDER BY date) AS INT) AS grp
    FROM events
) t
GROUP BY id, grp
ORDER BY id, island_start;
```

### How it works

**The key insight:** If dates are consecutive, subtracting an incrementing row number always gives the same value.

| date       | row_number | date - row_number |
| ---------- | ---------- | ----------------- | ---------- |
| 2026-01-01 | 1          | 2025-12-31 (same) |
| 2026-01-02 | 2          | 2025-12-31 (same) |
| 2026-01-03 | 3          | 2025-12-31 (same) |
| 2026-01-07 | 4          | 2026-01-03 (diff) | ← gap here |
| 2026-01-08 | 5          | 2026-01-03 (same) |

Rows with the same `grp` value belong to the same island (continuous streak).

### Example Output

| id  | island_start | island_end | streak_length |
| --- | ------------ | ---------- | ------------- |
| U1  | 2026-01-01   | 2026-01-03 | 3             |
| U1  | 2026-01-07   | 2026-01-08 | 2             |

### When to use it

- Continuous login streak detection
- Session grouping in user analytics
- Finding periods of continuous policy coverage

---

## 7️⃣ Ranking Pattern

### What it is

Assign ranks to rows within a group and filter by rank — used to find Nth highest values.

### Core Query

```sql
SELECT *
FROM (
    SELECT
        id,
        salary,
        DENSE_RANK() OVER (ORDER BY salary DESC) AS r
    FROM employees
) t
WHERE r = 3;  -- 3rd highest salary
```

### Ranking Functions Compared

| Function     | Example values | Behaviour                        |
| ------------ | -------------- | -------------------------------- |
| `ROW_NUMBER` | 1, 2, 3, 4     | Always unique, no ties           |
| `RANK`       | 1, 1, 3, 4     | Ties get same rank, next skipped |
| `DENSE_RANK` | 1, 1, 2, 3     | Ties get same rank, no gaps      |

### Example — 2nd Highest Premium Per Policy

```sql
WITH ranked AS (
    SELECT
        policy_id,
        premium,
        DENSE_RANK() OVER (
            PARTITION BY policy_id
            ORDER BY premium DESC
        ) AS r
    FROM policies
)
SELECT policy_id, premium AS second_highest_premium
FROM ranked
WHERE r = 2;
```

### Interview follow-up: "What if two premiums are equal?"

- `ROW_NUMBER` — one of them is ranked 2, the other 3 (arbitrary)
- `DENSE_RANK` — both are ranked 1, and the next distinct value is ranked 2 ✅ (correct for "second highest distinct value")
- `RANK` — both ranked 1, next value ranked 3 (skips rank 2)

> **Rule of thumb:** Use `DENSE_RANK` when you want the Nth distinct value. Use `ROW_NUMBER` when you want exactly N rows.

### When to use it

- Nth highest salary, premium, sales figure
- Leaderboards and performance rankings
- Finding outliers in ranked order

---

## 8️⃣ Conditional Aggregation Pattern

### What it is

Aggregate data conditionally within a single query — pivot-style summaries without actual pivoting.

### Core Query

```sql
SELECT
    policy_id,
    SUM(CASE WHEN status = 'active'   THEN 1 ELSE 0 END) AS active_count,
    SUM(CASE WHEN status = 'expired'  THEN 1 ELSE 0 END) AS expired_count,
    SUM(CASE WHEN status = 'pending'  THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN status = 'active'   THEN amount ELSE 0 END) AS active_amount
FROM policies
GROUP BY policy_id;
```

### How it works

- `CASE WHEN condition THEN value ELSE 0 END` — returns the value only when the condition is met, otherwise 0
- Wrapping it in `SUM()` or `COUNT()` accumulates only the matching rows
- Multiple conditions in one query = single table scan (efficient)

### Example Output

| policy_id | active_count | expired_count | active_amount |
| --------- | ------------ | ------------- | ------------- |
| P1        | 3            | 1             | 15000         |
| P2        | 0            | 2             | 0             |

### Variations

```sql
-- Count with filter (cleaner syntax in modern SQL)
COUNT(*) FILTER (WHERE status = 'active')

-- Average only for a subset
AVG(CASE WHEN region = 'North' THEN revenue END)

-- Boolean flag
MAX(CASE WHEN event = 'claim_filed' THEN 1 ELSE 0 END) AS has_claim
```

### When to use it

- Dashboard metrics (active vs inactive counts side by side)
- Pivot-like reports without PIVOT syntax
- Flagging whether a record ever met a condition

---

## 9️⃣ Self Join Pattern

### What it is

Join a table to itself to compare rows within the same table — used for hierarchical or parent-child relationships.

### Core Query

```sql
SELECT
    e.id         AS employee_id,
    e.name       AS employee_name,
    m.name       AS manager_name
FROM employees e
JOIN employees m
ON e.manager_id = m.id;
```

### How it works

- The same table is aliased twice (`e` for employee, `m` for manager)
- The join condition links a row to another row in the same table
- Rows without a match (e.g., top-level CEO with no manager) can be included with `LEFT JOIN`

### Example

**Input table: employees**

| id  | name    | manager_id |
| --- | ------- | ---------- |
| 1   | Alice   | NULL       |
| 2   | Bob     | 1          |
| 3   | Charlie | 1          |
| 4   | David   | 2          |

**Output:**

| employee_name | manager_name |
| ------------- | ------------ |
| Bob           | Alice        |
| Charlie       | Alice        |
| David         | Bob          |

### Common variations

```sql
-- Include employees with no manager (top level)
LEFT JOIN employees m ON e.manager_id = m.id

-- Find all employees who earn more than their manager
SELECT e.name
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

### When to use it

- Org hierarchy / reporting structure queries
- Parent-child category relationships
- Comparing a row against another row in the same table (e.g., price vs previous price)

---

## 🔟 Latest Record Without Window Functions

### What it is

Retrieve the most recent record per group using only `MAX()` and a JOIN — an alternative to ROW_NUMBER() that works in older SQL dialects and is a common interview trick.

### Core Query

```sql
SELECT t.*
FROM transactions t
JOIN (
    SELECT id, MAX(date) AS max_date
    FROM transactions
    GROUP BY id
) latest
ON t.id = latest.id
AND t.date = latest.max_date;
```

### How it works

- The subquery finds the maximum date per group
- The JOIN brings back the full row that matches that maximum date
- Only rows where both `id` AND `date` match are returned

### Example

**Input:**

| policy_id | transaction_date | amount |
| --------- | ---------------- | ------ |
| P1        | 2026-01-01       | 100    |
| P1        | 2026-01-15       | 200    |
| P2        | 2026-01-10       | 300    |

**Subquery result (MAX per policy):**

| policy_id | max_date   |
| --------- | ---------- |
| P1        | 2026-01-15 |
| P2        | 2026-01-10 |

**Final Output:**

| policy_id | transaction_date | amount |
| --------- | ---------------- | ------ |
| P1        | 2026-01-15       | 200    |
| P2        | 2026-01-10       | 300    |

### Window function equivalent (for comparison)

```sql
-- Same result, cleaner syntax
SELECT policy_id, transaction_date, amount
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY policy_id ORDER BY transaction_date DESC) AS rn
    FROM transactions
) t
WHERE rn = 1;
```

### When to use it

- Environments that don't support window functions
- Interview questions that explicitly say "without using window functions"
- A good fallback to know when ROW_NUMBER() is not available

---

## 1️⃣1️⃣ Sessionization Pattern

### What it is

Group a user's events into sessions by identifying inactivity gaps — if two consecutive events are more than N minutes apart, a new session starts.

### Core Query

```sql
WITH with_gaps AS (
    SELECT
        user_id,
        event_time,
        CASE
            WHEN event_time - LAG(event_time) OVER (
                    PARTITION BY user_id ORDER BY event_time
                 ) > INTERVAL '30 minutes'
            OR LAG(event_time) OVER (
                    PARTITION BY user_id ORDER BY event_time
                 ) IS NULL
            THEN 1 ELSE 0
        END AS is_new_session
    FROM events
),
with_session_id AS (
    SELECT *,
           SUM(is_new_session) OVER (
               PARTITION BY user_id
               ORDER BY event_time
           ) AS session_id
    FROM with_gaps
)
SELECT
    user_id,
    session_id,
    MIN(event_time) AS session_start,
    MAX(event_time) AS session_end,
    COUNT(*) AS event_count
FROM with_session_id
GROUP BY user_id, session_id;
```

### How it works
**Step 1 — Detect session boundaries:** If the gap from the previous event exceeds 30 minutes (or it's the first event), mark it as `is_new_session = 1`.

**Step 2 — Assign session IDs:** Use `SUM(is_new_session)` as a running counter — each time a new session starts, the session ID increments.

**Step 3 — Aggregate:** Group by `user_id` and `session_id` to get session-level metrics.

### Example

| user_id | event_time       | is_new_session | session_id |
| ------- | ---------------- | -------------- | ---------- | -------------- |
| U1      | 2026-01-01 09:00 | 1              | 1          |
| U1      | 2026-01-01 09:15 | 0              | 1          |
| U1      | 2026-01-01 09:55 | 1              | 2          | ← gap > 30 min |
| U1      | 2026-01-01 10:10 | 0              | 2          |

### When to use it
- Web analytics — group page views into user sessions
- App analytics — detect active usage periods
- Fraud detection — cluster transactions by time proximity

---

## 1️⃣2️⃣ Slowly Changing Dimension (SCD) Pattern

### What it is
Detect when a tracked attribute changes over time and maintain a full history of those changes — the foundation of SCD Type 2 in data warehouses.

### Core Query — Detecting Changes
```sql
SELECT
    id,
    value,
    effective_date,
    LAG(value) OVER (PARTITION BY id ORDER BY effective_date) AS previous_value,
    CASE
        WHEN value != LAG(value) OVER (PARTITION BY id ORDER BY effective_date)
        THEN 1 ELSE 0
    END AS has_changed
FROM tracked_table;
```

### SCD Type 2 — Full History Table Structure

| Column           | Description                               |
| ---------------- | ----------------------------------------- |
| `surrogate_key`  | Unique row identifier (auto-increment)    |
| `natural_key`    | Business key (e.g., policy_id)            |
| `attribute`      | The tracked value (e.g., address, tier)   |
| `effective_from` | Date this version became active           |
| `effective_to`   | Date this version expired (NULL = active) |
| `is_current`     | Boolean flag for the active row           |

### SCD2 MERGE Pattern

```sql
MERGE INTO dim_customer AS target
USING staging_customer AS source
ON target.customer_id = source.customer_id
   AND target.is_current = TRUE

-- If the attribute changed, expire the old row
WHEN MATCHED AND target.address != source.address THEN
    UPDATE SET
        target.effective_to = CURRENT_DATE - 1,
        target.is_current = FALSE

-- Insert the new version as a new row
WHEN NOT MATCHED THEN
    INSERT (customer_id, address, effective_from, effective_to, is_current)
    VALUES (source.customer_id, source.address, CURRENT_DATE, NULL, TRUE);
```

### Example — Policy Tier Change History

| surrogate_key | policy_id | tier   | effective_from | effective_to | is_current |
| ------------- | --------- | ------ | -------------- | ------------ | ---------- |
| 1             | P1        | Bronze | 2025-01-01     | 2025-06-30   | FALSE      |
| 2             | P1        | Silver | 2025-07-01     | NULL         | TRUE       |

### Querying history at a point in time
```sql
-- What tier was policy P1 on 2025-04-01?
SELECT tier
FROM dim_policy
WHERE policy_id = 'P1'
  AND effective_from <= '2025-04-01'
  AND (effective_to >= '2025-04-01' OR effective_to IS NULL);
```

### When to use it
- Track customer address, tier, or status changes over time
- Insurance policy endorsements and amendments
- Any dimension where historical accuracy matters

---

## 📋 Quick Reference Summary

| #   | Pattern                    | Key Functions               | Common Use Case                       |
| --- | -------------------------- | --------------------------- | ------------------------------------- |
| 1   | Deduplication              | `ROW_NUMBER`, `PARTITION`   | Latest record per key, CDC pipelines  |
| 2   | Top-N Per Group            | `ROW_NUMBER`, `DENSE_RANK`  | Top products/employees per category   |
| 3   | Running Total              | `SUM() OVER`                | Account balances, cumulative metrics  |
| 4   | Gap Between Rows           | `LAG()`                     | Inactivity detection, churn analysis  |
| 5   | Consecutive Events         | `LAG()`, date arithmetic    | Streak detection, fraud signals       |
| 6   | Gaps and Islands           | `ROW_NUMBER`, date - rownum | Session grouping, continuous streaks  |
| 7   | Ranking                    | `RANK`, `DENSE_RANK`        | Nth highest value, leaderboards       |
| 8   | Conditional Aggregation    | `CASE WHEN`, `SUM/COUNT`    | Pivot-style dashboards, KPI reports   |
| 9   | Self Join                  | `JOIN` on same table        | Hierarchy queries, parent-child trees |
| 10  | Latest Without Window Func | `MAX()`, subquery + JOIN    | Interviews without window functions   |
| 11  | Sessionization             | `LAG()`, `SUM() OVER`       | Web sessions, activity clustering     |
| 12  | SCD Pattern                | `LAG()`, `MERGE`            | Historical tracking, SCD Type 2       |

---

> 💡 **Interview Strategy:** When you see a new SQL problem, first ask yourself which pattern it maps to. Most problems are variations of one of these 12. Recognizing the pattern is half the solution.
