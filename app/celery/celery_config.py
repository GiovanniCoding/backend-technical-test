# app/celery_config.py

from celery import Celery

from app.core.config import settings

# Configurar Celery
celery_app = Celery(
    "my_app", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

# Configuración adicional
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["app.celery.tasks"])
