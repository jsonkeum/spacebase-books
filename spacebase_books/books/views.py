from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

from . import constants
from .forms import BookAddForm
from .models import Book, BookRating


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


class AddBookView(LoginRequiredMixin, FormView):
    login_url = "core:login"
    success_url = reverse_lazy("books:books")
    template_name = "books/book_add_form.html"
    form_class = BookAddForm

    def form_valid(self, form):
        data = form.cleaned_data
        book, created = Book.objects.get_or_create(title=data["title"], author=data["author"])
        if created:
            book.save()
        book.users.add(self.request.user)
        BookRating.objects.create(rating=data["rating"], book=book, user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())
