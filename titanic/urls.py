from django.urls import path,include,re_path
from titanic import views

urlpatterns = [
    path('',views.NewTitanicForm,name='titanic'),
]