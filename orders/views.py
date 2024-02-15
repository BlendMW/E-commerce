from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import Order
from django.db.models import Sum
from django.db import transaction
from django.urls import reverse

@transaction.atomic
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@transaction.atomic
def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_details.html', {'order': order})

@transaction.atomic
def track_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            return JsonResponse({'status': order.status})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Order not found'}, status=404)
    return render(request, 'orders/track_order.html')

@transaction.atomic
def order_history(request, order_id=None):
    if order_id:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'orders/order_details.html', {'order': order})
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@transaction.atomic
def order_analytics(request):
    user_orders = Order.objects.filter(user=request.user)
    total_spent = user_orders.aggregate(Sum('total'))
    order_count = user_orders.count()
    # Additional analytics can be added here

    return render(request, 'orders/analytics.html', {
        'total_spent': total_spent,
        'order_count': order_count,
        # Additional context variables for analytics
    })

@transaction.atomic
def update_order(request, order_id):
    if request.method == 'POST':
        # Assume you're updating order details based on POST data
        order = get_object_or_404(Order, pk=order_id)
        # Example: Update the order's shipping address
        order.shipping_address = request.POST.get('shipping_address', '')
        order.save()
        # Redirect to a specific view after update
        return HttpResponseRedirect(reverse('order_details', args=[order_id]))
    else:
        # If not a POST request, show the order update form
        return render(request, 'orders/update_order.html', {'order': Order.objects.get(pk=order_id)})

@transaction.atomic
def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    # Redirect to the orders list after deletion
    return HttpResponseRedirect(reverse('order_list'))

@transaction.atomic
def order_create(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        
        return redirect(reverse('order_detail', args=[order.id]))
    else:
        # Handle GET request or show an error/form
        pass