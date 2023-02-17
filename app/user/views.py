from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app import settings
from user.forms import CreateUserForm


class CreateUser(CreateView):
    form_class = CreateUserForm
    template_name = 'user/sign-up.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign-up'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('store:home')


class LogIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/log-in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log-in'
        return context

    def get_success_url(self):
        self.request.session[settings.CART_SESSION_ID] = {}
        return reverse_lazy('store:home')


def log_out(request):
    logout(request)
    return redirect('store:home')
