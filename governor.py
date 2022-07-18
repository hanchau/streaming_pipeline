from utils.logger import Logger
from tasks.tasks import extractor, transformer, loader
from celery import group

logger = Logger(logfile="logs/gov.log", _name="gov")

conf = {
        'servers': "localhost:9092",
        'group_id': "group3",
        'offset_reset': 'smallest',
        'logger': logger,
        }

topics = [ 'orders', 'transactions' ]

msg = """{1:2, 3:4, 5:6}"""

from connectors.kafka import KafkaConsumer, KafkaProducer

producer = KafkaProducer(conf)

eventlets = []
import pdb; pdb.set_trace()
for topic in topics:
        conf['topic'] = topic
        consumer = KafkaConsumer(conf)
        eventlets.append(extractor.s(consumer))


eventlets = group(eventlets)
res = eventlets.apply_async(serializer="pickle")
