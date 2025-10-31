from typing import Any
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView


PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()  # type: ignore


    #def get_queryset(self):
    #    return Post.objects.get_published()  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - ',
        })
        return context


def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()
    if user is None:
        raise Http404()


    posts = (Post.objects.get_published()#type: ignore
        .filter(created_by__pk=author_pk)) 
    user_full_name = user.username

    if user.first_name:
        user_full_name = f"{user.first_name} {user.last_name}"
    
    page_title = user_full_name + ' posts -'


    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return super().get_queryset().filter(category__slug=slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - ' #type: ignore
        ctx.update({'page_title': page_title})

        return ctx


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return super().get_queryset().filter(tags__slug=slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - ' #type: ignore
        ctx.update({'page_title': page_title})

        return ctx
    
class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'search_value': search_value,
            'page_title': f'{search_value[:30]} - Search - ',
        })
        return ctx
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)



def search(request):
    search_value = request.GET.get('search', '').strip()

    posts = (
        Post.objects.get_published() #type: ignore
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    )

    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - Página - ' #type: ignore
        ctx.update({'page_title': page_title})
        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

def page(request, slug):
    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
        ) 

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - Post - ' #type: ignore
        ctx.update({'page_title': page_title})
        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

def post(request, slug):
    post_obj = (
        Post.objects.get_published() #type: ignore
        .filter(slug=slug)
        .first()
        ) 
    
    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
