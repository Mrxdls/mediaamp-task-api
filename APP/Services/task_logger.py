from APP.database import db
from APP.models import TaskManager, TaskLogger
from APP.models import indian_time

def log_active_tasks():
    try:
        active_tasks = TaskManager.query.filter_by(is_active=True).all()
        for task in active_tasks:
            log_entry = TaskLogger(
                task_id=task.id,
                logged_at=indian_time()
            )
            db.session.add(log_entry)
        db.session.commit()
        print("Active tasks logged successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error logging active tasks: {e}")