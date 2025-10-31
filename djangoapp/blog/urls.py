from blog.views import created_by, PostListView, CategoryListView, TagListView, SearchListView, PageDetailView, PostDetailView
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('created-by/<int:author_pk>/', created_by, name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'), 
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'), 
]

