from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView

from store.services.views import MenuMixin
from .forms import CreateUserForm
from .services.views import AuthMixin


class CreateUser(MenuMixin, AuthMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'user/auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.set_redirect_url()
        context = super().get_context_data(**kwargs)
        header_context = self.get_header_context(
            title='Sign-up', page_title="Sign up", btn_text="Sign up")
        return context | header_context

    def form_valid(self, form):
        """
        Auto-login after signing up
        """
        user = form.save()
        login(self.request, user)
        return redirect(self.redirect_to())


class LogIn(MenuMixin, AuthMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'user/auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.set_redirect_url()
        context = super().get_context_data(**kwargs)
        header_context = self.get_header_context(
            title='Log-in', page_title='Log in', btn_text="Log in")
        return context | header_context

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.redirect_to())


class LogOut(AuthMixin, View):
    def get(self, request: WSGIRequest):
        self.set_redirect_url()
        redirect_to = self.redirect_to()
        logout(request)
        return redirect(redirect_to)
