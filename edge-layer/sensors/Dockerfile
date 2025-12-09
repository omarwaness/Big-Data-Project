# Use the FULL version (not slim)
FROM python:3.11

WORKDIR /app

# 1. Copy requirements from the root context
COPY requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the CONTENTS of the sensors folder into /app
COPY sensors/ .

# 4. Run the sensor script
# Make sure to run unbuffered so logs show up immediately
CMD ["python", "-u", "weather_sensor.py"]