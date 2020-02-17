from django.contrib import admin

# Register your models here.
from .models import Book, BookUser

admin.site.register(Book)
admin.site.register(BookUser)
