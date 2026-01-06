import schedule
import time
import subprocess
from datetime import datetime

def run_spark_job(script_name):
    print(f"[{datetime.now()}] Starting: {script_name}")
    
    # We use 'docker exec' to tell the spark-master to run the job
    command = [
        "docker", "exec", "spark-master", 
        "/opt/spark/bin/spark-submit",
        "--master", "spark://spark-master:7077",
        "--packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0",
        f"/opt/spark/work-dir/{script_name}"
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print(f"[{datetime.now()}] Success: {script_name}")
        else:
            print(f"[{datetime.now()}] FAILED: {script_name}\n{result.stderr}")
    except Exception as e:
        print(f"Error triggering job: {e}")

# SCHEDULES
# Run analysis every 30 minutes
schedule.every(30).minutes.do(run_spark_job, "soil_analysis.py")
schedule.every(30).minutes.do(run_spark_job, "smart_irrigation_logic.py")

# Run alerts more frequently (every 5 minutes)
schedule.every(10).minutes.do(run_spark_job, "soil_health_alerts.py")

# Run forecast audit twice a day
schedule.every().day.at("08:00").do(run_spark_job, "forecast_risk_audit.py")
schedule.every().day.at("20:00").do(run_spark_job, "forecast_risk_audit.py")

print("Smart Farm Orchestrator is running...")
while True:
    schedule.run_pending()
    time.sleep(1)