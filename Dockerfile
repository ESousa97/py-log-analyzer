FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application script
COPY py_log_analyzer.py .

# Entrypoint for the CLI utility
ENTRYPOINT ["python", "py_log_analyzer.py"]
