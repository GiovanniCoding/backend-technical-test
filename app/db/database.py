from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from alembic import command
from alembic.config import Config
from app.core.config import settings
from app.db.models.user import User, UserRepository

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def create_root_user():
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if user:
            return
        user_repository = UserRepository(db)
        user_repository.create(
            username="root",
            hashed_password="$2b$12$K6C642APMSAqBPn/AAA7LOJp1.syvOXIl3PWM5TaKlZ2ugd.SU/yC",
            is_active=True,
            is_admin=True,
        )
    finally:
        db.close()
