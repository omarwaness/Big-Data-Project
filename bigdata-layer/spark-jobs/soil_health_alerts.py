from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp, when

# Initialize Spark
spark = SparkSession.builder \
    .appName("SoilHealthStatus") \
    .config("fs.defaultFS", "hdfs://master:8020") \
    .getOrCreate()

# 1. Read the raw soil data
df = spark.read.json("hdfs://master:8020/farm/farm-soil/data.jsonl")

# 2. Logic: Classify every reading based on moisture levels
# FIXED: Chained .otherwise() correctly for the alert_message column
status_df = df.withColumn(
    "severity", 
    when(col("soil_moisture") < 10.0, "CRITICAL").otherwise("NORMAL")
).withColumn(
    "color_code", 
    when(col("soil_moisture") < 10.0, "red").otherwise("green")
).withColumn(
    "alert_message", 
    when(col("soil_moisture") < 10.0, "Immediate irrigation required: Moisture below 10%!") \
    .otherwise("Soil moisture is healthy.")
).withColumn(
    "processed_at", current_timestamp())

# 3. Select columns for the database
final_output = status_df.select(
    "timestamp", 
    "soil_moisture", 
    "soil_ph",
    "soil_temp_c",
    "severity", 
    "color_code", 
    "alert_message", 
    "processed_at"
)

# 4. Write to MongoDB
print("--- Updating Soil Health Status in MongoDB ---")
final_output.write \
    .format("mongodb") \
    .mode("append") \
    .option("connection.uri", "mongodb://mongodb:27017") \
    .option("database", "farm") \
    .option("collection", "soil_status") \
    .save()

print("--- Database Update Complete ---")
spark.stop()