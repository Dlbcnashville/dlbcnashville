from django.db import models
from taggit.managers import TaggableManager
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from django import forms
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from wagtail.users.models import UserProfile
from django.urls import reverse
from django.shortcuts import render
from django.utils.text import slugify
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from django.conf import settings
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
import re
from wagtail.search import index
from blog.utils.blog_utils import count_words, read_time
from wagtail.snippets.models import register_snippet
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from resources.models import ResourceIndexPage
# Create your models here.
AUTH_USER = settings.AUTH_USER_MODEL


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Blog Categories"
    

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class PostInfo(models.Model):
    post_title = models.CharField(
        max_length=500, null=True, blank=True, help_text='Enter the title of your post')
    short_highlight = models.CharField(
        max_length=1000, null=True, blank=True, help_text='Write a very short highlight of the post to captivate readers')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    post_image = CloudinaryField("image", null=True, blank=True)
    body = RichTextField(null=True, blank=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    

    class Meta:
        abstract = True
        ordering = ['-date_created']

class BlogIndexPage(Page):
    template = 'blog/blog_list.html'
    intro = RichTextField(blank=True)
    banner = CloudinaryField("image", null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner')
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPage.objects.live().public().order_by('-first_published_at')
        latest_post = BlogPage.objects.live().public().order_by('-first_published_at').first()
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 6)
        # Try to get the ?page=x value
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        
        context["latest_post"] = latest_post
        context["posts"] = posts
        return context
    


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
class BlogPage(PostInfo, Page):
    template = 'blog/blog_page.html'
    post_category = models.ForeignKey('BlogCategory', null=True, blank=True, on_delete=models.SET_NULL, related_name='post_category')
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    read_time = models.CharField(max_length=50, default=0)
    views = models.ManyToManyField(IpModel, related_name="blog_views", blank=True)
    likes = models.ManyToManyField(IpModel, related_name="blog_likes", blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('post_title'),
        index.SearchField('body'),
        index.FilterField('post_category'),
        index.FilterField('date_created'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('post_title'),
            FieldPanel('post_category'),
            FieldPanel('tags'),
            FieldPanel('post_image'),
            FieldPanel('allow_comments'),
            FieldPanel('short_highlight'),
        ], heading="Post information"),
        
        FieldPanel('body'),
    ]

    def __str__(self):
        return self.post_title
    
    def total_views(self):
        return self.views.count()

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return self.get_url()

    def save(self, *args, **kwargs):
        self.read_time = read_time(self.body)
        super(BlogPage, self).save(*args, **kwargs)
    
    # write a get_context method
    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        related_content = []
        if self.tags:
            for tag in self.tags.all():
                related_content += BlogPage.objects.live().filter(tags__name=tag)
        else:
            return related_content
        
        context["related_content"] = set(related_content)
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # adding like count
        like_status = False
        ip = get_client_ip(request)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            like_status = True
        else:
            like_status=False
        context['like_status'] = like_status


        return self.render_to_response(context)

class BlogTagIndexPage(Page):
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context



def blogLike(request, pk):
    postid = request.POST.get('blogid')
    post = get_object_or_404(BlogPage, pk=postid)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return redirect(post)
