from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url


class User(AbstractUser):
    # TextChoices : 장고 3에서 추가된거
    class GenderChoices(models.TextChoices):
        # 'DB에 저장되는 값', '보여지는 값'
        MALE = 'M', '남성'
        FEMALE = 'F', '여성'

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True,
                                    validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)
    profile = models.ImageField(blank=True, upload_to='accounts/profile/%Y/%m/%d',
                                help_text='48px X 48px 크기의 png/jpg 파일을 업로드해주세요')

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def profile_url(self):
        if self.profile:
            return self.profile.url
        else:
            return resolve_url('pydenticon_image', self.username)