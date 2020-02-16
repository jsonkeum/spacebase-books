from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

from .forms import BookForm
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
            book.user_rating = book.get_user_rating(self.request.user).rating
        return user_books


class AddBookView(LoginRequiredMixin, FormView):
    login_url = "core:login"
    success_url = reverse_lazy("books:books")
    template_name = "books/book_form.html"
    form_class = BookForm

    def form_valid(self, form):
        data = form.cleaned_data
        book, created = Book.objects.get_or_create(title=data["title"], author=data["author"])
        if created:
            book.save()
        book.users.add(self.request.user)
        BookRating.objects.create(rating=data["rating"], book=book, user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class EditBookView(LoginRequiredMixin, FormView):
    login_url = "core:login"
    success_url = reverse_lazy("books:books")
    template_name = "books/book_form.html"
    form_class = BookForm

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=kwargs['book_id'])
        rating = book.get_user_rating(request.user).rating
        context = self.get_context_data(**kwargs)
        context['form'] = BookForm({
            'title': book.title,
            'author': book.author,
            'rating': rating,
        })

        return self.render_to_response(context)

    def form_valid(self, form):
        # STILL TO DO need to check whether user isn't just resending the data back with no change

        # get or create on book to see if the edited book is new or already exists
        data = form.cleaned_data
        book, created = Book.objects.get_or_create(title=data["title"], author=data["author"])

        # save new book, add user.
        if created:
            book.save()
        book.users.add(self.request.user)

        # Remove user to old book relation
        print(self.kwargs)
        old_book = Book.objects.get(pk=self.kwargs['book_id'])

        print(old_book.users.count())
        # If user is the only reader, just delete and cascade. Else remove user relation and delete rating
        if old_book.users.count() <= 1:
            old_book.delete()
        else:
            old_book.users.remove(self.request.user)
            BookRating.objects.get(book=old_book, user=self.request.user).delete()

        # Save new rating
        BookRating.objects.create(rating=data["rating"], book=book, user=self.request.user)

        return HttpResponseRedirect(self.get_success_url())


def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.users.count() <= 1:
        book.delete()
    else:
        book.users.remove(request.user)
        BookRating.objects.get(book=book, user=request.user).delete()
    return HttpResponseRedirect(reverse_lazy('books:books'))
