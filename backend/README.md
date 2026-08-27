# PlanSoko backend

This directory contains the Django and Django REST Framework backend for the
PlanSoko marketplace.

## Local setup

### 1. Create and activate a virtual environment

From the `backend` directory:

```powershell
py -3.13 -m venv planenv
.\planenv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure local environment variables

Create your local secrets file from the safe template:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your own Django secret key, PostgreSQL credentials, and
Daraja sandbox credentials. Never commit `.env`.

`.env.example` is intentionally safe to commit. It documents the variables
the application needs without containing working credentials.

### 3. Create the PostgreSQL database

Connect to PostgreSQL as an administrator and create a dedicated local role
and database:

```sql
CREATE ROLE plan LOGIN PASSWORD 'choose-a-strong-local-password';
CREATE DATABASE plansoko OWNER plan_db;
```

Use the matching details in `.env`:

```text
DB_NAME=plan_db
DB_USER=plan
DB_PASSWORD=choose-a-strong-local-password
DB_HOST=127.0.0.1
DB_PORT=5432
```

The database and role names are examples. They may differ as long as the
values in `.env` match the PostgreSQL role and database you created.

### 4. Apply migrations

From the `backend` directory:

```powershell
cd plan
python manage.py migrate
```

`migrate` creates or updates database tables from the version-controlled
migration files. Do not manually create Django application tables.

### 5. Run the development server

```powershell
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`. The React development server
uses `http://localhost:5173/`, which must appear in `CORS_ALLOWED_ORIGINS` in
your `.env`.

## Required environment variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django cryptographic secret. |
| `DEBUG` | Enables development-only diagnostics when `True`. |
| `ALLOWED_HOSTS` | Comma-separated HTTP hosts Django accepts. |
| `CORS_ALLOWED_ORIGINS` | Comma-separated browser origins allowed to call the API. |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection details. |
| `DARAJA_ENVIRONMENT` | `sandbox` locally; production requires deliberate configuration. |
| `DARAJA_CONSUMER`, `DARAJA_SECRET`, `DARAJA_PASSKEY`, `DARAJA_SHORTCODE` | Daraja credentials. |

## Verification commands

Run these from `backend/plan` after activating the virtual environment:

```powershell
python manage.py check
python manage.py showmigrations
python manage.py test
```

Expected current result: system checks pass, all migrations are applied after
step 4, and the project has no automated tests yet. Adding tests is planned in
the MVP roadmap.

## Important conventions

- Keep production and development databases on PostgreSQL. This avoids finding
  SQLite/PostgreSQL differences late in the release process.
- Database timestamps remain in UTC (`USE_TZ=True`); convert them to a user's
  local time only when displaying them.
- Commit migrations and `.env.example`; never commit `.env`, virtual
  environments, uploaded media, or database files.
