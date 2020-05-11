from django.views.generic import TemplateView, View
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
# def NewTitanicForm(request):
#        return render(request,'titanic/titanic_form.html')

class NewTitanicForm(TemplateView):
	template_name = 'titanic/titanic_form.html'

	def get_context_data(self, **kwargs):
	 context = super().get_context_data(**kwargs)
	 titanic_table=create_HTML_table(titanic_df(pd.read_csv('titanic/data.csv')))
	 context['titanic_data_table'] = titanic_table
	 return context

	def titanic_guess(self, request):

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
				print(answer)
				#messages.success(request, 'Guess Submitted.')
				#messages.success(request, 'Your Fate: {}'.format(answer))
				#this is causing a problem for multiple attempts. the guess is being submitted multiple times but the response cannot be rendered multiple times
				#titanic_table=create_HTML_table(titanic_df(pd.read_csv('titanic/data.csv')))
				context = {
					'answer': answer,
					#'titanictable': titanic_table,
				}
			return render(request, 'titanic/titanic_form.html', {'context': context})

		else:
			form=TitanicForm()

		return render(request, 'titanic/titanic_form.html', {'form': form})

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
			print(answer)
			#messages.success(request, 'Guess Submitted.')
			#messages.success(request, 'Your Fate: {}'.format(answer))
			#this is causing a problem for multiple attempts. the guess is being submitted multiple times but the response cannot be rendered multiple times
			titanic_table=create_HTML_table(titanic_df(pd.read_csv('titanic/data.csv')))
			context = {
				'answer': answer,
				'titanictable': titanic_table,
			}
			return render(request, 'titanic/testform.html', {'context': context})

	else:
		form=TitanicForm()

	return render(request, 'titanic/testform.html', {'form': form}) 

def titanic_df(titanic_data):
			
	#cleaning the data
	titanic_data.replace('?', np.nan, inplace= True)
	titanic_data.replace({'male': 1, 'female': 0}, inplace=True)
	titanic_data = titanic_data.astype({"age": np.float64, "fare": np.float64})

	#combining siblings and parents into relatives
	titanic_data['relatives'] = titanic_data.apply (lambda row: int((row['sibsp'] + row['parch']) > 0), axis=1)
			
	titanic_df=pd.DataFrame(titanic_data)
			
	return titanic_df


# Creating a Styler object HTML table from a Dataframe
def create_HTML_table(dataframe):
    html_table_dataframe = (
        dataframe.style
        .set_properties(**{'font-size': '12pt', 'width': '100%', 'font-family': 'Calibri'})
        #.bar(subset=[column_bar_count], color='lightblue')
        .render()
    )
    return html_table_dataframe

