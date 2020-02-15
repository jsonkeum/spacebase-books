from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("mybooks", views.BooksView.as_view(), name="books"),
]
