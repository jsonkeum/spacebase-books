from django.test import TestCase

# Create your tests here.
from .models import Book, BookRating
from django.contrib.auth.models import User


class BookModelTests(TestCase):
    def setUp(self):
        Book.objects.create(title="The Road", author="Cormac MacCarthy")
        # Book.objects.create(title="The Grapes of Wrath", author="John Steinbeck")
        # Book.objects.create(title="1984", author="George Orwell")
        # Book.objects.create(title="Ulysses", author="James Joyce")
        # Book.objects.create(title="Lolita", author="Vladimir Nabokov")
        # Book.objects.create(title="The Catcher in the Rye", author="JD Salinger")
        # Book.objects.create(title="To Kill a Mockingbird", author="Harper Lee")
        # Book.objects.create(title="The Lord of the Rings", author="JRR Tolkien")
        # Book.objects.create(title="Brave New World", author="Aldous Huxley")
        # Book.objects.create(title="The Unbearable Lightness of Being", author="Milan Kundera")

        User.objects.create_user(username="abdullah", email="abdullah@gmail.com", password="123456")
        User.objects.create_user(username="bob", email="bob@gmail.com", password="123456")
        User.objects.create_user(username="carol", email="carol@gmail.com", password="123456")
        User.objects.create_user(username="dinah", email="dinah@gmail.com", password="123456")

    def test_prevents_case_sensitive_duplicates(self):
        book, created = Book.objects.get_or_create(
            title="The Road",
            author="Cormac MacCarthy"
        )
        self.assertEqual(book.title, "The Road")
        self.assertEqual(created, False)

    def test_get_user_rating(self):
        book = Book.objects.first()
        user = User.objects.first()
        rating = BookRating.objects.create(rating=3, book=book, user=user)

        self.assertEqual(book.get_user_rating(user), rating)

    def test_get_average_rating(self):
        book = Book.objects.first()
        users = User.objects.all()
        BookRating.objects.create(rating=3, book=book, user=users[0])
        BookRating.objects.create(rating=4, book=book, user=users[1])
        BookRating.objects.create(rating=5, book=book, user=users[2])
        BookRating.objects.create(rating=3, book=book, user=users[3])

        self.assertEqual(book.get_average_rating(), 3.75)

    def test_get_reader_count(self):
        book = Book.objects.first()
        users = User.objects.all()
        book.users.add(users[0])
        book.users.add(users[1], users[2])
        book.save()

        self.assertEqual(book.get_reader_count(), 3)
