from . import views
from django.urls import path

app_name = 'blog1'

urlpatterns = [
    path('', views.post_list, name = 'post_list'),
]