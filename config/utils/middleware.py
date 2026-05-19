class APIResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # Only process DRF JSON responses
        if hasattr(response, "data") and isinstance(response.data, dict):

            # Skip already formatted responses
            if "success" in response.data:
                return response

            response.data = {
                "success": True,
                "message": "",
                "data": response.data
            }

        return response