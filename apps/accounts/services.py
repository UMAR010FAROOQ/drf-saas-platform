from apps.accounts.tasks import send_welcome_email


def create_user_flow(user):
    send_welcome_email.delay(user.email)