# 🦠 ETL Pipeline for COVID-19 API using Airflow & Docker

This project is a **production-grade ETL pipeline** that ingests real-time COVID-19 statistics from a public API, transforms the data into structured formats, and loads it into a PostgreSQL database — all orchestrated by **Apache Airflow**, containerized with **Docker**, and managed with **Poetry** for dependency management.

---

## 🚀 Project Goals

- ✅ Automate COVID-19 data collection from a public API
- ✅ Clean and transform raw JSON into structured tables
- ✅ Persist data into a PostgreSQL warehouse
- ✅ Use Airflow to orchestrate daily ETL tasks
- ✅ Run everything in isolated containers using Docker Compose

---

## 📊 Use Case

This pipeline enables the automated collection of COVID-19 stats (cases, deaths, recoveries, etc.) at the **continent level**, including country mappings. The data can power dashboards, analytics, and trend reports for health orgs, journalists, or researchers.

---

## 📁 Project Structure
<details> <summary>📁 Click to expand - Project Directory Tree</summary>
    ```
    etl-pipeline-covid-api/
    │
    ├── dags/                  # Airflow DAGs for orchestration
    ├── scripts/               # ETL scripts: extract, transform, load
    │   ├── extract.py
    │   ├── transform.py
    │   ├── load.py
    │   └── run_etl.py
    ├── .env                   # Environment variables (DB credentials, etc.)
    ├── Dockerfile             # Custom Airflow image with Poetry
    ├── docker-compose.yml     # Services: airflow, postgres, scheduler
    ├── pyproject.toml         # Poetry-based dependency management
    └── README.md              # You are here
    ```
</details>
---

## 🛠️ Tech Stack

| Tool        | Purpose                          |
|-------------|----------------------------------|
| Airflow     | Orchestration of ETL workflow    |
| Python      | Core ETL logic                   |
| Pandas      | Data transformation              |
| SQLAlchemy  | Database interaction             |
| PostgreSQL  | Data warehouse                   |
| Docker      | Containerization                 |
| Poetry      | Dependency management            |

---

## 🔗 Data Source

- **API**: [disease.sh - COVID-19 API](https://disease.sh/docs/#/)
- **Endpoint Used**: `https://disease.sh/v3/covid-19/continents`

---

## 🧬 ETL Flow

1. **Extract** (`extract.py`)
   - Pulls JSON data from the COVID-19 API.

2. **Transform** (`transform.py`)
   - Converts raw JSON into two normalized tables:
     - `covid_continent_stats`: core stats per continent
     - `covid_continent_countries`: mapping of continent → countries

3. **Load** (`load.py`)
   - Inserts the transformed data into a PostgreSQL database.

4. **Orchestrate** (`run_etl.py` or Airflow DAG)
   - Runs the full ETL sequence in order.

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/codesvarun/data-engineering-journey.git
cd data-engineering-journey/projects/etl-pipeline-covid-api