# **Task Management API**

## **Overview**
This is a Flask-based Task Management API designed to handle tasks efficiently. It provides endpoints for creating, updating, retrieving, and deleting tasks, along with user authentication and rate-limiting features. The API also integrates Redis for caching and Celery for background task processing.

---

## **Features**
- **User Management**:
  - User registration and login with JWT-based authentication.
  - Role-based access control (e.g., admin privileges for certain actions).

- **Task Management**:
  - Create, update, retrieve, and delete tasks.
  - Retrieve tasks by date.
  - Task logging and priority management.

- **Rate Limiting**:
  - Protects endpoints with rate limits (e.g., 5 requests per minute).

- **Caching**:
  - Redis is used to cache frequently accessed data (e.g., task lists).

- **Database**:
  - SQLAlchemy is used for database interactions.
  - Flask-Migrate is used for database migrations.

- **Background Tasks**:
  - Celery is integrated for handling asynchronous tasks.

---

## **Technologies Used**
- **Backend Framework**: Flask
- **Database**: SQLAlchemy (PostgreSQL)
- **Caching**: Redis
- **Task Queue**: Celery
- **Authentication**: Flask-JWT-Extended
- **Rate Limiting**: Flask-Limiter
- **Environment Management**: Python 3.12
- **Deployment**: Localhost (development)

---

## **Setup Instructions**

### **1. Clone the Repository**

GitHub Copilot
Here’s the updated README.md file without mentioning the company name:

2. Install Dependencies
Use pip to install the required Python packages:
pip install -r requirements.txt

3. Configure Environment Variables
Create a credentials.py file in the APP directory with the following variables:

DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database>"
SECRET_KEY = "<your-secret-key>"
JWT_SECRET_KEY = "<your-jwt-secret-key>"
REDIS_URL = "redis://localhost:6379"

5. Start Redis
Ensure Redis is running on your system:

 Run Redis in Docker
If Redis is not already running in Docker, you can start a Redis container using the following command:
docker run -d --name redis-container -p 6379:6379 redis


-d: Runs the container in detached mode.
--name redis-container: Names the container redis-container.
-p 6379:6379: Maps port 6379 on the host to port 6379 in the container.


varify its running

docker ps

test redis connection
redis-cli -h localhost -p 6379

PING <--------- input
PONG < -----------------output

6. Run the Application
Start the Flask development server:

python3 run.py

The application will be available at http://127.0.0.1:5000.



table from image

Rate Limiting
Default Limit: 100 requests per hour.
Custom Limits:
/tasks/task/<string:date>: 5 requests per minute.
/api/check-limiter: 5 requests per minute.

Caching
Redis is used to cache task lists for 1 hour.
Example:
Key: task:<date> (e.g., task:2025-04-06).
Value: Serialized JSON of the task list.


Error Handling
400 Bad Request: Invalid input (e.g., incorrect date format).
401 Unauthorized: Missing or invalid JWT token.
404 Not Found: Resource not found (e.g., no tasks for a given date).
429 Too Many Requests: Rate limit exceeded.


Example Usage
1. register a user

curl -X POST http://127.0.0.1:5000/users/register \
-H "Content-Type: application/json" \
-d '{
    "username": "admin",
    "password": "admin123",
    "role": "admin"
}'

2. login

curl -X POST http://127.0.0.1:5000/users/login \
-H "Content-Type: application/json" \
-d '{
    "username": "admin",
    "password": "admin123"
}'

you retrive a jwt-token that you have to put in authentication

curl -X GET http://127.0.0.1:5000/tasks/task/2025-04-06 \
-H "Authorization: Bearer <your-jwt-token>"

project structure

TaskManagementAPI/
├── APP/
│   ├── __init__.py          # App factory and initialization
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── routes/
│   │   ├── task_routes.py   # Task-related routes
│   │   ├── user_routes.py   # User-related routes
│   │   ├── health_routes.py # Health check routes
│   ├── Services/
│   │   ├── rate_limiter.py  # Rate limiter setup
│   │   ├── redis_client.py  # Redis client setup
│   │   ├── celery_app.py    # Celery configuration
│   ├── schemas.py           # Pydantic schemas
├── migrations/              # Database migrations
├── requirements.txt         # Python dependencies
├── [run.py] <-------------------- Application entry point



