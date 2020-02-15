import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)

    class Meta:
        unique_together = [['title', 'author']]

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_user_rating(self, user):
        return self.bookrating_set.get(user=user).rating

    def get_average_rating(self):
        return self.bookrating_set.aggregate(Avg('rating'))['rating__avg']

    def get_reader_count(self):
        return self.users.count()


class BookRating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['book', 'user']]

    def __str__(self):
        return f"{self.user.username} rated {self.book.title} a {self.rating} out of 5."
