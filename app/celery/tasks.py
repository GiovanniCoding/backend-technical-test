import boto3

from app.celery.celery_config import celery_app
from app.core.config import settings

ses_client = boto3.client(
    "ses",
    region_name="us-east-1",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


@celery_app.task
def notify_users(email_list: list, reason: str, product_name: str):
    """
    Task to notify multiple users.
    email_list is a list of the emails to notify.
    """
    try:
        print(f"Sending email to {email_list} for reason {reason}")
        subject, body = get_email_content(reason, product_name)
        for email in email_list:
            send_email.delay(email, subject, body)
    except Exception as exc:
        print(f"Failed to send email to {email_list}: {str(exc)}")


@celery_app.task(bind=True, max_retries=5, default_retry_delay=5)
def send_email(self, email, subject, html_body):
    """
    Send an email to a single user.
    """
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

    try:
        response = ses_client.send_email(
            Destination={
                "ToAddresses": [email],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": html_body,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": subject,
                },
            },
            Source="egiovanni.vo@gmail.com",
        )
        print(f"Email sent! Message ID: {response['MessageId']} to {email}")

    except Exception as exc:
        print(f"Failed to send email to {email}: {str(exc)}")
        self.retry(exc=exc)


def get_email_content(reason, product_name):
    """
    Return the subject and body of the email based on the reason.
    """
    if reason == "create":
        return (
            "New Product!",
            f"""
                <html>
                    <head></head>
                    <h1 style='text-align:center'>Amazing Store</h1>
                    <p>A new product was created: {product_name}</p>
                    </body>
                </html>
            """,
        )
    elif reason == "update":
        return (
            "A Product Change!",
            f"""
                <html>
                    <head></head>
                    <h1 style='text-align:center'>Amazing Store</h1>
                    <p>The product :{product_name} changed.</p>
                    </body>
                </html>
            """,
        )
    elif reason == "delete":
        return (
            "A Product was deleted",
            f"""
                <html>
                    <head></head>
                    <h1 style='text-align:center'>Amazing Store</h1>
                    <p>A product was deleted: {product_name}</p>
                    </body>
                </html>
            """,
        )
    return (
        "No subject",
        """
            <html>
                <head></head>
                <h1 style='text-align:center'>Amazing Store</h1>
                <p>No content available for the specified reason.</p>
                </body>
            </html>
        """,
    )
