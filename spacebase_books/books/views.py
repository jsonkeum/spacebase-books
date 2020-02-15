from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.views import generic

from .models import Book


class DashboardView(generic.ListView):
    template_name = "books/dashboard.html"
    context_object_name = "dashboard_lists"
    model = Book
    queryset = {
        "top_rated": Book.objects.annotate(
            avg_rating=Coalesce(Avg("bookrating__rating"), 0)
        ).order_by("-avg_rating")[:5],
        "most_read": Book.objects.annotate(reader_count=Count("users")).order_by(
            "-reader_count"
        )[:5],
        "just_added": Book.objects.order_by("-created_at")[:5],
    }


class MyBooksView(LoginRequiredMixin, generic.ListView):
    login_url = "core:login"
    model = Book
    template_name = "books/books_list.html"

    def get_queryset(self):
        user_books = self.request.user.book_set.all()
        for book in user_books:
            book.user_rating = book.get_user_rating(self.request.user)
        return user_books
