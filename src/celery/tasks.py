from celery import Celery
import os

celery_app = Celery(
    'tasks',
    broker=f"pyamqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@rabbitmq//",
    backend='rpc://'
)


@celery_app.task
def add(a, b):
    return a + b
