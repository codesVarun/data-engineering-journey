# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install Poetry
RUN apt-get update && apt-get install -y curl \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && apt-get clean

ENV PATH="/root/.local/bin:$PATH"

# Copy project files (only inside visualizations)
COPY . .

# Install dependencies using visualizations/pyproject.toml
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Optional: verify streamlit is installed
RUN which streamlit && streamlit --version

# Default command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]