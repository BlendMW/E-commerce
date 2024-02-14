from django.shortcuts import render, get_object_or_404, redirect
from django.db import models  
from .models import Product, ProductVariant
from .forms import ReviewForm, ProductForm
from django.http import JsonResponse


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] if reviews else None
    images = product.images.all()  # Fetch all images associated with the product
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
            return redirect('product_detail', id=product.id)
    else:
        review_form = ReviewForm()
    return render(request, 'product/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'images': images  # Pass images to the template
    })

def add_to_cart(request, product_id):
    if request.method == 'POST':
        color = request.POST.get('color')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        # Logic to add the product with selected options to the cart
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        # Add your logic to manipulate the cart data
        cart[product_id] = {
            'id': product_id,
            'name': product.name,
            'price': str(product.price),
            'color': color,
            'size': size,
            'quantity': quantity,
        }
        request.session['cart'] = cart

    return redirect('cart_detail')

def product_management(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm()
    return render(request, 'product/product_management.html', {'products': products, 'form': form})

def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product/product_view.html', {'product': product})


def get_variant_quantity(request):
    color = request.GET.get('color')
    size = request.GET.get('size')
    product_id = request.GET.get('product_id')
    variant = ProductVariant.objects.filter(product_id=product_id, color=color, size=size).first()
    if variant:
        return JsonResponse({'quantity': variant.quantity})
    else:
        return JsonResponse({'quantity': 0})
 
