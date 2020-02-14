from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("books.urls")),
    path("accounts/", include("core.urls")),
    path("admin/", admin.site.urls),
]
