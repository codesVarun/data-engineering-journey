# Practical Coding Questions & Solutions

---

## 🐍 Python — 5 Practical Questions

---

### P1. Open an Excel file and find duplicates in Column A

**Question:**
You have an Excel file `employees.xlsx` with a column `Employee_ID` in Column A. Write Python code to find and display all duplicate Employee IDs.

**Solution:**

```python
import pandas as pd

# Load the Excel file
df = pd.read_excel("employees.xlsx")

# Identify duplicates in Column A (Employee_ID)
duplicates = df[df["Employee_ID"].duplicated(keep=False)]

# Sort for easier reading
duplicates_sorted = duplicates.sort_values("Employee_ID")

print(f"Total duplicate rows found: {len(duplicates_sorted)}")
print(duplicates_sorted)

# Optional: Save duplicates to a new Excel file
duplicates_sorted.to_excel("duplicates_report.xlsx", index=False)
```

**Sample Input (`employees.xlsx`):**

| Employee_ID | Name    |
|-------------|---------|
| 101         | Alice   |
| 102         | Bob     |
| 101         | Alice   |
| 103         | Charlie |
| 102         | David   |

**Output:**
```
Total duplicate rows found: 4
   Employee_ID   Name
0          101  Alice
2          101  Alice
1          102    Bob
4          102  David
```

---

### P2. Read a CSV, clean nulls, and write the result back

**Question:**
You have a CSV `sales.csv` with columns `order_id`, `product`, `quantity`, `price`. Some rows have null values. Drop rows where `quantity` or `price` is null, fill missing `product` with `"Unknown"`, and save the cleaned file.

**Solution:**

```python
import pandas as pd

df = pd.read_csv("sales.csv")

print("Before cleaning:")
print(df.isnull().sum())

# Fill missing product names
df["product"] = df["product"].fillna("Unknown")

# Drop rows where quantity or price is null
df.dropna(subset=["quantity", "price"], inplace=True)

# Reset index after dropping rows
df.reset_index(drop=True, inplace=True)

print("\nAfter cleaning:")
print(df.isnull().sum())

df.to_csv("sales_cleaned.csv", index=False)
print("\nCleaned file saved.")
```

---

### P3. Merge two Excel sheets and find mismatches

**Question:**
You have two sheets in `data.xlsx`:
- `Sheet1` — Master list of product codes
- `Sheet2` — Inventory list of product codes

Find products that are in the master list but **missing** from inventory, and vice versa.

**Solution:**

```python
import pandas as pd

master = pd.read_excel("data.xlsx", sheet_name="Sheet1")
inventory = pd.read_excel("data.xlsx", sheet_name="Sheet2")

master_codes = set(master["product_code"])
inventory_codes = set(inventory["product_code"])

# In master but not in inventory
missing_from_inventory = master_codes - inventory_codes

# In inventory but not in master
extra_in_inventory = inventory_codes - master_codes

print("Missing from Inventory:")
for code in sorted(missing_from_inventory):
    print(f"  {code}")

print("\nExtra in Inventory (not in Master):")
for code in sorted(extra_in_inventory):
    print(f"  {code}")
```

---

### P4. Parse a JSON API response and flatten nested fields

**Question:**
You receive the following JSON response from an API. Extract `order_id`, `customer_name`, `city`, and each `item_name` with its `qty` into a flat DataFrame.

```json
[
  {
    "order_id": 1,
    "customer": {"name": "Alice", "address": {"city": "New York"}},
    "items": [{"item_name": "Laptop", "qty": 1}, {"item_name": "Mouse", "qty": 2}]
  },
  {
    "order_id": 2,
    "customer": {"name": "Bob", "address": {"city": "Chicago"}},
    "items": [{"item_name": "Keyboard", "qty": 1}]
  }
]
```

**Solution:**

```python
import pandas as pd
import json

with open("orders.json") as f:
    data = json.load(f)

rows = []
for order in data:
    for item in order["items"]:
        rows.append({
            "order_id":      order["order_id"],
            "customer_name": order["customer"]["name"],
            "city":          order["customer"]["address"]["city"],
            "item_name":     item["item_name"],
            "qty":           item["qty"]
        })

df = pd.DataFrame(rows)
print(df)
```

**Output:**

| order_id | customer_name | city     | item_name | qty |
|----------|---------------|----------|-----------|-----|
| 1        | Alice         | New York | Laptop    | 1   |
| 1        | Alice         | New York | Mouse     | 2   |
| 2        | Bob           | Chicago  | Keyboard  | 1   |

---

### P5. Automate sending a summary email with an Excel attachment

**Question:**
After processing a dataset, generate a summary Excel report and email it automatically using Python.

**Solution:**

