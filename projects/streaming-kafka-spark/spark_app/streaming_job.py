# import json
# import os
# import signal
# import sys
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, col, current_timestamp, to_timestamp
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# class KafkaSparkStreaming:
#     def __init__(self, kafka_bootstrap_servers, kafka_topic, checkpoint_location):
#         self.kafka_bootstrap_servers = kafka_bootstrap_servers
#         self.kafka_topic = kafka_topic
#         self.checkpoint_location = checkpoint_location
#         self.spark = None
#         self.query = None

#         os.makedirs(checkpoint_location, exist_ok=True)
#         self._setup_spark_session()
#         self._setup_signal_handlers()

#     def _setup_spark_session(self):
#         try:
#             logger.info("Setting up Spark session...")
#             self.spark = SparkSession.builder \
#                 .appName("KafkaSparkStreaming") \
#                 .config("spark.jars.packages",
#                         "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,"
#                         "org.postgresql:postgresql:42.2.27") \
#                 .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
#                 .config("spark.sql.streaming.stopGracefullyOnShutdown", "true") \
#                 .config("spark.sql.shuffle.partitions", "2") \
#                 .config("spark.default.parallelism", "2") \
#                 .config("spark.sql.adaptive.enabled", "false") \
#                 .config("spark.sql.adaptive.coalescePartitions.enabled", "false") \
#                 .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
#                 .config("spark.sql.streaming.metricsEnabled", "true") \
#                 .getOrCreate()

#             self.spark.sparkContext.setLogLevel("WARN")
#             logger.info("Spark session created successfully")
#         except Exception as e:
#             logger.error(f"Failed to create Spark session: {e}")
#             raise

#     def _setup_signal_handlers(self):
#         def signal_handler(signum, frame):
#             logger.info(f"Received signal {signum}, shutting down gracefully...")
#             self.stop_streaming()
#             sys.exit(0)

#         signal.signal(signal.SIGINT, signal_handler)
#         signal.signal(signal.SIGTERM, signal_handler)

#     def stop_streaming(self):
#         try:
#             if self.query and self.query.isActive:
#                 logger.info("Stopping streaming query...")
#                 self.query.stop()
#                 logger.info("Streaming query stopped")

#             if self.spark:
#                 logger.info("Stopping Spark session...")
#                 self.spark.stop()
#                 logger.info("Spark session stopped")
#         except Exception as e:
#             logger.error(f"Error during shutdown: {e}")

#     def test_kafka_connection(self):
#         try:
#             logger.info("Testing Kafka connection...")
#             test_df = self.spark.read \
#                 .format("kafka") \
#                 .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
#                 .option("subscribe", self.kafka_topic) \
#                 .option("startingOffsets", "earliest") \
#                 .option("endingOffsets", "latest") \
#                 .load()

#             count = test_df.count()
#             logger.info(f"Kafka connection successful. Found {count} messages in topic '{self.kafka_topic}'")
#             return True
#         except Exception as e:
#             logger.error(f"Kafka connection failed: {e}")
#             return False

#     def start_streaming_with_postgres(self, table_name="events"):
#         """Start streaming with PostgreSQL sink"""
#         try:
#             logger.info("Starting streaming with PostgreSQL integration...")

#             # Define location schema for nested JSON
#             location_schema = StructType([
#                 StructField("country", StringType(), True),
#                 StructField("city", StringType(), True),
#             ])

#             # Define main schema matching producer output exactly
#             schema = StructType([
#                 StructField("event_id", StringType(), True),
#                 StructField("user_id", IntegerType(), True),
#                 StructField("product", StringType(), True),
#                 StructField("action", StringType(), True),
#                 StructField("timestamp", StringType(), True),
#                 StructField("session_id", StringType(), True),
#                 StructField("price", DoubleType(), True),
#                 StructField("quantity", IntegerType(), True),
#                 StructField("category", StringType(), True),
#                 StructField("location", location_schema, True),
#             ])

#             df = self.spark.readStream \
#                 .format("kafka") \
#                 .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
#                 .option("subscribe", self.kafka_topic) \
#                 .option("startingOffsets", "latest") \
#                 .option("failOnDataLoss", "false") \
#                 .load()

#             # First, let's see the raw JSON structure to debug
#             raw_json_df = df.selectExpr("CAST(value AS STRING) as json_str")
            
#             # Try to parse with schema, but also show raw JSON for debugging
#             json_df = raw_json_df \
#                 .withColumn("data", from_json(col("json_str"), schema)) \
#                 .select("data.*", "json_str") \
#                 .filter(col("event_id").isNotNull())

#             def write_batch_to_postgres(batch_df, batch_id):
#                 try:
#                     count = batch_df.count()
#                     if count > 0:
#                         logger.info(f"Processing batch {batch_id} with {count} records")
                        
