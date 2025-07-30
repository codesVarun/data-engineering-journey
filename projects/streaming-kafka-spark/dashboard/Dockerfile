# dashboard/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

# Install required packages
RUN pip install streamlit psycopg2-binary pandas streamlit-autorefresh

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]