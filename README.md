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

| Component        | Tech Stack               |
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
