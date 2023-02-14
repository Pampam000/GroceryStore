from django import forms as f


class CartAddProductForm(f.Form):
    quantity = f.IntegerField(min_value=1)

