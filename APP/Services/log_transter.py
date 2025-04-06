from APP.celery_app import celery
from APP.database import db
from APP.models import TaskManager, TaskLogger
from APP import create_app  # Import the app factory function

@celery.task(bind=True)
def log_active_tasks(self):
    # Create a Flask app instance
    app = create_app()

    # Use the app context for database operations
    with app.app_context():
        try:
            # Query active tasks
            active_tasks = TaskManager.query.filter_by(is_active=True).all()

            # Log each active task
            for task in active_tasks:
                logg = TaskLogger(
                    task_id=task.id,
                    logged_at=db.func.now()  # Log the current time
                )
                db.session.add(logg)

            # Commit the changes to the database
            db.session.commit()
            return f"Logged {len(active_tasks)} tasks to TaskLogger."

        except Exception as e:
            # Rollback in case of an error
            db.session.rollback()
            raise self.retry(exc=e, countdown=60, max_retries=3)