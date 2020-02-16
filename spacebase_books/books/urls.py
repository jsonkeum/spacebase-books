from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("mybooks", views.MyBooksView.as_view(), name="books"),
    path("mybooks/add", views.AddBookView.as_view(), name="add_book"),
    path("mybooks/edit/<int:book_id>", views.EditBookView.as_view(), name="edit_book"),
    path("mybooks/delete/<int:book_id>", views.delete_book, name="delete_book"),
]
