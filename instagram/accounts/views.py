from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as authPasswordChangeView
)
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import SignupForm, ProfileForm, PasswordChangeForm
from django.contrib.auth import login as auth_login

from .models import User

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


# follow, unfollow는 로그인을 해야함
@login_required
# urls에서 username을 넘겼으니 views 단에서 받아줘야 함
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)
    # 현재 유저(request.user)가 다른 유저(follow_user)를 팔로우함
    request.user.following_set.add(follow_user)
    # 거꾸로 다른 유저 입장에서는 팔로우를 당함
    follow_user.follower_set.add(request.user)
    messages.success(request, f'{follow_user}님을 팔로우했어요')
    redirect_url = request.META.get('HTTP_REFERER', 'ROOT')
    return redirect(redirect_url)


@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)
    # 현재 유저(request.user)가 다른 유저(follow_user)를 언팔로우함(팔로우 제거, remove)
    request.user.following_set.remove(unfollow_user)
    # 거꾸로 다른 유저 입장에서는 언팔로우를 당함(팔로우 제거, remove)
    unfollow_user.follower_set.remove(request.user)
    messages.success(request, f'{unfollow_user}님을 언팔로우했어요')
    redirect_url = request.META.get('HTTP_REFERER', 'ROOT')
    return redirect(redirect_url)