from django import forms
from . models import City


class CreateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Check the weather for...'})}
