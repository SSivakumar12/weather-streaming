import logging
import json
import os
import traceback
from confluent_kafka import Consumer, KafkaException
from elasticsearch import Elasticsearch

logger = logging.getLogger("example-consumer")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
)

consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "exampleGroup",
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
}

topic = ["city-topic-1", "city-topic-2", "city-topic-3", "city-topic-4"]
logger.info(f"Creating consumer for broker {consumer_config['bootstrap.servers']}")
consumer = Consumer(consumer_config)
logger.info(f"Subscribing consumer to topics: {topic}")
consumer.subscribe(topic)

# Connect to Elasticsearch instance
es = Elasticsearch("http://localhost:9200/")
INDEX_NAME = "weather-data"

mapping = {
    "mappings": {
        "properties": {
            # "Date/Time": {"type": "text"},
            "Temp_C": {"type": "float"},
            # "Dew Point Temp_C": {"type": "float"},
            # "Rel Hum_%": {"type": "integer"},
            # "Wind Speed_km/h": {"type": "integer"},
            # "Visibility_km": {"type": "float"},
            # "Press_kPa": {"type": "float"},
            "Weather": {"type": "text"},
            "topic": {"type": "text"},

        }
    }
}

# Create the index with the mapping
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=mapping)
    logger.info(f"Index '{INDEX_NAME}' created with the specified mapping.")


try:
    result = []
    while True:
        message = consumer.poll(timeout=2.0)
        if message is None:
            logger.info("No messages found...")

        else:
            value = message.value()
            data = json.loads(value.decode('utf-8'))
            result.append(data)
            res = es.index(index=INDEX_NAME, body=result)
            result = []
            # Insert data into Elasticsearch in bulk
            
            # if len(result) >= 20:
            #     # print(result, type(result), type(result[0]))
            #     res = es.index(index=INDEX_NAME, body=result)
            #     logger.info("bulk data inserted into elasticsearch.")
            #     result = []  # clear the list for next batch of inserts.
            #     if res['result']!='created':
            #         logger.error(f"Failed to insert batch of data into elasticsearch, response: {res}")
                

except Exception as e:
    logging.error(f"some error occured, stopping proces {e}")
    logging.error(f"{traceback.format_exc()}")

finally:
    logger.info("Committing offset & closing consumer...")
    try:
        consumer.commit(asynchronous=False)
    except KafkaException as err:
        logger.error(err)
    consumer.close()
