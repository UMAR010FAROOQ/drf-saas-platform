from celery import shared_task


@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, email):
    try:
        print(f"Sending welcome email to {email}")
        return True

    except Exception as e:
        raise self.retry(countdown=5)