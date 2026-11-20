# FitFlow — Gym Management System

A full-stack gym management starter project built with **FastAPI, SQLAlchemy, SQLite/MySQL, JWT authentication, and HTML/CSS/JavaScript**.

## Features

- Admin, trainer, and member roles with JWT login
- Member management (create, list, view, update, delete)
- Trainer management
- Membership plan creation and member subscription assignment
- Payment records and payment status tracking
- Attendance check-in and check-out
- Workout plan and diet plan assignment
- Dashboard summary: members, active memberships, daily attendance, monthly revenue, pending payments
- Interactive Swagger API documentation at `/docs`
- Dark responsive web dashboard

## Requirements

- Python 3.10+
- pip
- Optional: MySQL 8+ (SQLite is the default for quick local setup)

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/gym-management-system.git
cd gym-management-system
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
copy .env.example .env
```

On macOS/Linux use `cp .env.example .env`. For local development the default SQLite database works without extra setup. Change `SECRET_KEY` before sharing or deploying.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

Open:
- API health: http://127.0.0.1:8000/health
- Swagger documentation: http://127.0.0.1:8000/docs
- Frontend: open `frontend/index.html` in your browser (or serve it with `python -m http.server 5500 --directory frontend` and visit http://127.0.0.1:5500).

## First-time admin setup

The API does not create a default admin password. This is intentional: create your first account through Swagger.

1. Open `/docs`.
2. Expand `POST /auth/register`.
3. Register using your name, email, password (at least 8 characters), and role `admin`.
4. Use `POST /auth/login` with the same credentials.
5. Copy `access_token`.
6. Click **Authorize** in Swagger and enter `Bearer YOUR_ACCESS_TOKEN`.
7. Sign in to the web dashboard with the same email and password.

The sample values shown in the frontend login form are placeholders only; replace them with the admin account you created.

> Registration currently accepts the roles `admin`, `trainer`, and `member` for development convenience. Before a public production launch, restrict public registration to `member` and create admin/trainer accounts through an authorized admin workflow.

## MySQL setup (optional)

Create a database and user in MySQL:

```sql
CREATE DATABASE gym_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gym_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON gym_management.* TO 'gym_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `.env`:

```env
DATABASE_URL=mysql+pymysql://gym_user:your_password@localhost:3306/gym_management
SECRET_KEY=your-long-random-secret
```

Restart the API. Tables are created automatically on startup for this starter project.

## Main API routes

| Feature | Endpoints |
|---|---|
| Authentication | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` |
| Members | `POST/GET /members/`, `GET/PUT/DELETE /members/{id}` |
| Trainers | `POST/GET /trainers/`, `PUT/DELETE /trainers/{id}` |
| Membership plans | `POST/GET /plans/` |
| Memberships | `POST/GET /memberships/` |
| Payments | `POST/GET /payments/` |
| Attendance | `POST /attendance/check-in`, `POST /attendance/{id}/check-out`, `GET /attendance/` |
| Workout plans | `POST/GET /workouts/` |
| Diet plans | `POST/GET /diet-plans/` |
| Dashboard | `GET /dashboard/summary` |

## Suggested test flow

1. Register an admin and log in.
2. Create one trainer (`POST /trainers/`).
3. Create a member (`POST /members/`).
4. Create a plan (`POST /plans/`).
5. Assign a membership (`POST /memberships/`).
6. Record payment (`POST /payments/`).
7. Check the member in (`POST /attendance/check-in`) and check out using the returned attendance ID.
8. Assign workout and diet plans.
9. Review `/dashboard/summary`.

## Important notes before production

This is a portfolio-ready learning starter, not a certified commercial gym/payment platform. Before production use:
- Add Alembic migrations instead of relying on `create_all`.
- Restrict role registration and add admin-managed user provisioning.
- Add object-level authorization so members can only view their own records.
- Add pagination, audit logs, password reset, rate limiting, HTTPS, backups, and automated tests.
- Integrate a payment gateway only through its official server-side APIs; never store card details.
- Review privacy requirements before storing member personal data.
- Set a strong secret key and configure exact trusted CORS origins.

## License

MIT — see [LICENSE](LICENSE).
