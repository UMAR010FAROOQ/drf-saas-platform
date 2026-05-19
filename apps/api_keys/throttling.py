from rest_framework.throttling import SimpleRateThrottle
import hashlib


class APIKeyRateThrottle(SimpleRateThrottle):
    scope = "api_key"

    def get_cache_key(self, request, view):
        if not hasattr(request, "organization") or request.user:
            return None

        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return None

        hashed = hashlib.sha256(api_key.encode()).hexdigest()
        return f"throttle_api_key_{hashed}"




class OrganizationRateThrottle(SimpleRateThrottle):
    scope = "organization"

    def get_cache_key(self, request, view):
        org = getattr(request, "organization", None)

        if not org:
            return None

        return f"throttle_org_{org.id}"

    def get_rate(self):
        request = getattr(self, "request", None)

        if not request:
            return "100/hour"

        org = getattr(request, "organization", None)

        if not org:
            return "100/hour"

        plan = getattr(org, "plan", "free")

        if plan == "free":
            return "100/hour"
        elif plan == "pro":
            return "1000/hour"

        return "100/hour"

    def allow_request(self, request, view):
        self.request = request  
        return super().allow_request(request, view)