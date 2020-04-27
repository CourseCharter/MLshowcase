from django.urls import path,include,re_path
from titanic import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('titanic', views.Titanic_Guess_View)

urlpatterns = [
    path('',views.NewTitanicForm,name='titanic'),
    path('api/', include(router.urls)),
    path('status/', views.Titanic_Guess_View),
    path('test/', views.titanic_page_guess, name='testform')
]