from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class Post(models.Model) :
    message = models.TextField()
    photo = models.ImageField(blank = True)
    is_public = models.BooleanField(default = False, verbose_name = '공개여부')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models. DateTimeField(auto_now = True)
    
    def __str__(self) :
        # post_name = f'포스트 객체 ({self.id})'
        # return post_name
        return self.message
    
    def message_length(self) :
        return len(self.message)
    
    def photo_tag(self) :
        if self.photo :
            return mark_safe(f'<img src="{self.photo.url}" style="width: 72px;" />')
        return None
    
    message_length.short_description = '메시지 글자 수'