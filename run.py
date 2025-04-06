from flask import Flask
from APP import create_app
from APP.database import initialize_db
from APP.Services.initialize_admin import initialize_admin_user
from flask_apscheduler import APScheduler
# from APP.Services.task_logger import log_active_tasks

scheduler = APScheduler()

def main():
    app = create_app()
    # Note: initialize_db should be called with app context
    with app.app_context():
        print("Initializing database...")
        initialize_db(app)
        initialize_admin_user()
        print("Database initialized successfully.")
        # scheduler.init_app(app)
        # scheduler.start()
    return app

if __name__ == "__main__":
    
    app = main()

    app.run(debug=True)