import json
import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_kafka_producer(bootstrap_servers="kafka:9092", topic="streaming_data"):
    """Test Kafka producer"""
    try:
        logger.info("Testing Kafka producer...")
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        
        # Send test message
        test_message = {
            "event_id": "test-001",
            "user_id": 12345,
            "product": "test-product",
            "price": 99,
            "location": "test-location",
            "timestamp": str(int(time.time()))
        }
        
        future = producer.send(topic, value=test_message, key="test-key")
        result = future.get(timeout=10)
        
        logger.info(f"Message sent successfully: {result}")
        producer.close()
        return True
        
    except Exception as e:
        logger.error(f"Producer test failed: {e}")
        return False

def test_kafka_consumer(bootstrap_servers="kafka:9092", topic="streaming_data"):
    """Test Kafka consumer"""
    try:
        logger.info("Testing Kafka consumer...")
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            consumer_timeout_ms=10000,
            auto_offset_reset='latest'
        )
        
        logger.info("Waiting for messages...")
        message_count = 0
        
        for message in consumer:
            logger.info(f"Received: {message.value}")
            message_count += 1
            if message_count >= 5:  # Stop after 5 messages
                break
                
        consumer.close()
        logger.info(f"Consumer test completed. Received {message_count} messages")
        return True
        
    except Exception as e:
        logger.error(f"Consumer test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting Kafka connectivity tests...")
    
    # Test producer
    if test_kafka_producer():
        logger.info("✓ Producer test passed")
    else:
        logger.error("✗ Producer test failed")
    
    time.sleep(2)
    
    # Test consumer
    if test_kafka_consumer():
        logger.info("✓ Consumer test passed")
    else:
        logger.error("✗ Consumer test failed")
