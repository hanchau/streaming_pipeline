#### One for All
```
The purpose of this project is to create a Kafka consumer, which can consume from all the topics.
```


##### How?
- [X] Create a folder structure
- [X] Setup the proper environment
- [X] Write a simple consumer module
- [ ] Use celery to spawn multiple consumer eventlets
- [ ] Add feature of spawning eventlets in runtime
- [ ] Add feature of configuring the topics
- [ ] Add feature of configuring the schemas for each topic




##### Cheat Sheet
```console
$ # Kafka UI 
$ docker run -p 8081:8080 \
	-e KAFKA_CLUSTERS_0_NAME=kafka-broker-cluster \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka-broker:9092 \
	-d provectuslabs/kafka-ui:latest 
```


##### Design
  1. Debezium setup on the MySQL server
  2. Pushing records from binlogs to Kafka Topics
  3. Celery application oneforall running, polling recrods from all the topics
  4. For every topic there's a separate celery-eventlet
  5. All eventlets sending fetched records to transformer workers (fire & forget)
  6. The transformer workers sending the processed records to uploader - a celery-eventlet
  7. Which pushes these records to warehouse.