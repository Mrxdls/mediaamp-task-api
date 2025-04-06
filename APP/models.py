# from sqlalchemy import Column, Integer, String, ForeignKey
from APP.database import db
from datetime import datetime
import pytz


# create classes for the database models
# that will be used to create the tables in the database
# these classes also define the relationships between the tables
def indian_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def indian_date():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).date()

# user table
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)


# task_manager table 
class TaskManager(db.Model):
    __tablename__ = 'task_manager'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='priority_levels'), nullable=False, default='LOW')
    created_at = db.Column(db.Date, default=indian_date)
    assigned_user = db.Column(db.Integer, db.ForeignKey("user.id"))


# task_logger table where only active tasks are logged
class TaskLogger(db.Model):
    __tablename__ = 'task_logger'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task_manager.id"))
    logged_at = db.Column(db.DateTime, default=indian_time)


class Audit_logger(db.Model):
    __tablename__ = 'audit_logger'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task_manager.id"))
    previous_state = db.Column(db.String(255))
    current_state = db.Column(db.String(255))
    action_by = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=indian_time)