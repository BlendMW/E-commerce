from django.urls import path
from .views import home, user_dashboard, contact

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('contact/', contact, name='contact'),
    # Add more paths as needed
]
