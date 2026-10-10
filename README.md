# 💼 Job Tracker API & Dashboard

<p align="center">
  <strong>A modern, production-grade REST API and interactive dashboard to track, organize, and accelerate your job search.</strong>
</p>

<p align="center">
  <a href="https://github.com/Sabitapata/job-tracker-api/actions/workflows/tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/Sabitapata/job-tracker-api/tests.yml?branch=main&label=CI%20Tests&logo=github" alt="CI Status"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://sqlmodel.tiangolo.com/"><img src="https://img.shields.io/badge/SQLModel-SQLite%20%7C%20PostgreSQL-blue?logo=postgresql&logoColor=white" alt="SQLModel"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/Tests-Pytest%20(9%2F9%20Passed)-brightgreen?logo=pytest&logoColor=white" alt="Pytest"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/Sabitapata/job-tracker-api/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-purple" alt="License"></a>
</p>

<p align="center">
  <a href="#-quick-links">Quick Links</a> •
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-api-endpoints">API Endpoints</a> •
  <a href="#-local-setup">Local Setup</a> •
  <a href="#-docker-deployment">Docker</a> •
  <a href="#-dashboard-preview">Dashboard</a>
</p>

---

## 🎯 Why Job Tracker?

Tired of messy spreadsheets, forgotten follow-ups, and lost application links? 

**Job Tracker API** is built to give job seekers complete control and visibility over their career pipeline. Backed by a secure, high-performance **FastAPI** service and a clean **Streamlit** analytics dashboard, it combines enterprise-grade authentication with an intuitive user experience.

---

## ✨ Features

- 🔐 **Stateless JWT Authentication**: Secure login flow with OAuth2 password bearer tokens and Argon2 password hashing via `pwdlib`.
- 🛡️ **Per-User Data Isolation**: Multi-tenant authorization ensures users can strictly view, modify, and delete only their own records.
- 👤 **Developer Profiles**: Manage your career profile with verified links to your LinkedIn and GitHub profiles.
- ⚡ **Auto-Migrating Database Layer**: Built with SQLModel; effortlessly supports both local development on **SQLite** and cloud deployments on **PostgreSQL** with automatic startup schema synchronization.
- 📊 **Interactive Streamlit Dashboard**: Real-time metrics, status breakdowns (Applied ➔ Interview ➔ Offer ➔ Rejected), and visual bar charts.
- 🐳 **Containerized & CI-Tested**: Complete with Dockerfile containerization and GitHub Actions automated test pipeline.
- 📖 **Interactive API Documentation**: Auto-generated OpenAPI specification available instantly at `/docs` (Swagger UI) and `/redoc`.

---

## 🏗️ Architecture Overview

```text
 ┌───────────────────────────┐      ┌───────────────────────────┐
 │   Streamlit Dashboard     │      │   Swagger UI / OpenAPI    │
 │    (frontend/dashboard.py)│      │       (/docs, /redoc)     │
 └─────────────┬─────────────┘      └─────────────┬─────────────┘
               │                                  │
               └───────────────┐  ┌───────────────┘
                               ▼  ▼
                    ┌─────────────────────────┐
                    │    FastAPI Application  │
                    │         (app/main.py)   │
                    └────────────┬────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
        ┌─────────────────────┐     ┌─────────────────────┐
        │  Auth & Security    │     │  Routers & Logic    │
        │  • PyJWT            │     │  • /users           │
        │  • Argon2 (pwdlib)  │     │  • /applications    │
        └─────────────────────┘     └──────────┬──────────┘
                                               │
                                               ▼
                                    ┌─────────────────────┐
                                    │    SQLModel ORM     │
                                    │  (SQLite / Postgres)│
                                    └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|---|---|---|
| **API Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance async web framework |
| **ORM & Database** | [SQLModel](https://sqlmodel.tiangolo.com/) | Type-safe ORM powered by SQLAlchemy & Pydantic |
| **Databases** | [SQLite](https://www.sqlite.org/) / [PostgreSQL](https://www.postgresql.org/) | Embedded local storage or production cloud database |
| **Authentication** | [PyJWT](https://pyjwt.readthedocs.io/) & [Argon2](https://github.com/hynek/argon2-cffi) | Industry-standard password hashing and stateless token signing |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Strict data parsing and validation |
| **Frontend UI** | [Streamlit](https://streamlit.io/) | Fast, data-driven interactive web dashboard |
| **Testing** | [Pytest](https://docs.pytest.org/) & [HTTPX](https://www.python-httpx.org/) | Comprehensive automated test coverage |
| **Containerization** | [Docker](https://www.docker.com/) | Lightweight container images with Python 3.12 slim |

---

## 📡 API Endpoints

All protected endpoints require an `Authorization: Bearer <token>` header.

### 👤 Authentication & Profile
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/users/register` | Register a new user account | ❌ No |
| `POST` | `/users/login` | Authenticate and obtain JWT access token | ❌ No |
| `GET` | `/users/me` | Retrieve the authenticated user's profile | ✅ Yes |
| `PATCH` | `/users/me` | Update LinkedIn and GitHub profile links | ✅ Yes |

