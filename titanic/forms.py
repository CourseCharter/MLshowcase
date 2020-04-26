from django.forms import ModelForm
from . models import titanic_guess

class TitanicForm(ModelForm):
	class Meta:
		model=titanic_guess
		fields = '__all__'
	