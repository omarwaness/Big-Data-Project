from pyspark.sql import SparkSession
from pyspark.sql import Row

# Initialize Spark
spark = SparkSession.builder \
    .appName("HDFS_Connection_Test") \
    .master("spark://spark-master:7077") \
    .config("fs.defaultFS", "hdfs://master:9000") \
    .getOrCreate()

try:
    # 1. Create dummy farm data
    data = [
        Row(sensor_id="Sensor_A", type="Temperature", value=22.5),
        Row(sensor_id="Sensor_B", type="Humidity", value=60.0),
        Row(sensor_id="Sensor_C", type="Soil_Moisture", value=15.2)
    ]
    df = spark.createDataFrame(data)

    print("--- STEP 1: Writing data to HDFS ---")
    # 2. Write to HDFS as a Parquet file
    df.write.mode("overwrite").parquet("hdfs://master:9000/test/farm_test_data.parquet")
    print("Write successful!")

    print("--- STEP 2: Reading data back from HDFS ---")
    # 3. Read it back to verify
    read_df = spark.read.parquet("hdfs://master:9000/test/farm_test_data.parquet")
    read_df.show()
    
    print("--- TEST PASSED SUCCESSFULLY ---")

except Exception as e:
    print(f"--- TEST FAILED --- \n{e}")

finally:
    spark.stop()