```python
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Step 1: Create summary report
df = pd.read_csv("sales_cleaned.csv")
summary = df.groupby("product").agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("price", "sum")
).reset_index()

summary.to_excel("summary_report.xlsx", index=False)

# Step 2: Email the report
sender    = "you@example.com"
recipient = "manager@example.com"
password  = "your_app_password"

msg = MIMEMultipart()
msg["From"]    = sender
msg["To"]      = recipient
msg["Subject"] = "Daily Sales Summary Report"

msg.attach(MIMEText("Please find the attached sales summary report.", "plain"))

with open("summary_report.xlsx", "rb") as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=summary_report.xlsx")
    msg.attach(part)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.sendmail(sender, recipient, msg.as_string())

print("Email sent successfully.")
```

---

## ⚡ PySpark — 5 Practical Questions

---

### S1. Load a CSV, remove duplicates, and write to Parquet

**Question:**
Load `transactions.csv`, deduplicate records keeping the latest entry per `transaction_id` (based on `updated_at`), and write the result to Parquet.

**Solution:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Dedup").getOrCreate()

df = spark.read.csv("transactions.csv", header=True, inferSchema=True)

# Keep latest record per transaction_id
window = Window.partitionBy("transaction_id").orderBy(col("updated_at").desc())

df_deduped = (
    df.withColumn("rn", row_number().over(window))
      .filter(col("rn") == 1)
      .drop("rn")
)

df_deduped.write.mode("overwrite").parquet("output/transactions_clean")

print(f"Original count : {df.count()}")
print(f"Deduplicated   : {df_deduped.count()}")
```

---

### S2. Perform a join and calculate revenue per customer per region

**Question:**
You have two DataFrames:
- `orders` — `order_id`, `customer_id`, `amount`
- `customers` — `customer_id`, `name`, `region`

Join them and compute total revenue and order count per customer per region, sorted by revenue descending.

**Solution:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count, round as _round

spark = SparkSession.builder.appName("RevenueReport").getOrCreate()

orders = spark.read.parquet("orders/")
customers = spark.read.parquet("customers/")

result = (
    orders.join(customers, on="customer_id", how="inner")
          .groupBy("customer_id", "name", "region")
          .agg(
              count("order_id").alias("total_orders"),
              _round(_sum("amount"), 2).alias("total_revenue")
          )
          .orderBy(col("total_revenue").desc())
)

result.show(20, truncate=False)
result.write.mode("overwrite").parquet("output/revenue_by_customer_region")
```

---

### S3. Handle NULL values and apply conditional transformations

**Question:**
In a `products` DataFrame with columns `product_id`, `category`, `price`, `discount`:
- Fill null `discount` with `0`
- Fill null `category` with `"Uncategorized"`
- Add a `final_price` column = `price * (1 - discount / 100)`
- Flag products as `"Premium"` if `final_price > 1000`, else `"Standard"`

**Solution:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, round as _round

spark = SparkSession.builder.appName("ProductTransform").getOrCreate()

df = spark.read.parquet("products/")

df_transformed = (
    df.fillna({"discount": 0, "category": "Uncategorized"})
      .withColumn(
          "final_price",
          _round(col("price") * (1 - col("discount") / 100), 2)
      )
      .withColumn(
          "tier",
          when(col("final_price") > 1000, "Premium").otherwise("Standard")
      )
)

df_transformed.show()
```

---

### S4. Detect and flag late-arriving records using watermarking

**Question:**
You have an events stream where each record has an `event_time` and `ingestion_time`. Flag records where `ingestion_time - event_time > 30 minutes` as late arrivals.

**Solution:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, when

spark = SparkSession.builder.appName("LateArrivals").getOrCreate()

df = spark.read.parquet("events/")

df_flagged = df.withColumn(
    "delay_minutes",
    (unix_timestamp("ingestion_time") - unix_timestamp("event_time")) / 60
).withColumn(
    "arrival_status",
    when(col("delay_minutes") > 30, "LATE").otherwise("ON_TIME")
)

# Summary
df_flagged.groupBy("arrival_status").count().show()

# Write late records to quarantine
df_flagged.filter(col("arrival_status") == "LATE") \
          .write.mode("overwrite").parquet("output/late_arrivals")
```

---

### S5. Incremental load using watermark from a control table

**Question:**
Implement an incremental load pattern: read the last processed timestamp from a `control` table, load only new records from the source, process them, and update the watermark.

**Solution:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as _max, lit
from datetime import datetime

spark = SparkSession.builder.appName("IncrementalLoad").getOrCreate()

# Step 1: Read last watermark
control_df = spark.read.parquet("control/watermarks/").filter(col("pipeline") == "sales")
last_watermark = control_df.select("last_run").collect()[0][0]
print(f"Loading records after: {last_watermark}")

# Step 2: Load only new/changed records
df_source = spark.read.parquet("source/sales/") \
                 .filter(col("updated_at") > lit(last_watermark))

print(f"New records to process: {df_source.count()}")

