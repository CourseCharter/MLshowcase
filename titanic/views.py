from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . forms import TitanicForm
from . models import titanic_guess
from . serializers import titanic_guessSerializers
import pickle
from sklearn.externals import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd

# Create your views here.
def NewTitanicForm(request):
       return render(request,'titanic/titanic_form.html')

class Titanic_Guess_View(viewsets.ModelViewSet):
	queryset = titanic_guess.objects.all()
	serializer_class = titanic_guessSerializers
		
#@api_view(["POST"])
def survived(unit):
	try:
		mdl=joblib.load("/Users/user/projects/mlshowcase/titanic/titanic_model.pkl")
		#mydata=pd.read_excel('/Users/sahityasehgal/Documents/Coding/bankloan/test.xlsx')
		mydata=unit.data
		unit=np.array(list(mydata.values()))
		unit=unit.reshape(1,-1)
		X=unit
		y_pred=mdl.predict(X)
		y_pred=(y_pred>0.58)
		newdf=pd.DataFrame(y_pred, columns=['Survived'])
		newdf=newdf.replace({True:'Survived', False:'Perished'})
		return ('Your Status is {}'.format(newdf))
	except ValueError as e:
		return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def titanic_page_guess(request):

	if request.method =='POST':
		form=TitanicForm(request.POST)
		if form.is_valid():
			Pclass=form.cleaned_data['passengerclass']
			sex=form.cleaned_data['sex']
			age=form.cleaned_data['age']
			relatives=form.cleaned_data['relativesonboard']
			price=form.cleaned_data['ticketprice']
			myDict = (request.POST).dict()
			df=pd.DataFrame(myDict, index=[0])
			print(survived(df))

	form=TitanicForm()

	return render(request, 'titanic/testform.html', {'form': form})
