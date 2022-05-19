from tkinter import CASCADE
from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinLengthValidator

# Create your models here.
class Post(models.Model) :
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    message = models.TextField(
        validators = [MinLengthValidator(10)]
    )
    photo = models.ImageField(blank = True, upload_to = 'instagram/post/%Y%m%d')
    tag_set = models.ManyToManyField('Tag', blank = True)
    is_public = models.BooleanField(default = False, verbose_name = '공개여부')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models. DateTimeField(auto_now = True)
    
    def __str__(self) :
        # post_name = f'포스트 객체 ({self.id})'
        # return post_name
        return self.message
    
    def get_absolute_url(self):
        return reverse("instagram:post_detail", args = [self.pk])
    
    
    class Meta :
        ordering = ['-id']
    
    def message_length(self) :
        return len(self.message)
    
    def photo_tag(self) :
        if self.photo :
            return mark_safe(f'<img src="{self.photo.url}" style="width: 72px;" />')
        return None
    
    message_length.short_description = '메시지 글자 수'
    
class Comment(models.Model) :
    post = models.ForeignKey('instagram.Post',
                             on_delete = models.CASCADE,
                             limit_choices_to = {'is_public' : True})
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models. DateTimeField(auto_now = True)
    
class Tag(models.Model) :
    name = models.CharField(max_length = 50, unique = True)
    # post_set = models.ManyToManyField(Post)
    
    def __str__(self) :
        return self.name