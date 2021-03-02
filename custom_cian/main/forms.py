from django import forms
from django.core.exceptions import ValidationError

from .models import Realty, Saller


class RealtyForm(forms.ModelForm):

    class Meta:
        model = Realty
        exclude = ["published_at", "slug"]


class SallerProfileForm(forms.ModelForm):
    age = forms.IntegerField(max_value=120, min_value=0)

    class Meta:
        model = Saller
        fields = ["first_name", "last_name", "email"]

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise ValidationError("Вы должны быть старше 18 лет!", code="invalid")
