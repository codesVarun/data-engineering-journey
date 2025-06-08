FROM apache/airflow:2.9.1-python3.10

# Install dependencies for Poetry and dotenv
USER root
RUN apt-get update && apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working directory for airflow
WORKDIR /opt/airflow

# Copy project metadata and install dependencies
COPY pyproject.toml poetry.lock ./

# Disable poetry venv creation, install dependencies (including dotenv)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the application source code
COPY ./scripts ./scripts

# Copy Airflow DAGs and plugins (if any)
COPY ./dags ./dags
COPY ./plugins ./plugins

# Copy environment file
COPY .env .env

# Set proper permissions
USER airflow