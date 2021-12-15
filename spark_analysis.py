from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from cassandra.cluster import Cluster
import time
import configparser

# read from config file.
# source : https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read('/Users/i518758/Desktop/stream_assignment/stream/om/config.ini')

# get kafka meta data information.
KAFKA_TOPIC_NAME = config.get("SPARK_CONNECTER", "KAFKA_POST_TOPIC_NAME")
KAFKA_BOOTSTRAP_SERVERS = config.get("SPARK_CONNECTER", "KAFKA_BOOTSRAP_SERVER")

GLOBAL_COUNTER = 1

def start_spark_session():
    """
    Start spark session and process streaming data.
    """
    # source : https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.SparkSession.html
    spark = SparkSession \
            .builder \
            .appName("Community Streaming Application") \
            .master("local[*]") \
            .getOrCreate()

    print("Spark session is created.")

    # set logging level
    spark.sparkContext.setLogLevel("ERROR")

    # receive data from kafka topic and process them.
    process_data(spark)


def process_data(spark):
    """
    Read streaming data from kafka topic and process them.

    Parameters:
    -----------
    spark : created spark session.
    """
    posts_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC_NAME) \
        .option("startingOffsets", "latest") \
        .load()

    print("Schema of created posts data frame : ")
    posts_df.printSchema()

    posts_df1 = posts_df.selectExpr("CAST(value AS STRING)", "timestamp")

    posts_schema = StructType() \
        .add("_id", StringType()) \
        .add("author", StringType()) \
        .add("authorSlag", StringType()) \
        .add("content", StringType()) \
        .add("dateAdded", StringType()) \
        .add("dateModified", StringType()) \
        .add("length", StringType()) \
        .add("likes", StringType()) \
        .add("shares", StringType()) \
        .add("posted_time", StringType()) \
        .add("tags", StringType()) 


    posts_df2 = posts_df1 \
        .select(from_json(col("value"), posts_schema) \
        .alias("posts"), "timestamp")

    posts_df3 = posts_df2.select("posts.*", "timestamp")

    # Aggregation of likes and shares
    posts_df4 = posts_df3.groupBy("tags") \
        .agg({"likes" : 'sum'}) \
        .select("tags", col("sum(likes)").alias("sum_likes")) \
        .alias("total_number_of_likes")

    posts_df4.printSchema()

    query = posts_df4 \
        .writeStream \
        .trigger(processingTime="5 seconds") \
        .outputMode("update") \
        .option("truncate", "false") \
        .foreachBatch(save_row).start()  

    posts_agg_write_stream = posts_df4 \
        .writeStream \
        .trigger(processingTime="5 seconds") \
        .outputMode("update") \
        .option("truncate", "false") \
        .format("console") \
        .start() 



    # tag_like_count_stream =  posts_df4.write\
    #     .format("org.apache.spark.sql.cassandra") \
    #     .mode('append') \
    #     .options(table="tag_like_count", keyspace="community_app") \
    #     .save()

    posts_agg_write_stream.awaitTermination()
    query.awaitTermination()

    print("Stream data processing completed.")


def save_row(df, epoch_id):
    print("om sai ram..sri pada rajam sarnam prapadye")
    global GLOBAL_COUNTER 
    GLOBAL_COUNTER = GLOBAL_COUNTER + 1
    print(epoch_id)
    print("Inserting rows")

    # source : https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/
    cluster = Cluster()
    session = cluster.connect('community_app')
    for row in df.rdd.collect():
        session.execute(
            """
            INSERT INTO tag_like_count (id, count, tags)
            VALUES (%s, %s, %s)   
            """, (str(GLOBAL_COUNTER), int(row.sum_likes), row.tags))



if __name__ == "__main__":
    try:
        print("Started spark streaming application....")
        print("Current timestamp : ", time.strftime("%Y-%m-%d %H:%M:%S"))

        start_spark_session()
    except Exception as e:
        print("Some exception occured in spark streaming ", e)
