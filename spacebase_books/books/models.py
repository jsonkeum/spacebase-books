import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

from . import constants


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["title", "author"]]

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_user_detail(self, user):
        return self.bookuser_set.get(user=user)

    def get_average_rating(self):
        return self.bookuser_set.aggregate(Avg("rating"))["rating__avg"]

    def get_reader_count(self):
        return self.bookuser_set.count()


class BookUser(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(constants.MIN_RATING),
            MaxValueValidator(constants.MAX_RATING),
        ]
    )
    external_id = models.CharField(max_length=200, default=None, blank=True, null=True)

    class Meta:
        unique_together = [["book", "user"], ["user", "external_id"]]

    def __str__(self):
        return f"{self.user.username} rated {self.book.title} a {self.rating} out of 5."
