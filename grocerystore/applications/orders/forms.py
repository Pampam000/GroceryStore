from django import forms as f
from .models import Order


class OrderCreateForm(f.ModelForm):

    class Meta:
        model = Order
        fields = ('address',)
