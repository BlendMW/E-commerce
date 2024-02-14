from django.shortcuts import redirect, get_object_or_404, render
from .models import CartItem, Product
from .forms import CartAddProductForm
from django.http import JsonResponse

def cart_detail(request):
    cart = request.session.get('cart', {})
    product_ids = [item.split('_')[0] for item in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    cart_total = 0
    for product in products:
        for key, value in cart.items():
            if str(product.id) in key:
                total_price = int(cart[key]['quantity']) * product.price
                cart_items.append({
                    'product': product,
                    'quantity': cart[key]['quantity'],
                    'total_price': total_price,
                })
                cart_total += total_price
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'cart_total': cart_total})

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        item_id = f'{product_id}_{cd.get("size")}_{cd.get("color")}'
        if item_id not in cart:
            cart[item_id] = {'quantity': 0, 'price': str(product.price)}
        cart[item_id]['quantity'] += cd['quantity']
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    item_id = request.GET.get('item_id')
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_update(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for key in cart.keys():
            quantity_key = f'quantity_{key}'
            if quantity_key in request.POST:
                new_quantity = int(request.POST[quantity_key])
                cart[key]['quantity'] = new_quantity
        request.session['cart'] = cart
    return redirect('cart_detail')

def ajax_cart_update(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('quantity'))
        if item_id in cart:
            cart[item_id]['quantity'] = new_quantity
            request.session['cart'] = cart
        return JsonResponse({'success': True})

def ajax_cart_add(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))
        
        item_id = f'{product_id}_{size}_{color}'
        if item_id not in cart:
            cart[item_id] = {'quantity': 0, 'price': str(product.price)}
        
        cart[item_id]['quantity'] += quantity
        request.session['cart'] = cart
        
        return JsonResponse({'success': True, 'message': 'Product added to cart'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def ajax_cart_remove(request):
    cart = request.session.get('cart', {})
    item_id = request.GET.get('item_id')
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return JsonResponse({'success': True})
