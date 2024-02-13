from django import forms

class PaymentForm(forms.Form):
    # Example for Stripe; adjust accordingly if using a different provider
    stripe_token = forms.CharField()
    # Add any other fields as required by your payment process

# checkout/forms.py

from django import forms

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Shipping Address')
    payment_method = forms.ChoiceField(widget=forms.RadioSelect, choices=[('CC', 'Credit Card'), ('P', 'PayPal')], required=True, label='Payment Method')
    # Add other fields as necessary, such as billing information or payment method

