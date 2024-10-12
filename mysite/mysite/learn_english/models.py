from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    word = models.CharField(max_length=50, null=True)
    translate = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.word} - {self.translate}'