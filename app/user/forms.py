from django.contrib.auth import get_user_model
from django.contrib.auth import forms as f


class CreateUserForm(f.UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": f.UsernameField}

