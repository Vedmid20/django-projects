from django.contrib import admin
from .models import BlogPost, CommentForBlogPost


class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


lst = [BlogPost, CommentForBlogPost]
admin.site.register(lst)
