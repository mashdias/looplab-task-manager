# Task Management REST API

A production-ready Task Management REST API built with Django, Django REST Framework, and PostgreSQL. It includes token-based authentication (SimpleJWT), role-based permissions (Admin vs Member), soft deletion, activity logging via Django signals, and a minimal React frontend.


## Walkthrough Video
**Demo Video:** [Click here to watch the application walkthrough](https://drive.google.com/file/d/1KtapCDbwgcMIiAv45VEl08GDcwdAW6yH/view?usp=sharing)

## Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL server

## Local Setup Steps

### 1. Database Setup
Create a PostgreSQL database and user. The default `.env` assumes:
- **DB_NAME**: looplab_db
- **DB_USER**: postgres
- **DB_PASSWORD**: postgres

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Migrations & Superuser
Run the initial migrations and create a superuser.
```bash
cd task_manager
python manage.py makemigrations api
python manage.py migrate

# Create an Admin user (Superuser)
python manage.py createsuperuser
# IMPORTANT: Since we added a custom `role` field, it defaults to 'Member' for regular createsuperuser.
# You can change the role in the Django Admin panel or create it via a shell script.
```

### 4. Run Backend Server
```bash
python manage.py runserver
```

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`. You can log in using the superuser credentials you created.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/token/` | Obtain JWT access and refresh tokens. |
| POST | `/api/v1/token/refresh/` | Refresh JWT access token. |
| GET | `/api/v1/projects/` | List projects (Admins see all, Members see owned or assigned). |
| POST | `/api/v1/projects/` | Create a new project. |
| GET | `/api/v1/projects/{id}/` | Retrieve a specific project. |
| PUT/PATCH | `/api/v1/projects/{id}/` | Update a specific project. |
| DELETE | `/api/v1/projects/{id}/` | Delete a specific project. |
| GET | `/api/v1/tasks/` | List tasks (Supports pagination, search, filters). |
| POST | `/api/v1/tasks/` | Create a new task. |
| GET | `/api/v1/tasks/{id}/` | Retrieve a specific task. |
| PUT/PATCH | `/api/v1/tasks/{id}/` | Update a specific task. |
| DELETE | `/api/v1/tasks/{id}/` | Soft-delete a specific task (Admins only). |
| GET | `/api/v1/activity-logs/` | List activity logs (CREATE, UPDATE, DELETE actions). |

*Note: All `/api/v1/projects/`, `/api/v1/tasks/`, and `/api/v1/activity-logs/` endpoints require a valid `Bearer <token>` in the Authorization header.*
