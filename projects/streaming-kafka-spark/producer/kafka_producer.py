# producer/kafka_producer.py
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamingDataProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        self.topic = os.getenv('KAFKA_TOPIC', 'streaming_data')
        self.producer = None
        self.connect_to_kafka()
    
    def connect_to_kafka(self):
        """Connect to Kafka with retry mechanism"""
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=[self.bootstrap_servers],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: str(k).encode('utf-8') if k else None,
                    acks='all',
                    retries=3,
                    batch_size=16384,
                    linger_ms=10,
                    buffer_memory=33554432
                )
                logger.info(f"Successfully connected to Kafka at {self.bootstrap_servers}")
                return
            except Exception as e:
                retry_count += 1
                logger.error(f"Failed to connect to Kafka (attempt {retry_count}/{max_retries}): {e}")
                time.sleep(5)
        
        raise Exception("Failed to connect to Kafka after maximum retries")
    
    def generate_sample_data(self):
        """Generate sample streaming data"""
        user_ids = list(range(1, 1001))
        products = [
            'laptop', 'smartphone', 'tablet', 'headphones', 'keyboard',
            'mouse', 'monitor', 'camera', 'speaker', 'smartwatch'
        ]
        actions = ['view', 'click', 'purchase', 'add_to_cart', 'remove_from_cart']
        
        return {
            'event_id': f'evt_{int(time.time() * 1000)}_{random.randint(1000, 9999)}',
            'user_id': random.choice(user_ids),
            'product': random.choice(products),
            'action': random.choice(actions),
            'timestamp': datetime.utcnow().isoformat(),
            'session_id': f'session_{random.randint(100000, 999999)}',
            'price': round(random.uniform(10.0, 2000.0), 2),
            'quantity': random.randint(1, 5),
            'category': random.choice(['electronics', 'accessories', 'computers']),
            'location': {
                'country': random.choice(['US', 'UK', 'DE', 'FR', 'IN', 'JP']),
                'city': random.choice(['New York', 'London', 'Berlin', 'Paris', 'Mumbai', 'Tokyo'])
            }
        }
    
    def send_data(self, data, key=None):
        """Send data to Kafka topic"""
        try:
            future = self.producer.send(self.topic, value=data, key=key)
            record_metadata = future.get(timeout=10)
            logger.debug(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def start_streaming(self, interval=1):
        """Start streaming data continuously"""
        logger.info(f"Starting data stream to topic '{self.topic}' with {interval}s interval")
        
        try:
            while True:
                data = self.generate_sample_data()
                key = data['user_id']
                
                if self.send_data(data, key):
                    logger.info(f"Sent: {data['event_id']} - {data['action']} by user {data['user_id']}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Stopping data stream...")
        except Exception as e:
            logger.error(f"Error in streaming: {e}")
        finally:
            if self.producer:
                self.producer.close()
                logger.info("Producer closed")

def main():
    """Main function"""
    producer = StreamingDataProducer()
    
    # Start streaming with 1 second interval
    stream_interval = float(os.getenv('STREAM_INTERVAL', '1'))
    producer.start_streaming(interval=stream_interval)

if __name__ == "__main__":
    main()