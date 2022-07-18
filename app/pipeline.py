from celery import Celery
from kombu import Queue

pipeline = Celery('tasks', broker='redis://127.0.0.1:6379/'
,backend='redis://127.0.0.1:6379/1'
,include=['tasks.tasks']
)



pipeline.conf.task_default_queue = 'default'
pipeline.conf.task_queues = (
    Queue('kafka_to_extractors'),
    Queue('extractors_to_transformers'),
    Queue('transformers_to_loaders')
)

# consumer.conf.task_routes = {'workers.all_tasks.sum_list': {'queue': 'sum_list_only'}}
