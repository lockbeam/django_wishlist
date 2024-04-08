from django import forms
from django.forms import FileInput, DateInput
from .models import Place

# forms.ModelFrom = a form for the webpage but it's related to the model
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

# need to include the above in the request to the homepage
# so needs to be added to views.py   

# this will make a custom date input (would otherwise be plain text field)
class DateInput(forms.DateInput):
    input_type = 'date' # override the default text input field - this will show a date picker to make sure input is actually a date

class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }


