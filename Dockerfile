FROM python:3.9-slim

WORKDIR /challenge-globant

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

RUN echo "DIRECTORY LISTING START" && ls -la /challenge-globant/ && echo "DIRECTORY LISTING END"
# Make sure the entrypoint script is executable
RUN chmod +x entrypoint.sh

# Expose the port
EXPOSE 8000

# Use entrypoint script to wait for database and start application
ENTRYPOINT ["./entrypoint.sh"]