### 📋 Job Applications
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/applications/` | Create a new job application record | ✅ Yes |
| `GET` | `/applications/` | List all job applications for current user | ✅ Yes |
| `GET` | `/applications/{id}` | Retrieve details of a specific application | ✅ Yes |
| `PATCH` | `/applications/{id}` | Update application status, role, or notes | ✅ Yes |
| `DELETE` | `/applications/{id}` | Delete an application | ✅ Yes |

### 🩺 System & Health
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/` | API status and welcome message | ❌ No |
| `GET` | `/health` | Health-check endpoint for load balancers | ❌ No |
| `GET` | `/docs` | Interactive Swagger UI API documentation | ❌ No |

---

## 📂 Project Structure

```text
job-tracker-api/
├── .github/
│   └── workflows/
│       └── tests.yml            # CI test runner pipeline
├── app/
│   ├── routers/
│   │   ├── applications.py      # Job application CRUD endpoints
│   │   └── users.py             # User auth & profile endpoints
│   ├── auth.py                  # JWT encoding/decoding & Argon2 hashing
│   ├── config.py                # Pydantic BaseSettings environment config
│   ├── database.py              # Engine setup & auto-migration logic
│   ├── main.py                  # FastAPI lifespan & application factory
│   ├── models.py                # SQLModel database entity definitions
│   └── schemas.py               # Pydantic request & response schemas
├── frontend/
│   ├── dashboard.py             # Streamlit visual frontend dashboard
│   └── requirements.txt         # Frontend dependencies
├── tests/
│   ├── conftest.py              # In-memory SQLite test fixtures
│   ├── test_applications.py     # Application CRUD & authorization tests
│   └── test_users.py            # User registration, login, & profile tests
├── .env.example                 # Sample configuration values
├── Dockerfile                   # Production container definition
├── requirements.txt             # Pinned backend dependencies (UTF-8)
└── README.md                    # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/Sabitapata/job-tracker-api.git
cd job-tracker-api

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the sample environment file:

```bash
cp .env.example .env
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Fill in `.env`:
```env
SECRET_KEY=your-generated-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./job_tracker.db
```

> **Note**: For PostgreSQL, simply provide your connection string (e.g. `postgresql://user:password@localhost:5432/job_tracker`).

### 4. Run the API Server

```bash
python -m uvicorn app.main:app --reload
```

- 🌐 **Interactive Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- 🩺 **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### 5. Launch the Streamlit Dashboard

In a separate terminal tab:

```bash
streamlit run frontend/dashboard.py
```

Visit [http://localhost:8501](http://localhost:8501) to interact with your dashboard!

---

## 🐳 Docker Deployment

Run the API anywhere with Docker:

```bash
# Build the image
docker build -t job-tracker-api .

# Run container
docker run -d -p 8000:8000 --env-file .env --name job-tracker-app job-tracker-api
```

Test the container health:
```bash
curl http://localhost:8000/health
```

---

## 🧪 Running Automated Tests

The test suite runs against an isolated, high-speed, in-memory SQLite database:

```bash
python -m pytest -v
```

Expected output:
```text
============================= test session starts =============================
tests/test_applications.py::test_application_requires_login PASSED       [ 11%]
tests/test_applications.py::test_create_and_list_own_applications PASSED [ 22%]
tests/test_applications.py::test_user_cannot_access_another_users_application PASSED [ 33%]
tests/test_applications.py::test_update_and_delete_own_application PASSED [ 44%]
tests/test_users.py::test_register_user PASSED                           [ 55%]
tests/test_users.py::test_register_duplicate_email PASSED                [ 66%]
tests/test_users.py::test_login_user PASSED                              [ 77%]
tests/test_users.py::test_login_with_wrong_password PASSED               [ 88%]
tests/test_users.py::test_get_and_update_my_profile PASSED               [100%]

======================== 9 passed in 2.05s =========================
```

---

## 🔒 Security Best Practices Implemented

- **Password Storage**: Passwords are never stored in plain text. Hashed using **Argon2** (winner of the Password Hashing Competition).
- **Stateless Tokens**: JWTs expire automatically based on `ACCESS_TOKEN_EXPIRE_MINUTES`.
- **Strict Authorization**: Every database access strictly scopes records by the authenticated user's ID, preventing IDOR (Insecure Direct Object Reference) vulnerabilities.
- **Credential Hygiene**: Sensitive values (`SECRET_KEY`, `DATABASE_URL`) are read from environment variables; `.env` is ignored by `.gitignore`.

---

## 🗺️ Roadmap

- [ ] 📎 Resume and cover letter file attachments (AWS S3 / Cloudflare R2)
- [ ] ⏰ Follow-up reminder emails via automated background workers
- [ ] 🔍 Full-text search and pagination for large application volumes
- [ ] 📈 Interview conversion rate analytics and salary insights

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="center">
  Made with ❤️ by <a href="https://github.com/Sabitapata">Sabita Pata</a>
</p>