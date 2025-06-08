# 🌀 Airflow Basics

Apache Airflow is an open-source platform to programmatically author, schedule, and monitor workflows.

---

## 🧠 Key Concepts

| Term         | Description |
|--------------|-------------|
| **DAG**      | Directed Acyclic Graph - defines a workflow |
| **Task**     | A unit of work within a DAG (usually an Operator) |
| **Operator** | Template to define what a task does (e.g., PythonOperator) |
| **Scheduler**| Picks up DAGs and schedules task runs |
| **Webserver**| UI for DAG monitoring, triggering, debugging |
| **Executor** | Defines how tasks are executed (e.g., LocalExecutor, CeleryExecutor) |
| **Metadata DB** | Stores state of DAGs, tasks, logs, etc. |

---

## 🛠️ Basic Setup (Dockerized)

1. Use **Docker Compose** with services:
   - `airflow-webserver`
   - `airflow-scheduler`
   - `postgres`
   - `airflow-init` (optional setup script)

2. Folder structure:

    ```
    airflow/
    ├── dags/
    ├── plugins/
    ├── logs/
    ├── docker-compose.yml
    └── .env
    ```

---

## ⚙️ Common CLI Commands

```bash
# Initialize DB
airflow db init

# Create a user (if using basic_auth)
airflow users create --username admin ...

# Run a DAG manually
airflow dags trigger <dag_id>

# List DAGs
airflow dags list

# Test a task
airflow tasks test <dag_id> <task_id> <exec_date>