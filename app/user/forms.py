from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CreateUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": UsernameField}

