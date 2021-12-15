# Kakfa - Spark Streaming - Cassandra Community Application
-----------------------------------------------------------
### Prerequisites:

* Install java.   > java website
* Install python. > python website
* Install kafka.  > kafka official website -- download the tar file.
* Install spark.  > spark official website -- download the tar file.
* Install cassandra. > cassandra official website -- download the tar file.
* Create a virtual environment. > python3 -m venv [env_name]
* Activate the virtual environment > source env_name/bin/activate
* Install required python packages. > pip install -r requirements.txt


### Setup cassandra database:
-----------------------------
#### Navigate to the extracted cassandra folder and run the below commands.
* Start cassandra server -
``` $ bin/cassandra ```

* Start cassandra shell -
``` $ bin/cqlsh ```

#### Cassandra Query Language basic commands

```
Source : ![Cassandra Installation] (https://cassandra.apache.org/doc/latest/cassandra/getting_started/installing.html) 

Python-Cassandra driver : ![Python-Cassandra-Quickstart](https://cassandra.apache.org/doc/latest/cassandra/getting_started/installing.html)

```

- Keyspace  ==  Database,   Installation  ==  Node 

* Look at all keyspaces.
``` $ select * from system_schema.keyspaces; ```
``` $ describe keyspaces; ```

* create a key space.

```
 $ CREATE KEYSPACE community_app
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy', 
   'replication_factor' : 1 
  };
```

* select a key space.
``` $ use [keyspace_name] ```

* Look at all tables.
``` $ desc tables; ```

* Describe a particular table.
``` $ desc table [table_name]; ```

* Create a table.
``` 
$ create table tag_like_count (
	id  text PRIMARY KEY,
	tags text,
	count int); 
```

* Insert records in the table.
``` 
$ INSERT INTO store.shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('9876', 2, toTimeStamp(now())); 
```

* Look at records inserted in the table.
``` $ select * from [table_name]; ```


### Run the application:
------------------------
#### Navigate inside extracted kafka folder and run the below commands.
* Start zookeeper - 
``` $ bin/zookeeper-server-start.sh config/zookeeper.properties ```

* Start kafka server - 
``` $ bin/kafka-server-start.sh config/server.properties ```

#### Run the below python files.
* Start kafka producer - 
``` $ python kafka_producer.py ```

* Start kafka consumer - 
``` $ python kafka_consumer.py ```

#### Navigate to the extracted spark folder and run the below command.
* Run a spark-submit job -
``` 
$ ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
  --master local ~/Desktop/stream_assignment/stream/om/spark_analysis.py 100 
```

#### Check the analysis and visulisation 
* Run the python visualisation program -
``` $ python visualisation.py ```

