FROM python:3.11-slim

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io

WORKDIR /app

# Install Python schedule library
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Start the scheduler
CMD ["python", "-u", "orchestrator.py"]