from django.urls import path,include,re_path
from titanic import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('titanic', views.Titanic_Guess_View)

app_name='titanic'
urlpatterns = [
    path('',views.NewTitanicForm.as_view(),name='titanic'),
    path('api/', include(router.urls)),
    path('home/', views.Titanic_Home,name='titanic_home'),
    #path('result/', views.result, name='result'),
]