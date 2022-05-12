from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_list),
    path('<int:pk>/', views.post_detail),
]