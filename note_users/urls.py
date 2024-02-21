from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login),
    path('signup', views.signup),
    path('',views.get_routes)
]
