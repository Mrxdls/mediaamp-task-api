from flask_sqlalchemy import SQLAlchemy
import time
from sqlalchemy import create_engine, text

# Create the SQLAlchemy object
db = SQLAlchemy()

def initialize_db(app, retries=5, delay=2):
    attempt = 0
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    
    while attempt < retries:
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT 1'))
                print(f"Database connection successful: {result.fetchone()}")
                with app.app_context():
                    db.create_all()  # Create tables
                return
        except Exception as e:
            attempt += 1
            print(f"Database connection failed (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("Could not establish database connection after retries")
                raise Exception("Database connection failed")




