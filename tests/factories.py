import factory

from datetime import timedelta
from django.utils.timezone import now
from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.subscriptions.models import Plan
from apps.subscriptions.models import Subscription



class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(
        lambda n: f"user{n}@test.com"
    )

    is_active = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):

        password = extracted or "testpass123"

        obj.set_password(password)

        if create:
            obj.save()




class OrganizationFactory(
    factory.django.DjangoModelFactory
):

    class Meta:
        model = Organization

    name = factory.Sequence(
        lambda n: f"Organization {n}"
    )

    owner = factory.SubFactory(UserFactory)


class PlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Plan

    name = "Pro"

    code = factory.Sequence(
        lambda n: f"pro_{n}"
    )

    price = 99.99

    request_limit_per_month = 10000

    features = {
        "api_keys": True,
        "analytics": True,
        "priority_support": False,
        "advanced_usage": True,
    }


class SubscriptionFactory(
    factory.django.DjangoModelFactory
):

    class Meta:
        model = Subscription

    organization = factory.SubFactory(
        OrganizationFactory
    )

    plan = factory.SubFactory(
        PlanFactory
    )

    is_active = True

    start_date = factory.LazyFunction(now)

    end_date = factory.LazyFunction(
        lambda: now() + timedelta(days=30)
    )