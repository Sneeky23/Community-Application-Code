from kafka import KafkaConsumer
from json import loads
import configparser

# read from config file.
# source : https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read('config.ini')

# get kafka meta data information.
KAFKA_TOPIC_NAME = config.get("KAFKA_CONSUMER", "KAFKA_POST_TOPIC_NAME")
KAFKA_CONSUMER_GROUP_NAME = config.get("KAFKA_CONSUMER", "KAFKA_CONSUMER_GROUP_NAME")
KAFKA_BOOTSTRAP_SERVERS = config.get("KAFKA_PRODUCER", "KAFKA_BOOTSRAP_SERVER")


def pull_messages():
    """
    Pulls events from specified kafka topic.
    """
    # source : https://kafka-python.readthedocs.io/en/master/ 
    kafka_consumer = KafkaConsumer(
                KAFKA_TOPIC_NAME,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id=KAFKA_CONSUMER_GROUP_NAME,
                value_deserializer=lambda x: loads(x.decode('utf-8')))

    for event in kafka_consumer:
        post = event.value
        print("Message received: ", post)
    

if __name__ == "__main__":
    print("Started kafka consumer....")
    try:
        # initiating to pull messages from kafka topic.
        pull_messages()

    except Exception as ex:
        print("Failed to push kafka messages..")
        print("Exception occured : ", ex)