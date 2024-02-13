from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order

def home(request):
    # Implement logic to show latest orders or featured products
    return render(request, 'core/home.html')

@login_required
def user_dashboard(request):
    recent_orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]  # Get the 5 most recent orders
    context = {
        'recent_orders': recent_orders,
    }
    return render(request, 'core/user_dashboard.html', context)

def contact(request):
    # Contact form or information
    return render(request, 'core/contact.html')
