# SQL Intermediate - Notes & Practice

> 📁 File: `data-engineering-journey/notes/sql/intermediate.md`

---

## 🔸 1. GROUP BY Clause

### 📖 Theory:

Used to group rows that have the same values in specified columns, often used with aggregate functions.

### 🧪 Syntax:

```sql
SELECT department, COUNT(*)
FROM employees
GROUP BY department;
```

---

## 🔸 2. HAVING Clause

### 📖 Theory:

Filters grouped rows. Unlike `WHERE`, which filters individual rows, `HAVING` filters after grouping.

### 🧪 Syntax:

```sql
SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;
```

---

## 🔸 3. Aggregate Functions

| Function | Description                  |
| -------- | ---------------------------- |
| COUNT()  | Counts number of rows        |
| SUM()    | Adds up values in a column   |
| AVG()    | Calculates average of column |
| MAX()    | Returns maximum value        |
| MIN()    | Returns minimum value        |

### 🧪 Example:

```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department;
```

---

## 🔸 4. SQL JOINS

### 📖 Theory:

Used to combine rows from two or more tables based on a related column.

### 🔹 INNER JOIN

Returns only matching rows from both tables.

```sql
SELECT a.*, b.project_name
FROM employees a
INNER JOIN projects b ON a.id = b.employee_id;
```
🧠 Tip: Only employees who have an entry in the projects table (via employee_id) will appear in the result.

### 🔹 LEFT JOIN

Returns all rows from the left table and matching rows from the right.

```sql
SELECT a.*, b.project_name
FROM employees a
LEFT JOIN projects b ON a.id = b.employee_id;
```

### 🔹 RIGHT JOIN

Returns all rows from the right table and matching rows from the left.

```sql
SELECT a.*, b.project_name
FROM employees a
RIGHT JOIN projects b ON a.id = b.employee_id;
```

### 🔹 FULL OUTER JOIN

Returns all rows when there is a match in one of the tables.

```sql
SELECT a.*, b.project_name
FROM employees a
FULL OUTER JOIN projects b ON a.id = b.employee_id;
```

---

## 🔸 5. Subqueries

### 📖 Theory:

A query nested inside another query. Used in SELECT, FROM, or WHERE.

### 🧪 Example:

```sql
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

---

## 🔸 6. Window Functions

### 📖 Theory:

Performs calculations across a set of rows related to the current row.

### 🧪 ROW\_NUMBER():

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num
FROM employees;
```

### 🧪 RANK(), DENSE\_RANK():

```sql
SELECT *,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_dense_rank
FROM employees;
```

---

## 🔸 7. CASE Statement

### 📖 Theory:

Used for conditional logic in SQL.

### 🧪 Example:

```sql
SELECT first_name, salary,
  CASE
    WHEN salary > 90000 THEN 'High'
    WHEN salary BETWEEN 70000 AND 90000 THEN 'Medium'
    ELSE 'Low'
  END AS salary_level
FROM employees;
```

---

## 🔸 8. COALESCE, NULLIF

### 🧪 COALESCE:

Returns the first non-null value in the list.

```sql
SELECT first_name, COALESCE(middle_name, 'N/A') FROM employees;
```

### 🧪 NULLIF:

Returns NULL if both arguments are equal; else returns the first.

```sql
SELECT NULLIF(salary, 0) FROM employees;
```

---

✅ **Next Up:** Practice each topic above with your actual PostgreSQL data.