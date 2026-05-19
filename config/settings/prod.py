from .base import *
from datetime import timedelta

DEBUG = False

ALLOWED_HOSTS = ["*"] # Update with your actual domain

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}