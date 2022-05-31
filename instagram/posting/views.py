from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posting.forms import PostForm
from .models import Post


@login_required
def index(request):
    return render(
        request, 'posting/index.html', {
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


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(
        request, 'posting/post_detail.html', {
            'post': post,
        }
    )


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_count = post_list.count()
    return render(
        request, 'posting/user_page.html', {
            'page_user': page_user,
            'post_list': post_list,
            'post_count': post_count,
        }
    )
