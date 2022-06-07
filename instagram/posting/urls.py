from django.urls import path, re_path
from . import views

app_name = 'posting'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.post_new, name='post_new'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('<int:pk>/unlike/', views.post_unlike, name='post_unlike'),
    path('<int:post_pk>/comment/new', views.comment_new, name='comment_new'),
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_page, name='user_page'),
]
