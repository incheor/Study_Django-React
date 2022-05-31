from django.urls import path
from . import views

app_name = 'coupang'

urlpatterns = [
    path('', views.Search, name='search'),
]