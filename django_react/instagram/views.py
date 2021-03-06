from django.contrib import messages
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, \
    DayArchiveView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


# post_list = login_required(ListView.as_view(model = Post, paginate_by = 10))

@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')

        if q:
            qs = qs.filter(message__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.model.objects.all()
        q = self.request.GET.get('q', '')

        if q:
            qs = qs.filter(message__icontains=q)
        context.update({
            # 'post_list':qs,
            'q': q,
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


# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.success(request, '포스트를 저장했습니다')
#             return redirect(post)
#     else:
#         form = PostForm()
#
#     return render(
#         request,
#         'instagram/post_form.html',
#         {
#             'form': form,
#             'post': None,
#         }
#     )

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, '포스트를 저장했습니다')
        return super().form_valid(form)


post_new = PostCreateView.as_view()


# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 작성자 체크
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정할 수 있음')
#         return redirect(post)
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.success(request, '포스트를 수정했습니다')
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
#
#     return render(
#         request,
#         'instagram/post_form.html',
#         {
#             'form': form,
#             'post': post,
#         }
#     )

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, '포스트를 수정했습니다')
        return super().form_valid(form)

post_edit = PostUpdateView.as_view()

# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스트를 삭제했습니다')
#         # 삭제하고나면 pk가 없어져서 리다이렉트 안 해주면 오류 발생하기 때문에 리다이렉트해줘야 함
#         return redirect('instagram:post_list')
#     return render(
#         request, 'instagram/post_confirm_delete.html', {
#             'post': post,
#         }
#     )

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse('instagram:post_list')

post_delete = PostDeleteView.as_view()