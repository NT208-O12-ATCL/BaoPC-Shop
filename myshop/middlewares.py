from django.conf import settings

class AddCurrentDomainToCsrfTrustedOriginsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy tên miền hiện tại từ request
        current_origin = request.META.get('HTTP_ORIGIN')

        # Kiểm tra nếu tên miền hiện tại đã tồn tại trong danh sách trusted origins
        if current_origin and current_origin not in settings.CSRF_TRUSTED_ORIGINS:
            # Thêm tên miền hiện tại vào danh sách trusted origins
            settings.CSRF_TRUSTED_ORIGINS.append(current_origin)

        response = self.get_response(request)
        return response
