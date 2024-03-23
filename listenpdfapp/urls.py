from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('readpage/', views.readpage, name='readpage'),
    path('error/', views.errorpage, name='errorpage')
]
