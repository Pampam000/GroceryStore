from django.shortcuts import redirect

from grocerystore import settings

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

        http_referer = self.request.META.get("HTTP_REFERER")
        if http_referer:  # If user went to page after making an action
            if all([x not in http_referer for x in config.AUTH_URLS]):
                self.request.session[settings.PREVIOUS_URL_SESSION_ID] = \
                    self.request.META["HTTP_REFERER"]

    def redirect_to(self):

        if self.request.session.get(settings.PREVIOUS_URL_SESSION_ID):
            result = self.request.session[settings.PREVIOUS_URL_SESSION_ID]
            self.request.session[settings.PREVIOUS_URL_SESSION_ID] = ''
            return redirect(result)
        else:  # If user went to page by changing url in browser
            return redirect('store:home')
