from kafka import KafkaProducer
import json
import time
import random

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
)

def send_location_updates(driver_id):
    print("Producer starting...")
    while True:
        location = {
            "driver_id": driver_id,
            "latitude": round(random.uniform(40.0, 41.0), 6),
            "longitude": round(random.uniform(-74.0, -73.0), 6),
            "timestamp": time.time()
        }
        
        # .get(timeout=10) ensures we wait for a server acknowledgement
        # If this lines crashes, you know the Producer can't reach the Broker
        try:
            future = producer.send('driver-location', location)
            result = future.get(timeout=10) 
            print(f"Sent to partition {result.partition} at offset {result.offset}: {location}")
        except Exception as e:
            print(f"Error sending message: {e}")
            
        time.sleep(5)

# Start sending updates for driver_id = 101
send_location_updates(driver_id=101)