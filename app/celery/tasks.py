from app.celery.celery_config import celery_app

@celery_app.task(name="notify_admins")
def notify_admins():
    print(f"Notifying admins...")
