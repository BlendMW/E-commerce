from django.shortcuts import render, redirect
from orders.models import Order
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# checkout/views.py

from django.shortcuts import render, redirect
from .forms import CheckoutForm  # Import the CheckoutForm

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data
            # For demonstration, simply redirecting to a 'complete' page
            return redirect('checkout_complete')
    else:
        form = CheckoutForm()

    return render(request, 'checkout/checkout.html', {'form': form})


def payment(request):
    if request.method == 'POST':
        # Example: Process payment information here
        # Integrate with a payment gateway (e.g., Stripe, PayPal)
        
        # After processing payment, you might redirect to a 'complete' page
        # or render a template with a success message, for example:
        return redirect('checkout_complete')
    else:
        # For a GET request, you should render a template that contains
        # the payment form or payment instructions.
        return render(request, 'checkout/payment.html')
        # Ensure 'checkout/payment.html' exists and contains the relevant
        # form or instructions for submitting payment.

def complete(request):
    try:
        order = Order.objects.latest('id')
    except ObjectDoesNotExist:
        # Handle the case where an order does not exist
        # For example, redirect to a different page or show an error message
        return HttpResponse("No orders found.", status=404)  # Or use render to show a custom template

    context = {'order': order}
    return render(request, 'checkout/complete.html', context)