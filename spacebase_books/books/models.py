import datetime

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} - {self.author}"