#                         # Debug: Show actual schema received
#                         logger.info("Actual DataFrame schema:")
#                         batch_df.printSchema()
                        
#                         # Debug: Show sample raw JSON if available
#                         if "json_str" in batch_df.columns:
#                             logger.info("Sample raw JSON:")
#                             batch_df.select("json_str").show(2, truncate=False)
                        
#                         # Debug: Show sample raw data
#                         logger.info("Sample parsed records:")
#                         batch_df.drop("json_str").show(2, truncate=False)
                        
#                         # Check if we have all required columns
#                         available_columns = batch_df.columns
#                         logger.info(f"Available columns: {available_columns}")
                        
#                         # Transform data to match PostgreSQL table schema
#                         working_df = batch_df.drop("json_str") if "json_str" in batch_df.columns else batch_df
                        
#                         if "location" in working_df.columns:
#                             # Handle nested location structure
#                             transformed_df = working_df \
#                                 .withColumn("country", col("location.country")) \
#                                 .withColumn("city", col("location.city")) \
#                                 .withColumn("timestamp", to_timestamp(col("timestamp"))) \
#                                 .withColumn("created_at", current_timestamp()) \
#                                 .drop("location")
#                         else:
#                             # Location already flattened or columns already exist
#                             transformed_df = working_df \
#                                 .withColumn("timestamp", to_timestamp(col("timestamp"))) \
#                                 .withColumn("created_at", current_timestamp())
                        
#                         # Debug: Show columns after transformation
#                         logger.info(f"Columns after transformation: {transformed_df.columns}")
                        
#                         # Instead of trying to select specific columns that might not exist,
#                         # let's just use what we have and let PostgreSQL handle any missing columns
#                         final_df = transformed_df
                        
#                         # If we have more columns than needed, we can drop unnecessary ones
#                         # but let's keep all the columns we have for now
#                         logger.info(f"Using all available columns: {final_df.columns}")

#                         logger.info("Final transformed records:")
#                         final_df.show(5, truncate=False)

#                         # Write to PostgreSQL
#                         final_df.write \
#                             .format("jdbc") \
#                             .option("url", "jdbc:postgresql://postgres_streaming:5432/streaming_db") \
#                             .option("dbtable", table_name) \
#                             .option("user", "postgres") \
#                             .option("password", "postgres") \
#                             .option("driver", "org.postgresql.Driver") \
#                             .mode("append") \
#                             .save()

#                         logger.info(f"Batch {batch_id} written to PostgreSQL successfully")
#                     else:
#                         logger.info(f"Batch {batch_id} was empty, skipping")
#                 except Exception as e:
#                     logger.error(f"Error processing batch {batch_id}: {e}")
#                     import traceback
#                     traceback.print_exc()
#                     raise

#             postgres_checkpoint = f"{self.checkpoint_location}/postgres_{table_name}"
#             os.makedirs(postgres_checkpoint, exist_ok=True)

#             self.query = json_df.writeStream \
#                 .foreachBatch(write_batch_to_postgres) \
#                 .outputMode("append") \
#                 .option("checkpointLocation", postgres_checkpoint) \
#                 .trigger(processingTime='30 seconds') \
#                 .start()

#             logger.info("PostgreSQL streaming started successfully")
#             self.query.awaitTermination()

#         except Exception as e:
#             logger.error(f"PostgreSQL streaming failed: {e}")
#             import traceback
#             traceback.print_exc()
#             raise
#         finally:
#             self.stop_streaming()

# if __name__ == "__main__":
#     KAFKA_SERVERS = "kafka:9092"
#     KAFKA_TOPIC = "streaming_data"
#     CHECKPOINT_DIR = "/tmp/checkpoint"

#     logger.info("Starting Kafka-Spark Streaming Application")
#     logger.info(f"Kafka servers: {KAFKA_SERVERS}")
#     logger.info(f"Kafka topic: {KAFKA_TOPIC}")
#     logger.info(f"Checkpoint location: {CHECKPOINT_DIR}")

#     try:
#         streaming_app = KafkaSparkStreaming(
#             kafka_bootstrap_servers=KAFKA_SERVERS,
#             kafka_topic=KAFKA_TOPIC,
#             checkpoint_location=CHECKPOINT_DIR
#         )

#         # Test Kafka connection before starting streaming
#         if streaming_app.test_kafka_connection():
#             streaming_app.start_streaming_with_postgres()
#         else:
#             logger.error("Kafka connection test failed, exiting...")
#             sys.exit(1)

#     except KeyboardInterrupt:
#         logger.info("Application interrupted by user")
#     except Exception as e:
#         logger.error(f"Application failed: {e}")
#         import traceback
#         traceback.print_exc()
#         sys.exit(1)
#     finally:
#         logger.info("Application shutdown complete")


"""
Fixed Spark Streaming Job with proper schema handling
"""

