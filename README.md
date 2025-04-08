# kafka-docker-example

Very simple example of docker composing Kafka (& related services) with an example Python
consumer & producer to communicate with the docker composed Kafka cluster.

This example just serializes & deserializes data as utf-8 encoded bytes. A more
sophisticated use case may use avro serialization & communicate with a schema registry
which is not covered here.

## How to Run

Create & activate the virtual environment for the example:
* `python -m venv kafka-docker-example`
* `source kafka-docker-example/bin/activate`
* `pip install -r requirements.txt`

Run the scripts:
1. Start the Kafka infrastructure with `docker compose up`
2. Wait for the services to initialise (for the broker to show healthy)
3. Run the producer with `python produce.py` - observe the logs that messages were produced
successfully onto the Kafka topic.
4. Run the consumer with `python consume.py` - observe the logs that messages were consumed
successfully from the kafka topic.
5. (Optionally) Check out the control center (`http://localhost:9021/` in your browser) to see
the topics created and some metrics re. message production & consumption on those topics.
