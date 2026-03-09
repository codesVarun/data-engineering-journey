# SQL Interview Preparation (Data Engineer)

This document contains important SQL interview questions with detailed explanations, examples, and concepts frequently asked in Data Engineering interviews.

Topics covered include:
- SQL fundamentals
- Window functions
- Query optimization
- Deduplication patterns
- Aggregations and joins

---

# 1. What is the difference between WHERE and HAVING?

WHERE and HAVING are both used to filter data in SQL queries, but they operate at different stages of query execution.

## WHERE
- Filters rows **before aggregation**.
- Cannot be used with aggregate functions like SUM(), COUNT(), AVG().

Example:

SELECT *
FROM employees
WHERE salary > 5000;

This filters individual rows before grouping or aggregation happens.

---

## HAVING
- Filters **after GROUP BY aggregation**.
- Can be used with aggregate functions.

Example:

SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

This returns departments that have more than 10 employees.

---

## Key Difference

| Feature | WHERE | HAVING |
|------|------|------|
| Works on | Rows | Aggregated groups |
| Execution stage | Before GROUP BY | After GROUP BY |
| Supports aggregate functions | No | Yes |

---

# 2. What are Window Functions?

Window functions perform calculations across a set of rows related to the current row **without collapsing rows like GROUP BY does**.

They allow calculations like ranking, running totals, and moving averages while keeping all rows in the result.

Window functions use the **OVER() clause**.

Example functions:
- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- SUM()
- AVG()
- LAG()
- LEAD()

Example:

SELECT
    employee_id,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees;

Explanation:

- PARTITION BY department → ranking resets per department
- ORDER BY salary DESC → highest salary gets rank 1

---

# 3. Difference between ROW_NUMBER, RANK and DENSE_RANK

These functions assign ranking numbers within a partition.

## ROW_NUMBER()

Assigns a **unique sequential number to each row**, even if values are identical.

Example:

| value |
|------|
|100|
|100|
|90|

Result:

| value | row_number |
|------|-----------|
|100|1|
|100|2|
|90|3|

---

## RANK()

Rows with equal values receive the same rank, but **next ranks are skipped**.

Example:

| value | rank |
|------|------|
|100|1|
|100|1|
|90|3|

Rank 2 is skipped.

---

## DENSE_RANK()

Rows with equal values receive the same rank, but **no rank numbers are skipped**.

Example:

| value | dense_rank |
|------|-----------|
|100|1|
|100|1|
|90|2|

---

## Summary

| Function | Duplicate Values | Skips Numbers |
|--------|----------------|--------------|
|ROW_NUMBER|No|No|
|RANK|Yes|Yes|
|DENSE_RANK|Yes|No|

---

# 4. How do you remove duplicates?

Duplicates can be removed using the ROW_NUMBER() window function.

Example:

WITH ranked AS (
SELECT *,
ROW_NUMBER() OVER (PARTITION BY policy_id ORDER BY updated_at DESC) AS rn
FROM policies
)

SELECT *
FROM ranked
WHERE rn = 1;

Explanation:

- PARTITION BY policy_id groups records per policy
- ORDER BY updated_at DESC ensures latest record gets rank 1
- WHERE rn = 1 keeps only the latest record

This method is widely used in **data engineering pipelines to deduplicate records**.

---

# 5. How to find the second highest value?

One common method is using a subquery.

Example:

SELECT MAX(salary)
FROM employees
WHERE salary < (
SELECT MAX(salary)
FROM employees
);

Explanation:

1. Inner query finds highest salary
2. Outer query finds maximum salary less than highest

---

Alternative using window functions:

SELECT salary
FROM (
SELECT salary,
DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
FROM employees
) t
WHERE rnk = 2;

---

# 6. Difference between INNER JOIN and LEFT JOIN

## INNER JOIN

Returns only rows that match in both tables.

Example:

SELECT *
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;

If a customer has no orders, that customer will not appear in results.

---

## LEFT JOIN

Returns all rows from the left table and matching rows from the right table.

Example:

SELECT *
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

If a customer has no orders, the order columns will contain NULL values.

---

## Key Difference

| Join Type | Returned Rows |
|----------|--------------|
|INNER JOIN|Only matching rows|
|LEFT JOIN|All rows from left table|

---

# 7. What is a CTE (Common Table Expression)?

A CTE is a temporary named result set that can be referenced within a query.

It improves query readability and helps break complex queries into smaller steps.

Example:

WITH sales_cte AS (
SELECT *
FROM sales
WHERE year = 2024
)

SELECT *
FROM sales_cte;

Benefits:

- Improves readability
- Useful for recursive queries
- Helps simplify complex logic

---

# 8. What is indexing?

An index is a data structure that improves query performance by allowing faster data retrieval.

Without index:
Database scans entire table.

With index:
Database quickly locates required rows.

Example:

CREATE INDEX idx_employee_salary
ON employees(salary);

---

## Note for Snowflake

Snowflake does not use traditional indexes.

Instead it uses **micro-partitions and clustering keys** to optimize queries.

---

# 9. What is partitioning?

Partitioning divides a large table into smaller segments to improve performance.

Benefits:

- Faster query execution
- Reduced data scanning
- Improved manageability

Example partitioning strategy:

Partition data by date.

Example:

transactions table partitioned by transaction_date.

Queries filtering by date will scan fewer partitions.

---

# 10. What is query optimization?

Query optimization improves SQL performance by reducing processing time and resource usage.

Common techniques:

## 1. Filter Early

Use WHERE clause to reduce data before joins or aggregations.

Example:

SELECT *
FROM transactions
WHERE transaction_date > '2024-01-01';

---

## 2. Avoid SELECT *

Select only required columns.

Example:

SELECT policy_id, transaction_amount
FROM transactions;

---

## 3. Reduce Joins

Unnecessary joins increase computation and memory usage.

---

## 4. Use Aggregation Efficiently

Avoid aggregating unnecessary rows.

---

## 5. Partition Pruning

Filter by partition columns to reduce scanned data.

Example:

SELECT *
FROM transactions
WHERE transaction_date BETWEEN '2024-01-01' AND '2024-01-31';

---

# Conclusion

SQL remains the most critical skill for Data Engineers.

Key areas to master include:

- Window functions
- Joins
- Aggregations
- Query optimization
- Deduplication patterns

Strong SQL skills are essential for working with large-scale datasets and building reliable data pipelines.
