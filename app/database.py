from sqlalchemy import inspect, text
from sqlmodel import SQLModel, Session, create_engine

from app.config import settings

database_url = settings.database_url
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

connect_args = {}
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    database_url,
    connect_args=connect_args,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        user_table = "user" if "user" in table_names else ("users" if "users" in table_names else None)
        if user_table:
            existing_columns = {col["name"] for col in inspector.get_columns(user_table)}
            with engine.begin() as conn:
                for col_name in ("linkedin_url", "github_url"):
                    if col_name not in existing_columns:
                        quote = '"' if engine.dialect.name == "postgresql" else ""
                        conn.execute(
                            text(f"ALTER TABLE {quote}{user_table}{quote} ADD COLUMN {col_name} VARCHAR")
                        )
    except Exception:
        pass


def get_session():
    with Session(engine) as session:
        yield session