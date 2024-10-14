from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    LOGIN_FAILURES_TIME = 180  # seconds

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        ip = self._get_ip_from_request(request)
        cache_key = f'login_fail_{ip}'

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            login_failures = cache.get(cache_key, 0)
            login_failures += 1
            cache.set(cache_key, login_failures, self.LOGIN_FAILURES_TIME)
            raise e

        cache.delete(cache_key)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @staticmethod
    def _get_ip_from_request(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
