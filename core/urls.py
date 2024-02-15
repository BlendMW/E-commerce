from django.urls import path
from .views import home, profile, contact, edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

      
    ]
