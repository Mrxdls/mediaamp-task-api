celery -A app.celery_worker.celery worker --loglevel=info
celery -A app.celery_worker.celery beat --loglevel=info
