# Look at the next 5 days. If frost ($<2^\circ C$) or heatwave ($>35^\circ C$) is predicted, flag it for crop protection.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, when, lit, current_timestamp

# Initialize Spark
spark = SparkSession.builder \
    .appName("ForecastRiskAudit") \
    .config("fs.defaultFS", "hdfs://master:8020") \
    .getOrCreate()

# 1. Read the nested forecast data
# Note: I'm using the forecast path since the data provided is forecast data
df = spark.read.json("hdfs://master:8020/farm/farm-forecast/data.jsonl")

# 2. Flatten the data
# Use explode to turn the 'readings' list into individual rows
flattened_df = df.select(
    col("timestamp").alias("extraction_time"),
    explode(col("readings")).alias("reading")
)

# 3. Extract nested fields for easier analysis
forecast_df = flattened_df.select(
    "extraction_time",
    col("reading.dt_text").alias("forecast_time"),
    col("reading.temp").alias("temp"),
    col("reading.rain").alias("rain"),
    col("reading.description").alias("desc")
)

# 4. Audit Logic: Define Risks
# We check for Frost, Heat, and Heavy Rain
audit_df = forecast_df.withColumn(
    "risk_level",
    when(col("temp") < 2.0, "HIGH (FROST)")
    .when(col("temp") > 35.0, "HIGH (HEAT)")
    .when(col("rain") > 5.0, "MEDIUM (HEAVY RAIN)")
    .otherwise("LOW (CLEAR)")
).withColumn(
    "action_required",
    when(col("temp") < 2.0, "Prepare thermal covers")
    .when(col("temp") > 35.0, "Increase irrigation frequency")
    .when(col("rain") > 5.0, "Check drainage systems")
    .otherwise("No immediate action")
).withColumn("processed_at", current_timestamp())

# 5. Write results to MongoDB
print("--- Writing Forecast Risk Audit to MongoDB ---")
audit_df.write \
    .format("mongodb") \
    .mode("append") \
    .option("connection.uri", "mongodb://mongodb:27017") \
    .option("database", "farm") \
    .option("collection", "forecast_audit") \
    .save()

print("--- Forecast Audit Complete ---")
spark.stop()