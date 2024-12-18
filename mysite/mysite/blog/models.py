import datetime
from django.utils import timezone

from django.db import models
from django.conf import settings
from django.core.validators import *
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _


class PublishedBlogPostManager(models.Manager):
   def get_queryset(self):
      return super().get_queryset().filter(status=BlogPost.Status.PUBLISHED)
   

class BlogPost(models.Model):
   class Status(models.TextChoices):
      DRAFT = 'D', _('Draft')
      PUBLISHED = 'P', _('Published')

   title = models.CharField(max_length=200, validators=[MinLengthValidator(10)], verbose_name=_('Title'))
   text = models.TextField(validators=[MinLengthValidator(10)], verbose_name=_('Text'))
   owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Owner'))
   created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
   updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
   slug = models.SlugField(max_length=200, null=False, unique=True, blank=True, verbose_name=_('Slug'))
   tags = TaggableManager(verbose_name=_('Tags'))
   published_at = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Published At'))
   status = models.CharField(max_length=1, choices=Status, default=Status.DRAFT, verbose_name=_('Status'))

   objects = models.Manager()
   published_objects = PublishedBlogPostManager()

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.title)
         original_slug = self.slug
         queryset = BlogPost.objects.filter(slug=self.slug)
         counter = 1
         while queryset.exists():
            self.slug = f"{original_slug}-{counter}"
            queryset = BlogPost.objects.filter(slug=self.slug)
            counter += 1
      if self.pk:
         previos = BlogPost.objects.get(pk=self.pk)
         if previos.status == BlogPost.Status.DRAFT and self.status == BlogPost.Status.PUBLISHED:
            self.published_at = timezone.now()

      super().save(*args, **kwargs)

   def __str__(self):
      return f'{self.owner} - {self.title}'


class CommentForBlogPost(models.Model):
   owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments_owned')
   post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
   text = models.CharField(max_length=300)
   created_at = models.DateTimeField(auto_now_add=True)
   slug = models.SlugField(max_length=200, null=False, unique=True, blank=True, verbose_name=_('Slug'))

   def save(self, *args, **kwargs):
      if not self.slug or self.text != getattr(self, '_original_text', None):
         self.slug = slugify(self.text[:10])
         original_slug = self.slug
         queryset = CommentForBlogPost.objects.filter(slug=self.slug)
         counter = 1
         while queryset.exists():
            self.slug = f"{original_slug}-{counter}"
            queryset = CommentForBlogPost.objects.filter(slug=self.slug)
            counter += 1
      if self.pk:
         try:
            previos = BlogPost.objects.get(pk=self.pk)
            if previos.status == BlogPost.Status.DRAFT and self.status == BlogPost.Status.PUBLISHED:
               self.published_at = timezone.now()
         except BlogPost.DoesNotExist:
            previos = None

      super().save(*args, **kwargs)

   def __str__(self):
      return f'Owner: {self.owner} - {self.text}'
