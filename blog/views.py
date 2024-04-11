from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
# import listview from django

from django.views.generic.detail import DetailView
# Create your views here.

from blog.models import BlogPage, HowPage, WeeklyWordPage, Video


class BlogListView(TemplateView):
    template_name = "blog/blog_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = BlogPage.objects.all()
        return context
    



from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
class SearchResultsList(ListView):
    model = BlogPage
    context_object_name = "blogs"
    template_name = "blog/search.html"

    def get_queryset(self):
        query = self.request.GET.get("search")
        search_vector = SearchVector("post_title", "body")
        search_query = SearchQuery(query)

        search_headline = SearchHeadline("post_title", search_query)
        return BlogPage.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).annotate(headline=search_headline).filter(search=search_query).order_by("-rank")