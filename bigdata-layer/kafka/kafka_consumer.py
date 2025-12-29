import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from hdfs import InsecureClient

KAFKA_BROKER = 'kafka:29092'
HDFS_URL = 'http://master:9870'
HDFS_USER = 'root'
TOPICS = ['farm-weather', 'farm-forecast', 'farm-soil']

# 1. Initialize HDFS Client
hdfs_client = InsecureClient(HDFS_URL, user=HDFS_USER)

def get_consumer():
    """Try to connect to Kafka until successful."""
    while True:
        try:
            consumer = KafkaConsumer(
                *TOPICS,
                bootstrap_servers=[KAFKA_BROKER],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='hdfs-writer-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("✅ Consumer connected to Kafka")
            return consumer
        except NoBrokersAvailable:
            print("⏳ Waiting for Kafka brokers...")
            time.sleep(5)

def write_to_hdfs(topic, data):
    """Appends data to HDFS in JSON Lines format."""
    folder_path = f'/farm/{topic}'
    file_path = f'{folder_path}/data.jsonl'
    
    # Ensure folder exists
    if not hdfs_client.content(folder_path, strict=False):
        hdfs_client.makedirs(folder_path)

    # Prepare data (JSON string + newline)
    row = json.dumps(data, default=str) + "\n"
    
    try:
        # Check if file exists
        if hdfs_client.content(file_path, strict=False):
            # Use write with append=True instead of .append()
            hdfs_client.write(file_path, row, append=True, encoding='utf-8')
        else:
            hdfs_client.write(file_path, row, encoding='utf-8')
        print(f"✔️ Saved to HDFS: {topic}")
    except Exception as e:
        print(f"❌ HDFS Write Error: {e}")

# 2. Start Consuming
if __name__ == "__main__":
    print("🚀 HDFS Consumer Service Starting...")
    consumer = get_consumer()
    
    for message in consumer:
        topic = message.topic
        data = message.value
        write_to_hdfs(topic, data)