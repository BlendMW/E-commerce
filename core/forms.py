from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Corrected to use UserProfile
        fields = ['bio', 'mobile_number', 'address', 'city', 'country', 'postal_code', 'profile_picture']
