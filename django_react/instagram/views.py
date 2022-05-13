from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView

post_list = ListView.as_view(model = Post, paginate_by = 10)
# def post_list(request) :
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q :
#         qs = qs.filter(message__icontains = q)
        
#     return render(
#         request,
#         'instagram/post_list.html',
#         {
#             'post_list' : qs,
#             'q' : q
#         }
#     )

# def post_detail(request : HttpRequest, pk : int) -> HttpResponse :
#     post = get_object_or_404(Post, pk = pk)
#     return render(
#         request,
#         'instagram/post_detail.html',
#         {
#             'post' : post
#         }
#     )

class PostDetailView(DetailView) :
    model = Post
    def get_queryset(self) :
        qs = super().get_queryset()
        if not self.request.user.is_authenticated :
                qs = qs.filter(is_public = True)				
        return qs
    
post_detail = PostDetailView.as_view()