```markdown
# 🎯 Task Management API (Flask-based)

## 📌 Overview
This is a Task Management API built using Flask, designed to help manage, log, and update tasks efficiently. It includes features like authentication, rate limiting, Redis caching, and background task processing using Celery. I built this project as part of a backend assignment — and tried to keep it clean, modular, and production-ready for learning purposes!

---

## 🚀 Features

- **User Authentication**
  - Register and log in users with JWT tokens.
  - Role-based control (e.g., admin-level operations).

- **Task Operations**
  - Create, update, retrieve, and soft-delete tasks.
  - Filter tasks by date.
  - Handles task priorities and logs.

- **Rate Limiting**
  - Prevents spam with smart request limiting (e.g., 5/min per endpoint).

- **Caching (Redis)**
  - Tasks are cached by date for faster access.

- **Database**
  - PostgreSQL with SQLAlchemy ORM + Flask-Migrate for versioning.

- **Async Jobs**
  - Celery is used for background task processing (e.g., daily syncs).

---

## 🧱️ Technologies Used

| Component         | Tech Stack               |
|------------------|--------------------------|
| Backend Framework| Flask                    |
| Database         | PostgreSQL + SQLAlchemy  |
| Caching          | Redis                    |
| Auth             | Flask-JWT-Extended       |
| Rate Limiting    | Flask-Limiter            |
| Async Tasks      | Celery                   |
| Python Version   | 3.12                     |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/task-api.git
cd task-api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Environment Config
Create a `credentials.py` file inside the `APP/` folder:
```python
DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<db_name>"
SECRET_KEY = "<your-secret-key>"
JWT_SECRET_KEY = "<your-jwt-secret-key>"
REDIS_URL = "redis://localhost:6379"
```

### 4. Start Redis
If Redis isn't running:
```bash
docker run -d --name redis-container -p 6379:6379 redis
docker ps  # make sure it's running
redis-cli -h localhost -p 6379  # test it
PING  # returns PONG if it works
```

### 5. Run the App
```bash
python3 run.py
```

App will be live at `http://127.0.0.1:5000/`.

---

## 🔐 API Endpoints

### ✨ Authentication

| Method | Endpoint         | Description                 |
|--------|------------------|-----------------------------|
| POST   | `/users/register`| Register a new user         |
| POST   | `/users/login`   | Login and get a JWT token   |

### 📋 Task Management

| Method | Endpoint                            | Description                            |
|--------|-------------------------------------|----------------------------------------|
| GET    | `/tasks/task/<string:date>`         | Retrieve tasks by date (YYYY-MM-DD)    |
| POST   | `/tasks/create-task`                | Create a new task                      |
| PUT    | `/tasks/update-task/<int:task_id>`  | Update an existing task                |
| DELETE | `/tasks/delete/<int:task_id>`       | Soft delete a task (marks as inactive) |

### ✅ Health Check

| Method | Endpoint               | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | `/api/health/db`       | Check database connection           |
| GET    | `/api/check-limiter`   | Test rate limiter functionality     |

---

## 📈 Rate Limiting

| Endpoint                        | Limit              |
|---------------------------------|--------------------|
| `/tasks/task/<date>`           | 5 requests/minute  |
| `/api/check-limiter`           | 5 requests/minute  |
| **Global Default**             | 100 requests/hour  |

---

## 📀 Caching
- Redis caches task lists for 1 hour.
- Key format: `task:<YYYY-MM-DD>`  
- Value: JSON-serialized list of tasks.

---

## 🛯 Error Handling

| Code | Meaning                     | When it Happens                         |
|------|-----------------------------|------------------------------------------|
| 400  | Bad Request                 | Invalid input (e.g., bad date format)    |
| 401  | Unauthorized                | Missing or invalid JWT                   |
| 404  | Not Found                   | Task/date not found                      |
| 429  | Too Many Requests           | Rate limit exceeded                      |

---

## 🧪 Example Usage

### Register
```bash
curl -X POST http://127.0.0.1:5000/users/register \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin123", "role": "admin"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:5000/users/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin123"}'
```

### Retrieve Tasks (auth required)
```bash
curl -X GET http://127.0.0.1:5000/tasks/task/2025-04-06 \
-H "Authorization: Bearer <your-jwt-token>"
```

---

## 📂 Project Structure

```
TaskManagementAPI/
├── APP/
│   ├── __init__.py            # App setup
│   ├── config.py              # Config settings
│   ├── database.py            # DB connection
│   ├── models.py              # SQLAlchemy models
│   ├── routes/
│   │   ├── task_routes.py     # Task routes
│   │   ├── user_routes.py     # User auth routes
│   │   └── health_routes.py   # Health endpoints
│   ├── Services/
│   │   ├── rate_limiter.py    # Limiting config
│   │   ├── redis_client.py    # Redis setup
│   │   └── celery_app.py      # Celery init
│   └── schemas.py             # Data schemas
├── migrations/                # DB migrations
├── requirements.txt           # Dependencies
├── run.py                     # Entry point
```

---

## 🧓‍♂️ Notes
- All deletions are soft deletes unless stated otherwise.
- Background jobs like syncing task logs are handled using Celery.
- Rate limits are enforced at both global and per-endpoint levels.
