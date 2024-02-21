from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_note),
    path('share', views.share_note),
    path('version-history/<str:id>', views.get_version_history),
    path('<uuid:id>', views.get_note),
    
]
