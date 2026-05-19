from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, data=None, message="", status=None, success=True, **kwargs):

        super().__init__(
            data={
                "success": success,
                "message": message,
                "data": data
            },
            status=status,
            **kwargs
        )