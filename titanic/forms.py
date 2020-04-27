from django import forms
from . models import titanic_guess

class TitanicForm(forms.Form):

    passengerclass=forms.ChoiceField(choices=[(1, "First"), (2, "Second"), (3, "Third") ])
    sex=forms.ChoiceField(choices=[(0, "Female"), (1, "Male") ])
    age=forms.IntegerField()
    relativesonboard=forms.IntegerField()
    ticketprice=forms.FloatField()
	