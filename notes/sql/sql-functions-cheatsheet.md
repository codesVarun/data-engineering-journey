# 📌 SQL Functions Cheat-Sheet (Null & Conditional Handling)

| Function | Description | Example | Supported In |
|----------|-------------|---------|--------------|
| **COALESCE(expr1, expr2, …)** | Returns the first non-NULL value from the list | `COALESCE(NULL, 'X', 'Y') → 'X'` | ANSI SQL (Snowflake, Oracle, SQL Server, Postgres, MySQL) |
| **NVL(expr1, expr2)** | If `expr1` is NULL, returns `expr2` | `NVL(NULL, 'X') → 'X'` | Oracle, Snowflake |
| **IFNULL(expr1, expr2)** | Same as NVL (2 arguments only) | `IFNULL(NULL, 'X') → 'X'` | MySQL, Snowflake |
| **NULLIF(expr1, expr2)** | Returns NULL if both are equal, else returns `expr1` | `NULLIF(10, 10) → NULL` | ANSI SQL |
| **NVL2(expr, not_null_val, null_val)** | Returns one value if expr is NOT NULL, another if NULL | `NVL2(email, 'Has Email', 'No Email')` | Oracle, Snowflake |
| **CASE WHEN … THEN … ELSE … END** | Flexible IF-ELSE logic | `CASE WHEN sal>10000 THEN 'High' END` | ANSI SQL |
| **IFF(condition, true_expr, false_expr)** | Shorthand IF-ELSE (2 branches only) | `IFF(age>18,'Adult','Minor')` | Snowflake |
| **DECODE(expr, s1,r1,s2,r2,…,default)** | Maps values like CASE | `DECODE(status,'A','Active','I','Inactive','Unknown')` | Oracle, Snowflake |
| **GREATEST(expr1, expr2, …)** | Returns largest non-NULL value | `GREATEST(3,7,5) → 7` | Oracle, Snowflake, Postgres, MySQL |
| **LEAST(expr1, expr2, …)** | Returns smallest non-NULL value | `LEAST(3,7,5) → 3` | Oracle, Snowflake, Postgres, MySQL |
| **GREATEST_IGNORE_NULLS(exprs)** | Max value ignoring NULLs | `GREATEST_IGNORE_NULLS(5, NULL, 3) → 5` | Snowflake |
| **LEAST_IGNORE_NULLS(exprs)** | Min value ignoring NULLs | `LEAST_IGNORE_NULLS(NULL, 10, 3) → 3` | Snowflake |
| **ISNULL(expr)** | Returns 1 if expr is NULL, else 0 | `ISNULL(NULL) → 1` | SQL Server |