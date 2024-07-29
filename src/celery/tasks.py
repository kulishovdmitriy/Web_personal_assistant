from celery import Celery
import os

celery_app = Celery(
    'tasks',
    broker=f"pyamqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@rabbitmq//",
    backend='rpc://'
)


celery_app.conf.update(
    result_expires=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)