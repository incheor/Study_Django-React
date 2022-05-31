from .models import User
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
)


# 패스워드 암호화를 위해 UserCreationForm 사용
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필수 입력 사항 지정
        self.fields['email'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    # 입력받을 필드 정의
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # 유효성 검사
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('이미 등록된 이메일 주소입니다')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile', 'first_name', 'last_name', 'website_url', 'bio', 'phone_number', 'gender']


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError('새로운 암호와 기존 암호가 같아요')
        return new_password2
