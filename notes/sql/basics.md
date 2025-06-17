# SQL Basics - Notes & Practice

> 📁 File: `data-engineering-journey/notes/sql/basics.md`

---

## 📚 1. SQL Query Execution Order

Understanding how SQL executes a query helps you write better and optimized queries:

```
1. FROM         -- identifies the source table
2. WHERE        -- filters rows
3. GROUP BY     -- groups rows for aggregation
4. HAVING       -- filters grouped rows
5. SELECT       -- selects columns and expressions
6. ORDER BY     -- sorts the result
7. LIMIT        -- restricts number of rows
```

> 🔍 **Note**: Although `SELECT` appears first in syntax, it's evaluated after `FROM`, `WHERE`, and `GROUP BY` during execution.

---

## 🔹 2. SELECT Statement

### 📖 Theory:

Used to select data from a table. You can select specific columns or use `*` for all.

### 🧪 Query:

```sql
SELECT * FROM employees;
```

```sql
SELECT first_name, department FROM employees;
```

### 🧾 Output:

Returns all/specified columns from the `employees` table.

---

## 🔹 3. WHERE Clause

### 📖 Theory:

Filters rows that satisfy a condition.

### 🧪 Query:

```sql
SELECT * FROM employees WHERE department = 'Engineering';
```

### 🧾 Output:

Returns only employees in the Engineering department.

---

## 🔹 4. ORDER BY Clause

### 📖 Theory:

Sorts result in ascending (default) or descending order.

### 🧪 Query:

```sql
SELECT * FROM employees ORDER BY salary DESC;
```

### 🧾 Output:

List of employees sorted by salary from highest to lowest.

---

## 🔹 5. DISTINCT Keyword

### 📖 Theory:

Removes duplicate entries from the result.

### 🧪 Query:

```sql
SELECT DISTINCT department FROM employees;
```

### 🧾 Output:

Unique list of departments.

---

## 🔹 6. LIMIT Clause

### 📖 Theory:

Restricts the number of rows returned.

### 🧪 Query:

```sql
SELECT * FROM employees LIMIT 3;
```

### 🧾 Output:

Returns the first 3 rows from the table.

---

## 🔹 7. AND, OR Conditions

### 📖 Theory:

Used to combine multiple filter conditions in `WHERE` clause.

### 🧪 Query:

```sql
SELECT * FROM employees 
WHERE department = 'Engineering' AND salary > 90000;
```

```sql
SELECT * FROM employees 
WHERE department = 'Engineering' OR department = 'HR';
```

---

## 🔹 8. IN Clause

### 📖 Theory:

Matches a value against a list of values.

### 🧪 Query:

```sql
SELECT * FROM employees 
WHERE department IN ('HR', 'Sales');
```

---

## 🔹 9. BETWEEN Clause

### 📖 Theory:

Filters values within a specific range.

### 🧪 Query:

```sql
SELECT * FROM employees 
WHERE salary BETWEEN 70000 AND 90000;
```

---

## 📌 Practice Tip

Use `\x` in `psql` for better output formatting:

```sql
\x
```

---

✅ **Next Up:** GROUP BY, Aggregate Functions (SUM, COUNT, AVG), JOINs