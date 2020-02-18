from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.views import generic

from .. import constants
from ..models import Book


class DashboardView(generic.ListView):
    template_name = "books/dashboard.html"
    context_object_name = "dashboard_lists"
    model = Book

    def get_queryset(self):
        books = Book.objects.annotate(
            avg_rating=Coalesce(Avg("bookuser__rating"), 0),
            reader_count=Count("bookuser"),
        )

        return {
            "top_rated": books.order_by("-avg_rating")[:5],
            "most_read": books.order_by("-reader_count")[:5],
            "just_added": books.order_by("-created_at")[:5],
        }


class MyBooksView(LoginRequiredMixin, generic.ListView):
    login_url = constants.LOGIN_URL
    model = Book
    paginate_by = constants.SHOW_PER_PAGE
    template_name = "books/books_list.html"

    def get_queryset(self):
        user_books = Book.objects.filter(bookuser__user=self.request.user).order_by(
            "-created_at"
        )
        for book in user_books:
            details = book.get_user_detail(self.request.user)
            book.user_rating = details.rating
            book.external_id = details.external_id
        return user_books
