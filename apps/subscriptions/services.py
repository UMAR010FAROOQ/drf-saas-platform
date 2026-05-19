from django.core.cache import cache

from apps.subscriptions.models import Subscription


class SubscriptionService:

    CACHE_TIMEOUT = 300

    @staticmethod
    def get_active_subscription(org):

        cache_key = f"org_subscription_{org.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        subscription = (
            Subscription.objects
            .select_related("plan")
            .filter(
                organization=org,
                is_active=True
            )
            .first()
        )

        cache.set(
            cache_key,
            subscription,
            timeout=SubscriptionService.CACHE_TIMEOUT
        )

        return subscription

    @staticmethod
    def has_active_subscription(org):

        subscription = (
            SubscriptionService.get_active_subscription(org)
        )

        if not subscription:
            return False

        if subscription.is_expired():
            return False

        return subscription.is_active

    @staticmethod
    def has_feature(org, feature_name):

        subscription = (
            SubscriptionService.get_active_subscription(org)
        )

        if not subscription:
            return False

        return subscription.plan.features.get(
            feature_name,
            False
        )

    @staticmethod
    def get_plan_limit(org):

        subscription = (
            SubscriptionService.get_active_subscription(org)
        )

        if not subscription:
            return 0

        return subscription.plan.request_limit_per_month
    


    @staticmethod
    def resolve_feature(org, feature_name):

        subscription = (
            SubscriptionService.get_active_subscription(org)
        )

        if not subscription:
            return False

        features = subscription.plan.features or {}

        return features.get(feature_name, False)    


    @staticmethod
    def invalidate_subscription_cache(org_id):

        cache_key = f"org_subscription_{org_id}"

        cache.delete(cache_key)


