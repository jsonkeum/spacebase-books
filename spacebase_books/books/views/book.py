import csv
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from django.urls import reverse_lazy
from django.views.generic import FormView

from .. import constants
from ..forms import BookForm
from ..models import Book, BookUser


class BookFormView(LoginRequiredMixin, FormView):
    login_url = constants.LOGIN_URL
    success_url = reverse_lazy(constants.MAIN_PAGE)
    template_name = "books/book_form.html"
    form_class = BookForm

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            if "book_id" in self.kwargs:
                book, book_created = Book.objects.update_or_create(
                    pk=self.kwargs["book_id"],
                    defaults={"title": data["title"], "author": data["author"]},
                )
            else:
                book, book_created = Book.objects.get_or_create(
                    title=data["title"], author=data["author"]
                )
            BookUser.objects.update_or_create(
                user=self.request.user,
                book=book,
                defaults={
                    "rating": data["rating"],
                    "external_id": data["external_id"] or None,
                },
            )
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError as e:
            if book_created:
                book.delete()
            context = self.get_context_data(**self.kwargs)
            context["form"] = BookForm(
                {
                    "title": data["title"],
                    "author": data["author"],
                    "rating": data["rating"],
                    "external_id": data["external_id"],
                }
            )
            context["error"] = (
                constants.EXTERNAL_ID_ERROR if "external_id" in str(e) else str(e)
            )
            return self.render_to_response(context)


class EditBookView(BookFormView):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs["book_id"])
        book_user = get_object_or_404(
            BookUser, user=request.user, book_id=kwargs["book_id"]
        )
        context = self.get_context_data(**kwargs)
        context["form"] = BookForm(
            {
                "title": book.title,
                "author": book.author,
                "rating": book_user.rating,
                "external_id": book_user.external_id,
            }
        )

        return self.render_to_response(context)


def delete_book(request, book_id):
    get_object_or_404(BookUser, book_id=book_id, user=request.user).delete()
    return HttpResponseRedirect(reverse_lazy(constants.MAIN_PAGE))


def export_to_csv(request):
    user_books = get_list_or_404(Book, bookuser__user=request.user)

    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="books-{request.user.username}-{datetime.datetime.now()}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Book ID", "External ID", "Title", "Author", "Rating"])
    for book in user_books:
        details = book.get_user_detail(request.user)
        writer.writerow(
            [book.id, details.external_id, book.title, book.author, details.rating]
        )

    return response
