from django import forms
from .models import Place

# forms.ModelFrom = a form for the webpage but it's related to the model
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

# need to include the above in the request to the homepage
# so needs to be added to views.py    