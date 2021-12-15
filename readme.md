# SPA Assignement for WILP

# Kakfa - Spark Streaming - Cassandra Community Streaming Application
---------------------------------------------------------------------

1) User creates a post in real time (Data is being scraped using an api) --> 

# Github link to the api used : https://github.com/lukePeavey/quotable

# Actual post replica : https://api.quotable.io/random 

2) These posts are pushed by Kafka producer --> 
3) Read by kafka consumer --> 
4) Taken as input by spark streaming application -->
5) Perform some analytical operation on received data in spark in real time -->
6) Store the processed data in highly available cassandra database -->
7) Retreive the data from cassandra and perform some analysis.


## Contributors : 
```
1. Sanka Mahesh Sai
2. Snigdha Tarua
3. Chandra Sekhar Gupta Aravapalli
```
--- 
## Assignment Description :
<br />

1. Out of the two main workflows defined in Assignment 1
* Social Media Posts complete workflow 
* Messenger/Conversations between users/user groups . <br />
Choose any one workflow and implement it using open source Technologies such as 
Kafka, Spark, Flink etc. and in one programming language Python/Java. [6 Marks]

2. Create a streaming analytics pipeline and a dashboard that shows Realtime insights 
of the application.
Note: Based on your workflow decide what could be valuable data points you can 
gather and generate insights out of it. [6 Marks]

3. Submit both the codes 
* Of the working project
* Of the analytics pipeline <br />
Separately and Link of a short 5–10-minute video helping to understand how 
the integration between the different system subcomponent works. Proper flow 
needs to be shown between the different classes defined for the workflow and data 
pipeline. [3 Marks for the Video]
---
## Overview :

This is an example of building Kafka + Spark streaming application from scratch. 

When considering this project, we thought Twitter would be a great source of streamed data, plus it would be easy to peform simple transformations on the data. So for this example, we have :

1. Fake data twitter data generator
2. Create a stream of tweets that will be sent to a Kafka queue .
3. Pull the tweets from the Kafka cluster and perform analysis .
4. Save this data to a Cassandra table
---
## Architecture :

```
IoT devices --> Kafka --> Spark --> Cassandra  
```

To do this, we are going to set up an environment that includes :

* A single-node Kafka cluster
* A single-node Hadoop cluster
* Cassandra and Spark <br/>

Extract both the files.
spark version : spark-3.1.2-bin-hadoop3.2.tgz
kafka version : kafka-2.8.0-src.tgz

**Install Kafka :**

"Installing" Kafka is done by downloading the code from one of the several mirrors. After finding the latest binaries from the downloads page, choose one of the mirror sites and wget it into your home directory.

```

~$ tar -xvf kafka-2.8.0-src.tgz
~$ mv kafka-2.8.0-src.tgz kafka
~$ sudo apt install openjdk-8-jdk -y
~$ java -version
~$ pip3 install kakfa-python 
~$ pip3 list | grep kafka

```

**Install Spark :**

Download from https://spark.apache.org/downloads.html, make sure you choose the option for Hadoop 2.7 or later (unless you used and earlier version).

Unpack it, rename it

```
~$ tar -xvf Downloads/spark-3.1.2-bin-hadoop3.2.tgz
~$ mv spark-3.1.2-bin-hadoop3.2.tgz spark
~$ pip3 install pyspark
~$ pip3 list | grep spark
export PATH=$PATH:/home/<USER>/spark/bin
export PYSPARK_PYTHON=python3
~$ pyspark

Using Python version ....
SparkSession available as 'spark'.
>>> 

```
---
## Run code :

 
1. start zookeeper
``` 
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

2. start kafka server
```
$ bin/kafka-server-start.sh config/server.properties
```

3. pip install kafka-python

4. pip install pyspark

5. python producer.py

6. python consumer.py

7. Create tables in Cassandra

8. Navigate to spark extracted folder 

9. run spark-submit job

```
$ ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --master local ~/Desktop/stream_assignment/stream/om/trail_spark.py 100
```