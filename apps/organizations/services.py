from django.db import transaction
from apps.organizations.models import Organization, Membership
from django.core.cache import cache

class OrganizationService:

    @staticmethod
    @transaction.atomic
    def create_organization(user, name):
        """
        Create organization and assign creator as admin.
        """

        # 1. Create organization
        org = Organization.objects.create(
            name=name,
            owner=user
        )

        # 2. Create membership (admin role)
        Membership.objects.create(
            user=user,
            organization=org,
            role="admin"
        )

        return org

    @staticmethod
    def get_user_organizations(user):
        """
        Get all organizations where user is a member.
        """
        return Organization.objects.filter(memberships__user=user)

    @staticmethod
    def is_member(user, org):
        """
        Check if user belongs to organization.
        """
        return Membership.objects.filter(
            user=user,
            organization=org
        ).exists()

    @staticmethod
    def get_membership(user, org):
        """
        Get membership object (to access role).
        """
        return Membership.objects.filter(
            user=user,
            organization=org
        ).first()


    # invite_user
    @staticmethod
    @transaction.atomic
    def invite_user(org, email):
        from apps.accounts.models import User

        # 1. Get or create user
        user, user_created = User.objects.get_or_create(email=email)

        # 2. If new user → disable password (no login yet)
        if user_created:
            user.set_unusable_password()
            user.save()

        # 3. Prevent duplicate membership
        membership, membership_created = Membership.objects.get_or_create(
            user=user,
            organization=org,
            defaults={"role": "member"}
        )

        # 4. Structured response
        return {
            "user": user,
            "membership": membership,
            "user_created": user_created,
            "membership_created": membership_created,
        }
    

    @staticmethod
    def get_user_organizations(user):
        cache_key = f"user_orgs_{user.id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        orgs = Organization.objects.filter(memberships__user=user)

        # convert to safe primitive data
        data = list(
            orgs.values("id", "name", "created_at")
        )

        cache.set(cache_key, data, timeout=60)

        return data
    


    @staticmethod
    @transaction.atomic
    def create_organization(user, name):
        org = Organization.objects.create(
            name=name,
            owner=user
        )

        Membership.objects.create(
            user=user,
            organization=org,
            role="admin"
        )

        # invalidate user org cache
        cache.delete(f"user_orgs_{user.id}")

        return org