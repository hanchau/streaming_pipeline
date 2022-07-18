from app.pipeline import pipeline
from utils.logger import Logger


@pipeline.task(queue="kafka_to_extractors")
def extractor(consumer):
    for msg in consumer.consume():
        print(msg)
        pipeline.send_task('tasks.transformer', (msg))


@pipeline.task(queue="extractors_to_transformers")
def transformer(msg):
    print(f"Transformer receieved - [{msg}]")
    pipeline.send_task('tasks.loader', (msg))


@pipeline.task(queue="transformers_to_loaders")
def loader(msg):
    print(f"Loader receieved - [{msg}]")
