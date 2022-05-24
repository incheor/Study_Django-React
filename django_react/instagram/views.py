from django.contrib import messages
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, \
    DayArchiveView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostForm


# post_list = login_required(ListView.as_view(model = Post, paginate_by = 10))

@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    paginate_by = 10

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     q = self.request.GET.get('q', '')
    #
    #     if q:
    #         qs = qs.filter(message__icontains=q)
    #     return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.model.objects.all()
        q = self.request.GET.get('q', '')

        if q:
            qs = qs.filter(message__icontains=q)
        # context = {
        #     'post_list': qs,
        #     'q': q,
        # }
        context.update({
            'post_list':qs,
            'q':q
        })
        return context

post_list = PostListView.as_view()


# @login_required
# def post_list(request) :
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q :
#         qs = qs.filter(message__icontains = q)
#     messages.error(request, 'messages 테스트 중')
#     return render(
#         request,
#         'instagram/post_list.html',
#         {
#             'post_list' : qs,
#             'q' : q
#         }
#     )

def post_detail(request: HttpRequest, pk: int):
    post = get_object_or_404(Post, pk=pk)
    return render(
        request,
        'instagram/post_detail.html',
        {
            'post': post
        }
    )


# class PostDetailView(DetailView) :
#     model = Post
#     def get_queryset(self) :
#         qs = super().get_queryset()
#         if not self.request.user.is_authenticated :
#             qs = qs.filter(is_public = True)				
#         return qs

# post_detail = PostDetailView.as_view()

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '포스트를 저장했습니다')
            return redirect(post)
    else:
        form = PostForm()

    return render(
        request,
        'instagram/post_form.html',
        {
            'form': form,
            'post': None,
        }
    )


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 작성자 체크
    if post.author != request.user:
        messages.error(request, '작성자만 수정할 수 있음')
        return redirect(post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '포스트를 수정했습니다')
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'instagram/post_form.html',
        {
            'form': form,
            'post': post,
        }
    )