import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp, when, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FixedSparkStreamingApp:
    def __init__(self):
        self.spark = None
        self.query = None
        
        # Define the expected JSON schema
        self.json_schema = StructType([
            StructField("event_id", StringType(), True),
            StructField("user_id", IntegerType(), True),
            StructField("product", StringType(), True),
            StructField("action", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("session_id", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("quantity", IntegerType(), True),
            StructField("category", StringType(), True),
            StructField("location", StructType([
                StructField("country", StringType(), True),
                StructField("city", StringType(), True)
            ]), True)
        ])
        
        # Define the final output schema for PostgreSQL
        self.output_columns = [
            "event_id", "user_id", "product", "action", "timestamp",
            "session_id", "price", "quantity", "category",
            "country", "city", "created_at"
        ]

    def create_spark_session(self):
        """Create Spark session with required configurations"""
        try:
            self.spark = SparkSession.builder \
                .appName("FixedStreamingApp") \
                .config("spark.jars.packages", 
                       "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.postgresql:postgresql:42.2.27") \
                .config("spark.sql.adaptive.enabled", "true") \
                .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
                .getOrCreate()
            
            self.spark.sparkContext.setLogLevel("WARN")
            logger.info("Spark session created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create Spark session: {e}")
            return False

    def transform_data(self, df, batch_id):
        """Transform the streaming data with proper error handling"""
        try:
            logger.info(f"Processing batch {batch_id} with {df.count()} records")
            
            # Step 1: Parse JSON data
            parsed_df = df.select(
                from_json(col("value").cast("string"), self.json_schema).alias("data")
            ).select("data.*")
            
            logger.info("JSON parsing completed")
            parsed_df.printSchema()
            
            # Step 2: Extract location fields and add timestamp
            transformed_df = parsed_df.select(
                col("event_id"),
                col("user_id"),
                col("product"),
                col("action"),  # Make sure this column exists
                col("timestamp"),
                col("session_id"),
                col("price"),
                col("quantity"),
                col("category"),
                col("location.country").alias("country"),
                col("location.city").alias("city"),
                current_timestamp().alias("created_at")
            )
            
            logger.info("Data transformation completed")
            
            # Step 3: Validate schema before writing
            available_columns = transformed_df.columns
            missing_columns = [col for col in self.output_columns if col not in available_columns]
            
            if missing_columns:
                logger.error(f"Missing columns in transformed data: {missing_columns}")
                logger.info(f"Available columns: {available_columns}")
                return
            
            # Step 4: Write to PostgreSQL
            self.write_to_postgresql(transformed_df, batch_id)
            
        except Exception as e:
            logger.error(f"Error processing batch {batch_id}: {e}")
            import traceback
            traceback.print_exc()

    def write_to_postgresql(self, df, batch_id):
        """Write DataFrame to PostgreSQL with proper error handling"""
        try:
            # PostgreSQL connection properties
            postgres_properties = {
                "user": "postgres",
                "password": "postgres",
                "driver": "org.postgresql.Driver",
                "stringtype": "unspecified"
            }
            
            postgres_url = "jdbc:postgresql://postgres_streaming:5432/streaming_db"
            
            # Show sample data before writing
            logger.info("Sample data to be written:")
            df.show(5, truncate=False)
            
            # Write to PostgreSQL
            df.write \
                .mode("append") \
                .jdbc(postgres_url, "events", properties=postgres_properties)
            
            logger.info(f"Successfully wrote batch {batch_id} to PostgreSQL")
            
        except Exception as e:
            logger.error(f"Error writing batch {batch_id} to PostgreSQL: {e}")
            raise

    def start_streaming(self):
        """Start the streaming application"""
        try:
            if not self.create_spark_session():
                return False
            
            # Read from Kafka
            kafka_df = self.spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "kafka:9092") \
                .option("subscribe", "streaming_data") \
                .option("startingOffsets", "latest") \
                .option("failOnDataLoss", "false") \
                .load()
            
            logger.info("Kafka stream created successfully")
            
            # Start the streaming query
            self.query = kafka_df.writeStream \
                .foreachBatch(self.transform_data) \
                .option("checkpointLocation", "/tmp/checkpoint") \
                .trigger(processingTime="10 seconds") \
                .start()
            
            logger.info("Streaming query started successfully")
            
            # Wait for termination
            self.query.awaitTermination()
            
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            return False
        
        finally:
            if self.spark:
                logger.info("Stopping Spark session...")
                self.spark.stop()
                logger.info("Spark session stopped")

def main():
    """Main function"""
    app = FixedSparkStreamingApp()
    
    try:
        logger.info("Starting Fixed Spark Streaming Application...")
        success = app.start_streaming()
        
        if success:
            logger.info("Application completed successfully")
        else:
            logger.error("Application failed")
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed: {e}")
    finally:
        logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()