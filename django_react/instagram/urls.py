from . import views
from django.urls import path

app_name = 'instagram'

urlpatterns = [
    path('', views.post_list, name = 'post_list'),
    path('<int:pk>/', views.post_detail, name = 'post_detail')
]