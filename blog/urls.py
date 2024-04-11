from django.urls import path
from blog.views import BlogListView, SearchResultsList
from blog.models import blogLike
app_name = "blog"

urlpatterns = [
    path('blogs/list/', BlogListView.as_view(), name='blog_list'),
    path('blog/like/<int:pk>', blogLike, name='blog_like'),

    path(
        route='search_results',
        view=SearchResultsList.as_view(),
        name='search_results'
    ),
    # path("<slug:slug>/", AuthorDetailView.as_view(), name="author_detail"),
]