from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as authPasswordChangeView
)
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import SignupForm, ProfileForm, PasswordChangeForm
from django.contrib.auth import login as auth_login

login = LoginView.as_view(template_name='accounts/login_form.html', next_page='/')


def logout(request):
    messages.success(request, '로그아웃되었습니다')
    return logout_then_login(request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            # 첫번째 인자 : request, 두번째 인자 : 유저
            auth_login(request, signed_user)
            messages.success(request, '회원가입 완료 환영합니다')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(
        request, 'accounts/signup_form.html', {
            'form': form,
        }
    )


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 수정했어요')
            return redirect('accounts:profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(
        request, 'accounts/profile_edit.html', {
            'form': form,
        }
    )


class PasswordChangeView(LoginRequiredMixin, authPasswordChangeView):
    success_url = reverse_lazy('accounts:password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, '암호를 변경했어요')
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()
