from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    return {
        "sensor_id": random.randint(1, 5),
        "timestamp": int(time.time()),
        "temperature": round(random.uniform(20.0, 35.0), 2)
    }

while True:
    data = generate_sensor_data()
    producer.send("sensor-data", value=data)
    print("Produced:", data)
    time.sleep(1)
