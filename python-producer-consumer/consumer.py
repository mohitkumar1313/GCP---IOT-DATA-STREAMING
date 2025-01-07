import json
from confluent_kafka import Consumer, KafkaException, KafkaError
import os
from pymongo import MongoClient

# MongoDB connection details (from environment variables)
MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')  # from kubernetes manifest
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD') 
#MONGO_URI = f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongo-nodeport-svc:27017/?authSource=admin'
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://adminuser:password123@mongo-nodeport-svc:27017/?authSource=admin') 
MONGO_DB = os.getenv('MONGO_DB', 'weather_db')  # MongoDB Database name
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'weather_data')  # MongoDB Collection name

# Kafka Configuration
# Kafka Configuration
consumer_conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVER', 'kafka-cluster-kafka-bootstrap.default.svc.cluster.local:9092'),  # Use env variable or default to internal listener
    'group.id': 'weather-consumer-group',           # Consumer group ID
    'auto.offset.reset': 'earliest'                 # Start reading from the earliest message if no offset is stored
}


# Create Kafka Consumer instance
consumer = Consumer(consumer_conf)

# MongoDB client setup
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Function to handle the incoming message and store it in MongoDB
def handle_message(msg):
    try:
        # Decode the message value from bytes to JSON
        weather_data = json.loads(msg.value().decode('utf-8'))

        # Process the weather data (example: print the weather data)
        print(f"Received weather data for {weather_data['city']}:")
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Description: {weather_data['description']}")
        print("-" * 50)

        # Insert the weather data into MongoDB
        store_data_in_mongo(weather_data)

    except Exception as e:
        print(f"Error processing message: {e}")

# Function to store weather data into MongoDB
def store_data_in_mongo(weather_data):
    try:
        # Insert the weather data into MongoDB
        collection.insert_one(weather_data)
        print(f"Data for {weather_data['city']} inserted into MongoDB.")
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")

# Subscribe to the 'current-weather' topic
consumer.subscribe(['current-weather'])

# Polling loop to keep the consumer running
try:
    while True:
        # Poll for messages (timeout is set to 1 second)
        msg = consumer.poll(timeout=1.0)

        # Check if message is None (no new messages)
        if msg is None:
            continue

        # Check if there's an error with the message
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition reached: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Handle valid message
            handle_message(msg)

except KeyboardInterrupt:
    print("Consumer interrupted by user.")

finally:
    # Close the consumer connection
    consumer.close()
