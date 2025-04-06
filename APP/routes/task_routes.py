import json
from flask import request, jsonify, Blueprint
from APP.models import User, TaskManager, TaskLogger, Audit_logger, indian_time, indian_date
from APP.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
from werkzeug.security import generate_password_hash
from datetime import datetime
from APP.Services.rate_limiter import limiter
from APP.Services.cache import redis_client


task_blueprint = Blueprint('task_blueprint', __name__)

@task_blueprint.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Task Management API!",
        "description": "This API allows you to manage tasks, including creating, updating, and deleting tasks.",
        "endpoints": {
            "GET": [
                "/tasks/task-records",
                "/tasks/task-log/<int:id>"
            ],
            "POST": [
                "/tasks/create-task",
                "/tasks/upload-csv",
                "/tasks/update-task/<int:task_id>"
            ],
            "DELETE": [
                "/tasks/delete/<int:task_id>"
            ]
        }
    }), 200

# ================================================================

@task_blueprint.route('/upload-csv', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
def upload_csv():

    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_identity['id']).first()
    
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "You are not authorized to upload CSV files."}), 403

    # Validate file upload
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400

    required_columns = ['task_name', 'description', 'status', 'priority', 'created_at', 'assigned_user']
    if not all(column in df.columns for column in required_columns):
        return jsonify({"error": f"The CSV file must contain the following columns: {', '.join(required_columns)}"}), 400

    # Create a dictionary to track success and errors
    results = {
        "success": [],
        "errors": []
    }

    # Normalize priority values
    priority_map = {
        'LOW': 'LOW',
        'MEDIUM': 'MEDIUM',
        'MED': 'MEDIUM',
        'HIGH': 'HIGH',
        'CRITICAL': 'CRITICAL',
        'CRIT': 'CRITICAL',
        'URGENT': 'CRITICAL'
    }

    try:
        for _, row in df.iterrows():
            task_name = row['task_name']
            description = row['description']

            # Convert status to boolean
            status_value = row['status']
            if isinstance(status_value, str):
                is_active = status_value.strip().upper() in ['TRUE', 'YES', 'Y', '1', 'ACTIVE']
            else:
                is_active = bool(status_value)

            # Normalize and validate priority
            priority = str(row['priority']).strip().upper()
            priority = priority_map.get(priority, 'MEDIUM')  # Default to MEDIUM if priority is invalid

            # Parse date with multiple format support
            try:
                date_formats = ['%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']
                created_at = None
                for fmt in date_formats:
                    try:
                        created_at = datetime.strptime(str(row['created_at']), fmt)
                        break
                    except ValueError:
                        continue

                if created_at is None:
                    created_at = indian_date()
            except Exception:
                created_at = indian_date()

            # Handle assigned user - fetch from the CSV and create if not present
            username = str(row['assigned_user']).strip()
            assigned_user = User.query.filter_by(username=username).first()
            if not assigned_user:
                # Create a new user with a default password
                default_password = f"{username}123"
                assigned_user = User(
                    username=username,
                    password=generate_password_hash(default_password),
                    role='user'  # Default role for new users
                )
                db.session.add(assigned_user)
                db.session.flush()  # Flush to get the new user's ID
                results["success"].append(f"Created new user '{username}' with default password.")

            assigned_user_id = assigned_user.id

            # Create a new task
            new_task = TaskManager(
                task_name=task_name,
                description=description,
                is_active=is_active,
                priority=priority,
                created_at=created_at,
                assigned_user=assigned_user_id
            )
            db.session.add(new_task)
            results["success"].append(f"Created task '{task_name}'")

        # Commit all successful tasks and new users at once
        db.session.commit()

        # Create an audit log entry for this import
        for task_name in results["success"]:
            # Fetch the task that was just created
            task = TaskManager.query.filter_by(task_name=task_name.split("'")[1]).first()
            if task:
                audit_log = Audit_logger(
                    task_id=task.id,
                    current_state="Task added",
                    previous_state=None,  # No previous state as the task is new
                    action_by=current_user.id,
                    timestamp=indian_time()
                )
                db.session.add(audit_log)

        # Commit all audit logs at once after the loop
        db.session.commit()

        # Create a response with results
        response = {
            "message": f"CSV processing complete. {len(results['success'])} tasks imported successfully.",
            "details": results
        }

        return jsonify(response), 200

    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        return jsonify({"error": f"Error processing CSV: {str(e)}"}), 500
    


# ========================================================

