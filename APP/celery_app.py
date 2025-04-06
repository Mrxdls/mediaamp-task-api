from celery import Celery
from credentials import REDIS_URL
from celery.schedules import crontab
def make_celery(app_name=__name__):
    celery = Celery(
        app_name, 
        broker=REDIS_URL,
        backend=REDIS_URL
    )
    return celery
celery = make_celery()

celery.conf.beat_schedule = {
    "daily_task":{
        "task": "APP.Services.log_transter.log_active_tasks",
        "schedule": crontab(hour=2, minute=43)
        # Run every day at midnight
    }
}