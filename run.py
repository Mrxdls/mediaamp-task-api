from flask import Flask
from APP import create_app
from APP.database import initialize_db
from APP.Services.initialize_admin import initialize_admin_user
from flask_apscheduler import APScheduler
from flask_migrate import upgrade, init, Migrate
import os
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
        if not os.path.exists("migrations"):
            try:
                init(directory="migrations")
                print("Applying database migrations...")
            except Exception as e:
                print(f"Error initializing migrations: {e}")
        else:
            print("Migrations directory already exists. skipping init.")
        # Apply migrations
        upgrade()
        print("Database migrations applied successfully.")
        return app

if __name__ == "__main__":
    
    app = main()

    app.run(debug=True)