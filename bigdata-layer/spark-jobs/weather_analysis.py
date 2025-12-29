from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window, to_timestamp

spark = SparkSession.builder \
    .appName("WeatherAnalysisToMongo") \
    .master("spark://spark-master:7077") \
    .config("fs.defaultFS", "hdfs://master:8020") \
    .getOrCreate()

# 1. Read from HDFS
df = spark.read.json("hdfs://master:8020/farm/farm-weather/data.jsonl")

# 2. Transformations
df = df.withColumn("ts", to_timestamp(col("timestamp")))
weather_stats = df.groupBy(
    window(col("ts"), "1 hour"), 
    col("description")
).agg(
    avg("temp").alias("avg_temp"),
    avg("humidity").alias("avg_humidity")
)

# Flatten window
weather_stats = weather_stats.select(
    col("window.start").alias("start_time"),
    "description",
    "avg_temp",
    "avg_humidity"
)

# 3. Write to MongoDB (Updated for Connector 10.x)
print("--- Writing to MongoDB ---")
weather_stats.write \
    .format("mongodb") \
    .mode("append") \
    .option("connection.uri", "mongodb://mongodb:27017") \
    .option("database", "farm") \
    .option("collection", "weather_stats") \
    .save()

print("--- Job Completed Successfully ---")
spark.stop()