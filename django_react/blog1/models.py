from venv import create
from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model) :
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete = models.CASCADE,
                               related_name = '+')
    title = models.CharField(max_length = 100)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)