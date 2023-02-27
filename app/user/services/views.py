from app import settings

from . import config


class AuthMixin:
    def set_redirect_url(self):
        """
        Set redirect url if http_referer does not contain any of auth_urls.
        It is necessary for redirecting on not auth pages
        Good Example for condition:
            http_referer = http://127.0.0.1:8000/
        Bad Examples:
             http_referer = http://127.0.0.1:8000/log-in/
             http_referer = http://127.0.0.1:8000/log-out/
             http_referer = http://127.0.0.1:8000/sign-up/

        """

        http_referer = self.request.META["HTTP_REFERER"]

        if all([x not in http_referer for x in config.AUTH_URLS]):
            self.request.session[settings.AUTH_FROM_URL_SESSION_ID] = \
                self.request.META["HTTP_REFERER"]

    def redirect_to(self):
        return self.request.session[settings.AUTH_FROM_URL_SESSION_ID]
