from django.contrib import admin
from django.urls import path
from . import views

app_name = 'DataExcel'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('loginValidate/', views.loginValidate, name='loginValidate'),
    path('index/', views.index, name="index"),
    path('upload/', views.upload, name="upload"),
    path('validate/', views.validate, name="validate"),
    path('download/', views.download, name="download"),
    path('home/', views.home, name="home"),
    path('selectRecord/', views.selectRecord, name="selectRecord"),
    path('navigate/', views.navi, name="navigate"),
    path('homePage/', views.homePage, name="homePage"),
    path('page/', views.page, name="page")
]
