from APP.celery_app import celery
from APP.database import db
from APP.models import TaskManager, TaskLogger
from APP import app  # Import the app instance

@celery.task(bind=True)
def log_active_tasks(self):
    with app.app_context():
        active_tasks = TaskManager.query.filter_by(is_active=True).all()
        for task in active_tasks:
            logg = TaskLogger(
                task_id=task.id,
                task_name=task.task_name,
                status=task.status,
                created_at=task.created_at
            )
            db.session.add(logg)
        db.session.commit()
        return f"Logged {len(active_tasks)} transfered"
    