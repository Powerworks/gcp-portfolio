FROM python:3.11-slim

WORKDIR /app

# Install native dependencies and purge local cache pools to keep image footprints light
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Run via Uvicorn, mapping explicitly to Cloud Run's dynamic PORT expectations
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]