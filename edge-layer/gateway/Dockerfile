
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI using uvicorn
# Replace "main:app" with your filename and FastAPI instance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# 4. Run the API using the module method (safer)
#CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]