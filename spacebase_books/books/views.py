from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

from . import constants
from .forms import BookForm
from .models import Book, BookUser


class DashboardView(generic.ListView):
    template_name = "books/dashboard.html"
    context_object_name = "dashboard_lists"
    model = Book
    queryset = {
        "top_rated": Book.objects.annotate(
            avg_rating=Coalesce(Avg("bookuser__rating"), 0)
        ).order_by("-avg_rating")[:5],
        "most_read": Book.objects.annotate(reader_count=Count("bookuser")).order_by(
            "-reader_count"
        )[:5],
        "just_added": Book.objects.order_by("-created_at")[:5],
    }


class MyBooksView(LoginRequiredMixin, generic.ListView):
    login_url = constants.LOGIN_URL
    model = Book
    template_name = "books/books_list.html"

    def get_queryset(self):
        user_books = Book.objects.filter(bookuser__user=self.request.user)
        for book in user_books:
            details = book.get_user_detail(self.request.user)
            book.user_rating = details.rating
            book.external_id = details.external_id
        return user_books


class AddBookView(LoginRequiredMixin, FormView):
    login_url = constants.LOGIN_URL
    success_url = reverse_lazy(constants.MAIN_PAGE)
    template_name = "books/book_form.html"
    form_class = BookForm

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            book, created = Book.objects.get_or_create(title=data["title"], author=data["author"])
            BookUser.objects.create(rating=data["rating"], book=book, user=self.request.user,
                                    external_id=data["external_id"])
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError as e:
            if created:
                book.delete()
            if 'external_id' in str(e):
                context = self.get_context_data(**self.kwargs)
                context['form'] = BookForm({
                    'title': data["title"],
                    'author': data["author"],
                    'rating': data["rating"],
                    'external_id': data["external_id"],
                })
                context['external_id_error'] = constants.EXTERNAL_ID_ERROR
            return self.render_to_response(context)


class EditBookView(LoginRequiredMixin, FormView):
    login_url = constants.LOGIN_URL
    success_url = reverse_lazy(constants.MAIN_PAGE)
    template_name = "books/book_form.html"
    form_class = BookForm

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=kwargs['book_id'])
        book_user = book.get_user_detail(request.user)
        context = self.get_context_data(**kwargs)
        context['form'] = BookForm({
            'title': book.title,
            'author': book.author,
            'rating': book_user.rating,
            'external_id': book_user.external_id,
        })

        return self.render_to_response(context)

    def form_valid(self, form):
        # STILL TO DO need to check whether user isn't just resending the data back with no change

        # get or create on book to see if the edited book is new or already exists
        data = form.cleaned_data
        book, created = Book.objects.get_or_create(title=data["title"], author=data["author"])

        old_book = Book.objects.get(pk=self.kwargs['book_id'])
        BookUser.objects.get(book=old_book, user=self.request.user).delete()
        BookUser.objects.create(book=book, user=self.request.user, rating=data["rating"],
                                external_id=data['external_id'])

        if old_book.bookuser_set.count() <= 1:
            old_book.delete()

        return HttpResponseRedirect(self.get_success_url())


def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.bookuser_set.count() <= 1:
        book.delete()
    else:
        BookUser.objects.get(book=book, user=request.user).delete()
    return HttpResponseRedirect(reverse_lazy(constants.MAIN_PAGE))