@task_blueprint.route('/<int:task_id>', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
def update_task(task_id):

    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_identity['id']).first()
    
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "You are not authorized to update tasks."}), 403

    data = request.get_json()
    data_format = jsonify({
        "task_name": "string",
        "description": "string",
        "is_active": "boolean",
        "priority": "string (LOW, MEDIUM, HIGH, CRITICAL)",
        "created_at": "date (YYYY-MM-DD)",
        "assigned_user": "string (username)"
    })
    if not data:
        return jsonify({"error": "Invalid input. Please provide a JSON object with task details.",
                        "data_format": data_format}), 400

    # fetch task id from task manager to update the task
    task = TaskManager.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Update task details
    if 'task_name' in data:
        task.task_name = data['task_name']
    if 'description' in data:
        task.description = data['description']
    if 'is_active' in data:
        task.is_active = bool(data['is_active'])
    if 'priority' in data:
        priority_value = str(data['priority']).strip().upper()
        priority_map = {
            'LOW': 'LOW',
            'MEDIUM': 'MEDIUM',
            'HIGH': 'HIGH',
            'CRITICAL': 'CRITICAL'
        }
        task.priority = priority_map.get(priority_value, 'MEDIUM')
    db.session.commit()

    task = TaskManager.query.filter_by(id=task_id).first()

    if task:
        audit  = Audit_logger.query.filter_by(task_id=task.id).first()
        audit_log = Audit_logger(
            task_id=task.id,
            previous_state = audit.current_state,  # No previous state as the task is new
            current_state="Task updated",
            action_by=current_user.id,
            timestamp=indian_time()
        )

    # Commit all audit logs at once after the loop
    db.session.add(audit_log)
    db.session.commit()
    return jsonify({
        "message": "Task updated successfully",
        "task": {
            "task_name": task.task_name,
            "description": task.description,
            "is_active": task.is_active,
            "priority": task.priority,
            "created_at": task.created_at,
            "assigned_user": task.assigned_user
        }
    }), 200


@task_blueprint.route('/delete/<int:task_id>', methods=['DELETE'])
@limiter.exempt
@jwt_required()
def delete_task(task_id):
    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_identity['id']).first()
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "You are not authorized to delete tasks."}), 403
    
    task = TaskManager.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task.is_active = False
    db.session.add(task)
    db.session.commit()

    task = TaskManager.query.filter_by(id=task_id).first()
    if task:
        audit = Audit_logger(
            task_id=task.id,
            previous_state=task.is_active,
            current_state= False,
            action_by=current_user.id,
            timestamp=indian_time()
        )
    db.session.add(audit)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200
# ========================================================


@task_blueprint.route('/task-records', methods=['GET'])
@limiter.limit("5 per minute")
@jwt_required()
def get_tasks():
    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_identity['id']).first()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    page = request.args.get('page', default=1, type=int)
    per_page = 5
    
    query = db.session.query(
        User.username,
        User.id.label('user_id'),
        TaskManager.id.label('task_id'),
        TaskManager.task_name,
        TaskManager.description,
        TaskManager.created_at,
        TaskManager.priority,
        TaskLogger.logged_at
    ).join(
        TaskManager.assigned_user == User.id
    ).join(
        TaskLogger,
        TaskLogger.task_id == TaskManager.id
    ).filter(
        TaskManager.is_active == True
    ).order_by(TaskLogger.logged_at.desc())

    paginated_task = query.paginate(
        page = page,
        per_page = 5,
        error_out = False
        # error_out  = False is used handle 404 error if pages are out of bound
    )

    result = []
    for task in paginated_task.items:
        result.append(
            {
                "username": task.username,
                "user_id": task.user_id,
                "task_id": task.task_id,
                "task_name": task.task_name,
                "description": task.description,
                "created_at": task.created_at,
                "priority": task.priority,
                "logged_at": task.logged_at
            }
        )

    return jsonify(
        {
            "data": result,
            "page": paginated_task.page,
            "per_page": per_page,
            "total No of records": paginated_task,
            "total pages": paginated_task.pages,

        }
    ), 200
# ========================================================

@task_blueprint.route('/task-log/<int:id>', methods=['GET'])
@limiter.limit("5 per minute")
@jwt_required()
def get_task_log(id):
    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_identity['id']).first()
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    task_log = TaskLogger.query.filter_by(task_id = id).first()
    if not task_log:
        return jsonify({"error": "Task log not found"}), 404
    return jsonify({
        "log_id": task_log.id,
        "task_id": task_log.task_id,
        "logged_at": task_log.logged_at
    }), 200





@task_blueprint.route('/task/<string:date>', methods=['GET'])
@limiter.limit("5 per minute")
@jwt_required()
def get_task_by_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()  # Expected format: YYYY-MM-DD
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    key = f"task: {date}"
    cached_tasks = redis_client.get(key)
    if cached_tasks:
        print("Cache hit")
        return cached_tasks
    task = TaskManager.query.filter_by(created_at = date).all()
    if not task:
        return jsonify({"error": "No task found for the given date"}), 404
    task_list = []
    for task in task:
        task_list.append(
            {
                "id": task.id,
                "task_name": task.task_name,
                "description": task.description,
                "is_active": task.is_active,
                "priority": task.priority,
                "assigned_user": task.assigned_user   
            }
        )
    redis_client.set(key, json.dumps(task_list), ex=3600)
    redis_client.expire(key, 3600)
    return jsonify(
            {
                "task_list": task_list,
                "message": "Task found successfully",
                "date": date
            }
        )
    


