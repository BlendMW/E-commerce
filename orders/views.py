from django.shortcuts import render, redirect
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def view_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/view_order.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, id):
    order = Order.objects.get(id=id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})