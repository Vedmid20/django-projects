# Generated by Django 5.1.3 on 2024-11-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_published_at_blogpost_slug_blogpost_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentforblogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug'),
        ),
    ]
