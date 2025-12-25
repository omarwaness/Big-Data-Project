from kafka import KafkaProducer
import json
import time
import random

# Kafka Producer
def create_kafka_producer():
    time.sleep(10)
    return KafkaProducer(
        bootstrap_servers=['kafka:29092'],
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')  # Serialize data to JSON
    )

def send_to_kafka(producer, topic: str, data: dict):
    """
    Sends JSON data to a specific Kafka topic.
    """
    print(f"Streaming to {topic}...")
    try:
        future = producer.send(topic, value=data)
        result = future.get(timeout=10)
        print(f"✔️ Message delivered to {topic} [Partition: {result.partition}, Offset: {result.offset}]")
        return True
    except Exception as e:
        print(f"❌ Error streaming to Kafka: {e}")
        return False
                                                                                                                       