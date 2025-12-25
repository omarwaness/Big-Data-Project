from kafka import KafkaConsumer
import json

# Kafka Consumer
consumer = KafkaConsumer(
    'driver-location',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start from the earliest message
    enable_auto_commit=True,
    group_id='location-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize data from JSON
)

def process_location_updates():
    print("Waiting for location updates...")
    for message in consumer:
        print(f"Received: {message.value}")

# Start consuming location updates
process_location_updates()