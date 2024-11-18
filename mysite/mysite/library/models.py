from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Author(models.Model):
    first_name = models.CharField(null=True, max_length=30)
    last_name = models.CharField(null=True, max_length=50)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Book(models.Model):
    title = models.CharField(null=True, max_length=100)
    realise = models.IntegerField(null=True, validators=[MinValueValidator(1800), MaxValueValidator(datetime.datetime.now().year)])
    make_name = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.realise}'