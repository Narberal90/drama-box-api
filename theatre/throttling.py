from rest_framework.throttling import BaseThrottle
from django.core.cache import cache


class LoginFailRateThrottle(BaseThrottle):
    INCORRECT_LOGIN_TRIES = 3
    LOGIN_FAILURES_BLOCK_TIME = 300

    def allow_request(self, request, view):
        ip = self.get_ident(request)

        fail_key = f"login_fail_{ip}"
        block_key = f"login_block_{ip}"

        if cache.get(block_key):
            return False

        login_failures = cache.get(fail_key, 0)

        if login_failures >= self.INCORRECT_LOGIN_TRIES:
            cache.set(block_key, True, self.LOGIN_FAILURES_BLOCK_TIME)
            return False

        return True

    def wait(self):
        return self.LOGIN_FAILURES_BLOCK_TIME
