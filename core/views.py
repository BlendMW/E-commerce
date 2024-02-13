from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order

def home(request):
    # Implement logic to show latest orders or featured products
    return render(request, 'core/home.html')

def contact(request):
    # Contact form or information
    # Implement form handling logic if it's a form submission
    if request.method == 'POST':
        # Process the form data, send email, or save contact info
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        # Dummy response for demonstration
        return HttpResponse("Thank you for contacting us!")
    else:
        return render(request, 'core/contact.html')

def home_view(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    # Corrected indentation
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]  # Get the 5 most recent orders
    context = {
        'recent_orders': recent_orders,
        'user': request.user  # Pass the user in the context
    }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)  # Ensure we're using the user's profile
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'core/edit_profile.html', {'form': form})

