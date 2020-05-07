from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from django.contrib import messages
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
from sklearn.preprocessing import StandardScaler
from joblib import load as jload

# Create your views here.
def NewTitanicForm(request):
       return render(request,'titanic/titanic_form.html')

class Titanic_Guess_View(viewsets.ModelViewSet):
	queryset = titanic_guess.objects.all()
	serializer_class = titanic_guessSerializers
		
#@api_view(["POST"])
def survived(unit):
	try:
		mdl=jload("/Users/user/projects/mlshowcase/titanic/titanic_model.pkl")
		#mydata=pd.read_excel('/Users/sahityasehgal/Documents/Coding/bankloan/test.xlsx')
		sc=StandardScaler()
		X=sc.fit_transform(unit)
		y_pred=mdl.predict_classes(X)
		#newdf=pd.DataFrame(y_pred, columns=['Survived'])
		#newdf=newdf.replace({1:'Survived', 0:'Perished'})
		
		return (str(y_pred))	
	except ValueError as e:
		return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def titanic_page_guess(request):

	if request.method =='POST':
		form=TitanicForm(request.POST)
		if form.is_valid():
			sex=form.cleaned_data['sex']
			pclass=form.cleaned_data['pclass']
			age=form.cleaned_data['age']
			relatives=form.cleaned_data['relatives']
			fare=form.cleaned_data['fare']
			myDict = (request.POST).dict()
			df=pd.DataFrame(myDict, index=[0])
			df=df.drop(['csrfmiddlewaretoken'], axis=1)
			answer = survived(df)
			messages.success(request, 'Guess Submitted.')
			#messages.success(request, 'Your Fate: {}'.format(answer))
			#this is causing a problem for multiple attempts. the guess is being submitted multiple times but the response cannot be rendered multiple times

	
	form=TitanicForm()

	return render(request, 'titanic/testform.html', {'form': form}) 

# Creating a Styler object HTML table from a Dataframe
def create_HTML_table(dataframe, colum_bar_count):
    html_table_dataframe = (
        dataframe.style
        .set_properties(**{'font-size': '12pt', 'width': '100%', 'font-family': 'Calibri'})
        .bar(subset=[colum_bar_count], color='lightblue')
        .render()
    )
    return html_table_dataframe