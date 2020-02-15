from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic.base import ContextMixin

from .models import Book


class DashboardView(ContextMixin, generic.View):
    template_name = "books/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top-rated"] = []
        context["most-read"] = []
        return context

    def get(self, request):
        return render(request, self.template_name)


class BooksView(LoginRequiredMixin, generic.ListView):
    login_url = "core:login"

    model = Book
    template_name = "books/books_list.html"
    queryset = Book.objects.order_by("-title")
