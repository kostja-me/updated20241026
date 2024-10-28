import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue
from .settings import BASE_DIR
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")
app.autodiscover_tasks()
app.conf.broker_url = env("CELERY_BROKER_URL", default=None)
app.conf.accept_content = ["application/json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.result_backend = env("REDIS_URL", default=None)
app.conf.task_default_queue = "default"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# Task soft time limit in seconds.
# app.conf.task_soft_time_limit = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# Task hard time limit in seconds.
# The worker processing the task will be killed and replaced with a new one when this is exceeded.
# app.conf.task_time_limit = 600
app.conf.task_create_missing_queues = True
app.conf.task_queues = (Queue("default"),)
app.conf.broker_pool_limit = 1
app.conf.broker_connection_timeout = 30
# worker_prefetch_multiplier: appropriate for long running tasks, default is 4
app.conf.worker_prefetch_multiplier = 1
app.conf.redbeat_redis_url = env("REDIS_URL", default=None)
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#beat-entries
"""
Example of entries:

Run on 00:01, first day of month

    "example-celery-task": {
        "task": "example_celery_task",
        'schedule': crontab(
            minute=1,
            hour=0,
            day_of_month=1
         ),
         'schedule': 60 * 10 # run every 10 minutes
        "options": {
            "ignore_result": True,
            "queue": "default",
        },
    }
Run every 10 minutes
    "example-celery-task": {
        "task": "example_celery_task",
        'schedule': 60 * 10 # run every 10 minutes
        "options": {
            "ignore_result": True,
            "queue": "default",
        },
    }
"""
app.conf.beat_schedule = {
}
