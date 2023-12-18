from django.conf import settings

class AddCurrentDomainToCsrfTrustedOriginsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_origin = request.META.get('HTTP_ORIGIN')

        if current_origin and current_origin not in settings.CSRF_TRUSTED_ORIGINS:
            settings.CSRF_TRUSTED_ORIGINS.append(current_origin)

        response = self.get_response(request)
        return response
