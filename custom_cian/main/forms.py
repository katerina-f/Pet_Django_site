from django import forms

from .models import Saller

class SallerProfileForm(forms.ModelForm):

    class Meta:
        model = Saller
        fields = ["first_name", "last_name", "email"]
