FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Copy example config files (actual config should be mounted or passed via env vars)
COPY config.ini.example ./config.ini.example
COPY .env.example ./.env.example

# Set default environment
ENV ENV=prod

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
