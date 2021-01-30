from django import forms


class ProfileForm(forms.Form):
    first_name = forms.CharField(label="Имя")
    last_name = forms.Charfield(label="Фамилия")
    email = forms.EmailField(label="Email")
