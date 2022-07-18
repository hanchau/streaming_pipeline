from gc import callbacks
from confluent_kafka import Consumer, Producer, KafkaError
from datetime import datetime
import time


class Kafka:

    def __init__(self, kwargs):
        self.conf = {
            'bootstrap.servers': kwargs['servers'],
            'group.id': kwargs['group_id'],
            'auto.offset.reset': kwargs['offset_reset']
            }
        self.logger = kwargs['logger']


class KafkaProducer(Kafka):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.producer = Producer(self.conf)

    def produce(self, topic, msg):
        def acked(err, msg):
            if err is not None:
                self.logger.error(f"Failed to deliver message: {msg}: {err}")
            else:
                self.logger.info(f"Message produced: {msg}")
        self.producer.produce(topic, key=f"{datetime.now()}", value=msg, callback=acked)


class KafkaConsumer(Kafka):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([kwargs['topic']])

    def consume_one(self):
        try:
            import pdb; pdb.set_trace()
            msg = self.consumer.poll(timeout=1.0)
            if msg is None: 
                return

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    self.logger.error(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                elif msg.error():
                    self.logger.error(msg.error())
            else:
                self.consumer.close()
                return msg.key(), msg.value()
        except Exception as err:
            self.logger.error(err)


    def consume(self):
        while True:
            try:
                msg = self.consumer.poll()
                if msg is None: 
                    time.sleep(1)
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        self.logger.error(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                    elif msg.error():
                        self.logger.error(msg.error())
                else:
                    yield {"key": str(msg.key()), "value": str(msg.value())}
            except Exception as err:
                self.logger.error(err)
                yield None

    def close_consumer(self):
        try:
            self.consumer.close()
        except Exception as err:
            self.logger.error(err)
