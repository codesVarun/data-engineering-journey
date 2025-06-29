from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType

spark = SparkSession.builder.appName("KafkaSparkStreaming").getOrCreate()

schema = StructType() \
    .add("sensor_id", IntegerType()) \
    .add("timestamp", IntegerType()) \
    .add("temperature", FloatType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "sensor-data") \
    .load()

parsed_df = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

# Write to console or S3
query = parsed_df.writeStream \
    .format("console") \
    .start()

query.awaitTermination()