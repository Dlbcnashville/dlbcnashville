from django.contrib import admin

# # Register your models here.
# Register your models here.
from .models import BlogPage
@admin.register(BlogPage)
class BlogAdmin(admin.ModelAdmin):
    fields = ('post_title','date_created', 'date_updated', 'post_image', 'body', 'allow_comments', 'post_category', 'tags', 'read_time', 'views', 'likes')
    list_display = ('post_title','date_created', 'date_updated', 'post_image', 'body', 'allow_comments', 'read_time')
    list_filter = ('post_title', 'date_created',)
    search_fields = ('post_title', 'date_created',)
