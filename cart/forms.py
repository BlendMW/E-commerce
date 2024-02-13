from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    # Assuming your Product model has `size` and `color` attributes
    size = forms.ChoiceField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], required=False)
    color = forms.ChoiceField(choices=[('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green')], required=False)
