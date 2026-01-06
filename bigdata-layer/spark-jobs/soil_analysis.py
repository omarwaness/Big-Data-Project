# calculate averages per day
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, to_date

# Initialize Spark
spark = SparkSession.builder \
    .appName("DailySoilAnalysis") \
    .config("fs.defaultFS", "hdfs://master:8020") \
    .getOrCreate()

# 1. Read JSON data from HDFS
# Using the specific file path you provided
df = spark.read.json("hdfs://master:8020/farm/farm-soil/data.jsonl")

# 2. Pre-processing: Convert string timestamp to a Date object
# This changes "2025-12-29 19:10:14..." to just "2025-12-29"
df_with_date = df.withColumn("reading_date", to_date(col("timestamp")))

# 3. Analysis: Group by Date and calculate averages
# We handle moisture, pH, and soil temperature
daily_stats = df_with_date.groupBy("reading_date").agg(
    avg("soil_moisture").alias("avg_moisture"),
    avg("soil_ph").alias("avg_ph"),
    avg("soil_temp_c").alias("avg_temp_c")
)

# 4. Sort by date for cleaner MongoDB storage
daily_stats = daily_stats.orderBy("reading_date")

# 5. Write to MongoDB
print("--- Writing Daily Soil Averages to MongoDB ---")
daily_stats.write \
    .format("mongodb") \
    .mode("append") \
    .option("connection.uri", "mongodb://mongodb:27017") \
    .option("database", "farm") \
    .option("collection", "daily_soil_stats") \
    .save()

print("--- Job Successfully Completed ---")
spark.stop()