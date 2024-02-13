from django.shortcuts import render, get_object_or_404
from .models import Product
from .forms import ReviewForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] if reviews else None
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
        'review_form': review_form
    })
