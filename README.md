# Staff CRM

Staff CRM is a modern Django REST Framework application designed to manage employee profiles, departments, and user accounts with JWT authentication and interactive API documentation.

---

## 🚀 Features

- **Custom User Authentication**: Email-based user model (`accounts.User`) with JWT authentication via SimpleJWT.
- **Department Management**: Hierarchical department structure with manager assignments and active status tracking.
- **Employee Management**: Profile records linked to users and departments, including birth date validation and custom permissions (e.g. employee deactivation).
- **Interactive API Documentation**: OpenAPI 3.0 schema generation powered by `drf-spectacular` and served via `django-scalar` UI.

---

## 🛠️ Tech Stack

- **Framework**: Django 6.0+, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt`
- **API Documentation**: `drf-spectacular`, `django-scalar`
- **Package Manager**: `uv`
- **Database**: PostgreSQL (configured via `django-environ`) / SQLite

---

## 📁 Project Structure

```text
staff-crm/
├── accounts/       # Custom user model, authentication serializers & views
├── departments/    # Department model, serializers & API endpoints
├── employees/      # Employee profile model, modularized serializers & views
├── config/         # Django project configuration & settings
├── templates/      # Base templates and dashboard views
├── manage.py
├── pyproject.toml
└── uv.lock
```

---

## 📊 Database Schema

```mermaid
erDiagram
    USER ||--o| EMPLOYEE : has
    DEPARTMENT ||--o{ EMPLOYEE : contains
    EMPLOYEE ||--o| DEPARTMENT : manages
    DEPARTMENT ||--o| DEPARTMENT : sub_department_of

    USER {
        int id PK
        string email "UK"
        string password
        boolean is_staff
        boolean is_active
        boolean is_superuser
        datetime last_login
    }

    EMPLOYEE {
        int id PK
        int user_id FK
        int department_id FK
        string first_name
        string last_name
        date birth_date
        string gender
        datetime created_at
        datetime updated_at
    }

    DEPARTMENT {
        int id PK
        int manager_id FK
        int parent_department_id FK
        string name "UK"
        string description
        boolean is_active
        datetime created_at
        datetime updated_at
    }
```

---

## ⚙️ Getting Started

### Prerequisites

- Python `>= 3.14`
- [`uv`](https://github.com/astral-sh/uv) package manager

### 1. Environment Setup

Create a `.env` file in the root directory (refer to `.env.example` if available):

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://crm_user:password@localhost:5432/staff_crm
```

### 2. Install Dependencies

Install all project dependencies using `uv`:

```bash
uv sync
```

### 3. Database Migrations

Apply database migrations:

```bash
uv run python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
uv run python manage.py createsuperuser
```

### 5. Run Development Server

```bash
uv run python manage.py runserver
```

The application will be running at `http://127.0.0.1:8000/`.

---

## 📖 API Documentation & Endpoints

| Endpoint | Description |
| :--- | :--- |
| `/api/docs/` | **Scalar Interactive API Reference** |
| `/api/schema/` | OpenAPI 3.0 Schema endpoint |
| `/api/employees/` | Employee management endpoints |
| `/api/departments/` | Department management endpoints |
| `/api/auth/` | Authentication & JWT token endpoints |
| `/admin/` | Django Admin portal |

---

## 🧪 System Check

To run system checks and verify configuration:

```bash
uv run python manage.py check
```
