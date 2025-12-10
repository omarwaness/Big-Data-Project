  # Use a lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the sensor code
COPY . .

# Run the soil sensor script
# Replace "sensor.py" with your actual filename
CMD ["python", "-u", "main_sensors.py"]