# Cross-layer analysis: If Soil is dry AND Weather is hot/windy, calculate a "Watering Priority" score.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, avg, when, current_timestamp

# Initialize Spark
spark = SparkSession.builder \
    .appName("SmartIrrigationLogic") \
    .config("fs.defaultFS", "hdfs://master:8020") \
    .getOrCreate()

# 1. Read Soil and Weather Data
soil_df = spark.read.json("hdfs://master:8020/farm/farm-soil/data.jsonl")
weather_df = spark.read.json("hdfs://master:8020/farm/farm-weather/data.jsonl")

# 2. Pre-processing: Round timestamps to the nearest minute for joining
# This creates a "join_key" like "2025-12-29 19:10"
soil_prepared = soil_df.withColumn("join_time", date_format(col("timestamp"), "yyyy-MM-dd HH:mm"))
weather_prepared = weather_df.withColumn("join_time", date_format(col("timestamp"), "yyyy-MM-dd HH:mm"))

# 3. Join the datasets on the time window
# We use an inner join to only calculate scores when we have both readings
combined_df = soil_prepared.join(weather_prepared, "join_time")

# 4. Calculate Watering Priority Score
# Formula: (100 - Moisture) + (Temp * 0.5) + (Wind * 2)
# Logic: High temp and high wind accelerate evaporation (drying out soil faster)
analysis_df = combined_df.withColumn(
    "priority_score",
    (100 - col("soil_moisture")) + (col("temp") * 0.5) + (col("wind_speed") * 2.0)
)

# 5. Classify the Score
final_df = analysis_df.withColumn(
    "irrigation_need",
    when(col("priority_score") > 110, "CRITICAL")
    .when(col("priority_score") > 80, "HIGH")
    .when(col("priority_score") > 50, "MODERATE")
    .otherwise("LOW")
).withColumn("processed_at", current_timestamp())

# 6. Select final columns for MongoDB
# We keep the raw metrics so the UI can explain *why* the score is high
output_df = final_df.select(
    "join_time",
    "soil_moisture",
    "temp",
    "wind_speed",
    "priority_score",
    "irrigation_need",
    "processed_at"
)

# 7. Write to MongoDB
print("--- Writing Smart Irrigation Analysis to MongoDB ---")
output_df.write \
    .format("mongodb") \
    .mode("append") \
    .option("connection.uri", "mongodb://mongodb:27017") \
    .option("database", "farm") \
    .option("collection", "irrigation_logic") \
    .save()

print("--- Job Successfully Completed ---")
spark.stop()