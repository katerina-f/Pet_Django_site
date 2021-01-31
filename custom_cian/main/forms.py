from django import forms

from .models import Realty

class ProfileForm(forms.Form):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Email")


class RealtyForm(forms.ModelForm):

    class Meta:
        model = Realty
        exclude = ["published_at", "slug"]
