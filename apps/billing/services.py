from datetime import timedelta
import logging

from django.db import transaction
from django.utils.timezone import now

from apps.audit.services import AuditService
from apps.billing.models import Payment
from apps.subscriptions.models import (
    Subscription,
    Plan
)
from apps.subscriptions.services import (
    SubscriptionService
)

logger = logging.getLogger(__name__)


class BillingService:

    SUBSCRIPTION_DURATION_DAYS = 30

    @staticmethod
    @transaction.atomic
    def process_payment(
        org,
        plan,
        request=None
    ):

        payment = Payment.objects.create(
            organization=org,
            plan=plan,
            amount=plan.price,
            status="paid",
            paid_at=now(),
            metadata={
                "billing_type": "subscription"
            }
        )

        subscription, created = (
            Subscription.objects.update_or_create(
                organization=org,
                defaults={
                    "plan": plan,
                    "is_active": True,
                    "start_date": now(),
                    "end_date": (
                        now() +
                        timedelta(
                            days=BillingService.SUBSCRIPTION_DURATION_DAYS
                        )
                    )
                }
            )
        )

        # cache invalidation
        SubscriptionService.invalidate_subscription_cache(
            org.id
        )

        # audit logging
        AuditService.log_action(
            action="upgrade_plan",
            resource_type="subscription",
            resource_id=subscription.id,
            organization=org,
            user=(
                request.user
                if request and request.user.is_authenticated
                else None
            ),
            request=request,
            metadata={
                "plan": plan.name,
                "payment_id": payment.id,
                "subscription_created": created,
            }
        )

        # structured logging
        logger.info(
            f"Subscription activated | "
            f"organization={org.id} | "
            f"plan={plan.code} | "
            f"payment_id={payment.id}"
        )

        return {
            "payment": payment,
            "subscription": subscription,
            "payment_id": payment.id,
            "subscription_id": subscription.id,
            "plan": plan.name,
            "amount": str(plan.price),
            "status": payment.status,
        }

    @staticmethod
    @transaction.atomic
    def change_plan(
        org,
        new_plan,
        request=None
    ):

        subscription = (
            Subscription.objects
            .select_related("plan")
            .get(organization=org)
        )

        old_plan = subscription.plan

        subscription.plan = new_plan

        subscription.save(
            update_fields=["plan"]
        )

        payment = Payment.objects.create(
            organization=org,
            plan=new_plan,
            amount=new_plan.price,
            status="paid",
            paid_at=now(),
            metadata={
                "billing_type": "plan_change",
                "old_plan": old_plan.code,
                "new_plan": new_plan.code,
            }
        )

        # cache invalidation
        SubscriptionService.invalidate_subscription_cache(
            org.id
        )

        # audit trail
        AuditService.log_action(
            action="upgrade_plan",
            resource_type="subscription",
            resource_id=subscription.id,
            organization=org,
            user=(
                request.user
                if request and request.user.is_authenticated
                else None
            ),
            request=request,
            metadata={
                "old_plan": old_plan.name,
                "new_plan": new_plan.name,
                "payment_id": payment.id
            }
        )

        # structured logs
        logger.info(
            f"Plan changed | "
            f"organization={org.id} | "
            f"old_plan={old_plan.code} | "
            f"new_plan={new_plan.code} | "
            f"payment_id={payment.id}"
        )

        return {
            "payment": payment,
            "subscription": subscription,
            "old_plan": old_plan.name,
            "new_plan": new_plan.name,
            "payment_id": payment.id,
            "status": payment.status,
        }