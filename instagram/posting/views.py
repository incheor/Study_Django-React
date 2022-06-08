import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from posting.forms import PostForm, CommentForm
from .models import Post


@login_required
def index(request):
    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all() \
        .filter(  # Q 활용해서
        Q(author=request.user) |  # 작성자가 자기자신이거나
        Q(author__in=request.user.following_set.all())  # 팔로잉한 유저만 필터링
    ).filter(created_at__gte=timesince)
    suggested_user_list = get_user_model().objects.all() \
        .exclude(pk=request.user.pk) \
        .exclude(pk__in=request.user.following_set.all())
    comment_form = CommentForm()
    return render(
        request, 'posting/index.html', {
            'post_list': post_list,
            'suggested_user_list': suggested_user_list,
            'comment_form': comment_form,
        }
    )


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, '포스팅을 저장했어요')
            return redirect(post)
    else:
        form = PostForm()

    return render(
        request, 'posting/post_form.html', {
            'form': form
        }
    )


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(
        request, 'posting/post_detail.html', {
            'post': post,
            'comment_form': comment_form,
        }
    )


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, '좋아요를 전달했어요')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, '좋아요를 취소했어요')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_count = post_list.count()
    # 로그인 여부 확인해서 로그인이 되어 있다면 
    if request.user.is_authenticated:
        # 해당 유저의 following_set에서 해당 유저(page_user)를 팔로우하고 있는지 확인
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
        if request.user.pk == page_user.pk:
            is_follow = 'Me'
    else:
        is_follow = False

    return render(
        request, 'posting/user_page.html', {
            'page_user': page_user,
            'post_list': post_list,
            'post_count': post_count,
            'is_follow': is_follow,
        }
    )


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글을 보냈어요')
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return render(
                    request, 'posting/_comment.html', {
                        'comment': comment,
                    })
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(
        request, 'posting/comment_form.html', {
            'form': form,
        }
    )
