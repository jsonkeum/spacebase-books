from django.forms import RadioSelect
from django.urls import path

from .views import main, book

app_name = "books"
urlpatterns = [
    path("", main.DashboardView.as_view(), name="dashboard"),
    path("mybooks", main.MyBooksView.as_view(), name="books"),
    path("mybooks/export", book.export_to_csv, name="csv"),
    path("mybooks/add", book.BookFormView.as_view(), name="add_book"),
    path("mybooks/edit/<int:book_id>", book.EditBookView.as_view(), name="edit_book"),
    path("mybooks/delete/<int:book_id>", book.delete_book, name="delete_book"),
]
