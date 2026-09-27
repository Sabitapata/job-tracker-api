# Job Tracker API

A secure REST API for managing job applications. Users can create accounts, log in with JWT authentication, and manage only their own job-application records.

## Features

- User registration with email validation
- Password hashing with Argon2
- JWT-based login and protected endpoints
- Per-user authorization and ownership checks
- Create, read, update, and delete job applications
- Input validation for application status and text fields
- SQLite database persistence with SQLModel
- Environment-based configuration using `.env`
- Automated tests using pytest and FastAPI TestClient
- Streamlit dashboard for registration, login, job-application management, metrics, and status visualization

## Tech Stack

- Python
- FastAPI
- SQLModel and SQLite
- Pydantic
- PyJWT
- pwdlib / Argon2
- pytest
- Uvicorn

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `POST` | `/users/register` | Create a new user account | No |
| `POST` | `/users/login` | Log in and receive JWT token | No |
| `GET` | `/` | API welcome route | No |
| `GET` | `/health` | Health-check route | No |
| `POST` | `/applications/` | Create a job application | Yes |
| `GET` | `/applications/` | List the current user's applications | Yes |
| `GET` | `/applications/{id}` | Get one owned application | Yes |
| `PATCH` | `/applications/{id}` | Update one owned application | Yes |
| `DELETE` | `/applications/{id}` | Delete one owned application | Yes |

## Project Structure

```text
job_tracker_api/
├── app/
│   ├── routers/
│   │   ├── applications.py
│   │   └── users.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── frontend/
│   └── dashboard.py
|── tests/
│   ├── conftest.py
│   ├── test_applications.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/job-tracker-api.git](https://github.com/YOUR_GITHUB_USERNAME/job-tracker-api.git)
cd job-tracker-api
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./job_tracker.db
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Run the FastAPI backend

```bash
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
python -m pytest -v
```
### 6. Run the Streamlit frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/dashboard.py
```

Open the dashboard:

```text
http://localhost:8501
```

## Example Workflow

1. Register a user using `POST /users/register`.
2. Log in using `POST /users/login`.
3. Copy the `access_token` from the login response.
4. Click **Authorize** in `/docs` and paste the token.
5. Create and manage job applications through `/applications/`.

## Security Notes

- Passwords are hashed with Argon2; plain passwords are not stored.
- The JWT secret key is loaded from `.env` rather than source code.
- `.env` and local SQLite database files are excluded through `.gitignore`.
- Users can access only their own job applications.

## Future Improvements

- Add application search, filtering, and pagination
- Add deadline reminders and job-status analytics
- Add PostgreSQL for production deployment
- Add Docker support and deployment configuration
- Build a frontend with React or Streamlit
- Add GitHub Actions CI for automated testing