# Step 3: Transform and write
df_transformed = df_source.withColumn("load_ts", lit(datetime.utcnow().isoformat()))
df_transformed.write.mode("append").parquet("output/sales/")

# Step 4: Update watermark
new_watermark = df_source.select(_max("updated_at")).collect()[0][0]

new_control = spark.createDataFrame(
    [("sales", new_watermark)],
    ["pipeline", "last_run"]
)
new_control.write.mode("overwrite").parquet("control/watermarks/")

print(f"Watermark updated to: {new_watermark}")
```

---

## 🗄️ SQL — 5 Practical Questions

---

### Q1. Top N customers per region using PARTITION BY + RANK

**Question:**
Find the **top 2 customers by total spend** in each region.

**Tables:** `orders(order_id, customer_id, region, amount)`

**Solution:**

```sql
WITH customer_spend AS (
    SELECT
        customer_id,
        region,
        SUM(amount)                                          AS total_spend
    FROM orders
    GROUP BY customer_id, region
),
ranked AS (
    SELECT
        customer_id,
        region,
        total_spend,
        RANK() OVER (PARTITION BY region ORDER BY total_spend DESC) AS spend_rank
    FROM customer_spend
)
SELECT
    region,
    customer_id,
    total_spend,
    spend_rank
FROM ranked
WHERE spend_rank <= 2
ORDER BY region, spend_rank;
```

> **Note:** Use `RANK()` if ties should share a rank and skip the next rank. Use `DENSE_RANK()` if ties share a rank without gaps. Use `ROW_NUMBER()` if you want exactly 2 rows regardless of ties.

---

### Q2. Find departments where average salary exceeds company average — GROUP BY + HAVING

**Question:**
From the `employees` table, find all departments where the **average salary is above the company-wide average**, and show the count of employees in those departments.

**Table:** `employees(emp_id, name, department, salary)`

**Solution:**

```sql
SELECT
    department,
    COUNT(emp_id)        AS headcount,
    ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM employees)
ORDER BY avg_salary DESC;
```

**Sample Output:**

| department  | headcount | avg_salary |
|-------------|-----------|------------|
| Engineering | 25        | 95000.00   |
| Data        | 12        | 88500.00   |

---

### Q3. Running total and month-over-month growth using window functions

**Question:**
From the `monthly_sales` table, calculate:
1. A running total of sales
2. Month-over-month sales growth (%)

**Table:** `monthly_sales(year, month, sales_amount)`

**Solution:**

```sql
SELECT
    year,
    month,
    sales_amount,

    -- Running total
    SUM(sales_amount) OVER (
        ORDER BY year, month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                         AS running_total,

    -- Previous month's sales
    LAG(sales_amount) OVER (ORDER BY year, month)            AS prev_month_sales,

    -- Month-over-month growth %
    ROUND(
        100.0 * (sales_amount - LAG(sales_amount) OVER (ORDER BY year, month))
              / NULLIF(LAG(sales_amount) OVER (ORDER BY year, month), 0),
        2
    )                                                         AS mom_growth_pct

FROM monthly_sales
ORDER BY year, month;
```

---

### Q4. Find employees earning more than their manager using self-join

**Question:**
From the `employees` table, find all employees whose salary is **higher than their direct manager's salary**.

**Table:** `employees(emp_id, name, salary, manager_id)`

**Solution:**

```sql
SELECT
    e.emp_id,
    e.name                AS employee_name,
    e.salary              AS employee_salary,
    m.name                AS manager_name,
    m.salary              AS manager_salary,
    e.salary - m.salary   AS salary_difference
FROM employees e
JOIN employees m
    ON e.manager_id = m.emp_id
WHERE e.salary > m.salary
ORDER BY salary_difference DESC;
```

---

### Q5. Use QUALIFY to filter window function results inline (Snowflake / BigQuery)

**Question:**
In each product category, find products whose sales rank in the **top 3** and whose total sales are above **$10,000** — all in a single query using `QUALIFY`.

**Table:** `product_sales(product_id, product_name, category, total_sales)`

**Solution (Snowflake / BigQuery syntax):**

```sql
SELECT
    product_id,
    product_name,
    category,
    total_sales,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) AS sales_rank
FROM product_sales
WHERE total_sales > 10000
QUALIFY DENSE_RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) <= 3
ORDER BY category, sales_rank;
```

> **Why QUALIFY?** It filters on window function results *without* needing a subquery or CTE, making the query cleaner and more readable. Equivalent to using `HAVING` for `GROUP BY`, but for window functions.

**Equivalent without QUALIFY (standard SQL):**

```sql
WITH ranked AS (
    SELECT
        product_id,
        product_name,
        category,
        total_sales,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) AS sales_rank
    FROM product_sales
    WHERE total_sales > 10000
)
SELECT * FROM ranked WHERE sales_rank <= 3
ORDER BY category, sales_rank;
```

---

*Generated: July 2026*
