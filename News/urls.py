from django.urls import path
from django.views.generic.base import TemplateView

from .views import *

app_name = "news"

urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('post/<str:slug>/',GetPost.as_view(), name='post'),
    path('post/like/<int:pk>/', like_post, name='like_post'),
    path('category/<str:slug>/',PostsByCategory.as_view(), name='category'),
    path('nation/<str:slug>/',PostsByNation.as_view(), name='nation'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('author/<int:pk>/', PostsByAuthor.as_view(), name='author'),
    path('search/',Search.as_view(), name='search'),
    path('post/<slug:post_slug>/add_comment/', add_comment, name='add_comment'),
    path('create_post', AddPostView.as_view(), name='create_post'),
]
