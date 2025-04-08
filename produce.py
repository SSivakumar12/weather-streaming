import logging
import time
import random
import json
import pandas as pd
import numpy as np
from confluent_kafka import Producer

logger = logging.getLogger("example-producer")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
)

producer_config = {
    "bootstrap.servers": "localhost:9092",
}

logger.info("Creating producer...")
producer = Producer(producer_config)

data = pd.read_csv("data/city_1_weather_data.csv")
# random generate topics for cities
topics = ["city-topic-1", "city-topic-2", "city-topic-3", "city-topic-4"]

for _, row in data.iterrows():
    topic = random.choice(topics)
    message = json.dumps({**row.to_dict(), "topic": topic})
    logger.info(f"Producing message {message} for topic {topic}...")
    producer.produce(topic, message.encode("utf-8"))
    time.sleep(0.1) # simulate delay in recieval of data

logger.info("Flushing producer")
producer.flush()
