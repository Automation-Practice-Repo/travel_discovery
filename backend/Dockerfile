FROM python:3.12-slim

WORKDIR /workspace

# Install system dependencies needed for building python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Make start.sh executable
RUN chmod +x /workspace/start.sh

# Expose FastAPI port
EXPOSE 8000

# Run start script
CMD ["/workspace/start.sh"]
