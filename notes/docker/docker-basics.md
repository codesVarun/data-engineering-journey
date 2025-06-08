# 🐳 Docker Basics for Data Engineers

This note summarizes key Docker concepts with practical examples in the context of data engineering.

---

## ✅ What is Docker?

Docker is a tool to create, deploy, and run applications using containers. A container bundles all necessary components: code, dependencies, system tools, etc.

---

## 🧱 Core Concepts

| Concept | Description | Example |
|--------|-------------|---------|
| Image | Blueprint of your container | `apache/airflow:2.9.1-python3.10` |
| Container | A running instance of an image | Airflow Webserver |
| Volume | Persist data from container to host | `./dags:/opt/airflow/dags` |
| Network | Communication layer for containers | Airflow ↔ Postgres |
| Dockerfile | Custom image definition | For Python ETL scripts |
| Compose | Define multi-container setup | `docker-compose.yml` |

---

## 🚀 Docker Commands

```bash
# Build image from Dockerfile
docker build -t my-etl-image .

# Run container
docker run -it my-etl-image

# List containers
docker ps -a

# Stop all
docker stop $(docker ps -aq)

# Remove stopped containers
docker rm $(docker ps -aq)

# Start services from docker-compose
docker-compose up -d

# Stop services
docker-compose down