from django.db import models
from django.conf import settings
from django.urls import reverse
import re


# 이렇게 BaseModel(이름은 자유임)을 만들어놓고
class BaseModel(models.Model):
    # 필드를 정의해놓고
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Meta 클래스의 abstract 속성을 True로 해놓으면
    # 나중에 모델 클래스를 정의할 때 이 모델 클래스를 부모로 상속해주면
    # 위에 정의한 필드도 자동으로 상속되서 정의됨
    class Meta:
        abstract = True


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='my_post_set',
                               on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='posting/post/%Y/%m/%d')
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           related_name='list_post_set',
                                           blank=True)

    @property
    def author_name(self):
        return f'{self.author.name} {self.author.name}'

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = list()
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse('posting:post_detail', args=[self.pk])

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ['-pk']


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-pk']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# class LikeUser(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
