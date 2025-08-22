# syntax=docker/dockerfile:1
FROM python:3.13-slim-bookworm

WORKDIR /app

# Create the directory for the SQLite database and set permissions
RUN mkdir -p /app/data && chmod -R 777 /app/data

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY backend/app ./app

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
