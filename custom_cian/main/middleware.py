from django.utils.deprecation import MiddlewareMixin


class MobileMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)

    def process_request(self, request):
        mobile_version = request.META.get("HTTP_USER_AGENT", '')
        request.mobile = mobile_version in ["iphone", "mobile", "android"]

        response = self.get_response(request)

        return response
