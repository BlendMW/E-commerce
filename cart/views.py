from django.shortcuts import redirect, get_object_or_404, render
from .models import CartItem, Product
from .forms import CartAddProductForm

def cart_detail(request):
    cart = request.session.get('cart', {})
    product_ids = [item.split('_')[0] for item in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    for product in products:
        for key, value in cart.items():
            if str(product.id) in key:
                cart_items.append({
                    'product': product,
                    'quantity': cart[key]['quantity'],
                    'total_price': int(cart[key]['quantity']) * product.price,
                    # Add any variations here
                                    })
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})

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
    product = get_object_or_404(Product, id=product_id)
    item_id = f'{product_id}_{request.POST.get("size")}_{request.POST.get("color")}'
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return redirect('cart_detail')
