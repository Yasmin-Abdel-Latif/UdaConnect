import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Prefer `DATABASE_URL` environment variable, fall back to sensible default.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://udaconnect:udaconnect@postgres:5432/udaconnect",
)

# Allow building a URL from PGUSER/PGPASSWORD if provided and DATABASE_URL is not set
if "DATABASE_URL" not in os.environ:
    pguser = os.environ.get("PGUSER")
    pgpass = os.environ.get("PGPASSWORD")
    if pguser and pgpass:
        DATABASE_URL = f"postgresql://{pguser}:{pgpass}@postgres:5432/udaconnect"

# Create engine with a small retry loop so services can wait for Postgres readiness
engine = None
for _ in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        # attempt a short connection check
        with engine.connect():
            pass
        break
    except Exception:
        time.sleep(2)
else:
    # Final attempt — will raise the underlying connection error when used
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
