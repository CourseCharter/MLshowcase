from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def NewTitanicForm(request):
       return render(request,'titanic/titanic_form.html')