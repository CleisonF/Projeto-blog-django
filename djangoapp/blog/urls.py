from blog.views import  page, post, created_by, search, PostListView, CategoryListView, TagListView
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('created-by/<int:author_pk>/', created_by, name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'), 
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', search, name='search'), 
]

