from kafka import KafkaProducer
from datetime import datetime
import requests
import time
import json
import configparser
import random

# read from config file.
# source : https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read('config.ini')

# get kafka meta data information.
KAFKA_TOPIC_NAME = config.get("KAFKA_PRODUCER", "KAFKA_POST_TOPIC_NAME")
KAFKA_BOOTSTRAP_SERVERS = config.get("KAFKA_PRODUCER", "KAFKA_BOOTSRAP_SERVER")

# get random quote by hitting the url.
# source : https://github.com/lukePeavey/quotable 
REQUEST_URL = config.get("KAFKA_PRODUCER", "POST_URL")
NUM_POSTS = int(config.get("KAFKA_PRODUCER", "NUM_POSTS_TO_READ"))

def display_post(post):
    """
    Display the post and it's attributes.

    Parameters:
    ----------
    post : it is the post created by an user.
    """      
    # adding a few attributes to the user post
    post["posted_time"] = datetime.now()
    post["likes"] = random.randint(1, 1000)
    post["shares"] = random.randint(1, 50) 

    print("Attributes present :  ",  post.keys())
    for key, value in post.items():
        print(key, value, sep="\t")


def push_messages():
    """
    Initiate a kafka producer and push the messages to a topic.
    """
    # source : https://kafka-python.readthedocs.io/en/master/
    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                   value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    print("-"*100, "Demo post structure...", "-"*100, sep="\n")

    post = dict(requests.get(REQUEST_URL).json())
    display_post(post)

    for i in range(1, NUM_POSTS):
        print("User adding a post : " + str(i))
        event_datetime = datetime.now()

        post = dict(requests.get(REQUEST_URL).json())
        # adding a few attributes to the user post
        post["likes"] = random.randint(1, 1000)
        post["shares"] = random.randint(1, 50) 
        post["posted_time"] = event_datetime.strftime("%Y-%m-%d %H:%M:%S")
        post["tags"] = post["tags"][0]

        print("Message posted : ", post)
    
        # source : https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
        # post_json = json.dumps(post, indent=4, sort_keys=True, default=str)
        kafka_producer.send(KAFKA_TOPIC_NAME, post)
        time.sleep(1)


if __name__ == "__main__":
    print("Started kafka producer....")

    try:
        # initiate the kafka producer.
        push_messages()

    except Exception as ex:
        print("Failed to push kafka messages..")
        print("Exception occured : ", ex)

