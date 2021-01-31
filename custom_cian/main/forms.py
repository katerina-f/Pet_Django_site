from django import forms

from .models import Saller

class SallerProfileForm(forms.ModelForm):
    age = forms.IntegerField(max_value=120, min_value=18)

    class Meta:
        model = Saller
        fields = ["first_name", "last_name", "email"]
