from django.core.management.base import BaseCommand

from apps.subscriptions.models import Plan


FREE_FEATURES = {
    "api_keys": False,
    "analytics": False,
    "priority_support": False,
    "advanced_usage": False,
}

PRO_FEATURES = {
    "api_keys": True,
    "analytics": True,
    "priority_support": False,
    "advanced_usage": True,
}

ENTERPRISE_FEATURES = {
    "api_keys": True,
    "analytics": True,
    "priority_support": True,
    "advanced_usage": True,
}


class Command(BaseCommand):

    help = "Seed subscription plans"

    def handle(self, *args, **kwargs):

        plans = [
            {
                "name": "Free",
                "code": "free",
                "price": 0,
                "request_limit_per_month": 1000,
                "features": FREE_FEATURES,
            },
            {
                "name": "Pro",
                "code": "pro",
                "price": 29.99,
                "request_limit_per_month": 10000,
                "features": PRO_FEATURES,
            },
            {
                "name": "Enterprise",
                "code": "enterprise",
                "price": 199.99,
                "request_limit_per_month": 100000,
                "features": ENTERPRISE_FEATURES,
            },
        ]

        for plan_data in plans:

            Plan.objects.update_or_create(
                code=plan_data["code"],
                defaults=plan_data
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Plans seeded successfully"
            )
        )