import requests
import json
import time
from confluent_kafka import Producer

# OpenWeather API Key and Kafka Configuration
api_key = '5da0d448b41b9bf704520a7460772814'
producer_conf = {'bootstrap.servers': 'kafka-cluster-kafka-external-bootstrap:29092'}
weather_topic = 'current-weather'  # Set your Kafka topic name
producer = Producer(producer_conf)

# Function to get weather data from OpenWeather API
def get_current_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extracting necessary data
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
        return weather_data
    else:
        print(f"Error fetching weather data for {city}")
        return None

# Kafka Producer Delivery Callback
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Function to produce weather data to Kafka topic
def produce_weather_data(api_key, city, producer, topic):
    weather_data = get_current_weather_data(api_key, city)
    if weather_data:
        try:
            json_data = json.dumps(weather_data)
            producer.produce(topic, value=json_data, callback=delivery_report)
            producer.flush()
        except Exception as e:
            print(f"Error producing message: {e}")

# Main Program
if __name__ == "__main__":
    city = 'edmonton' #input('Enter city name: ')
    
    # Run the loop to send data every 1 minute
    while True:
        print(f"Fetching and sending weather data for {city}...")
        produce_weather_data(api_key, city, producer, weather_topic)
        
        # Wait for 1 minute (60 seconds)
        time.sleep(60)