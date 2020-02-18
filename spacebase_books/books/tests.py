import time

from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from .models import Book, BookUser
from django.contrib.auth.models import User


class BookModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(title="The Road", author="Cormac MacCarthy")

        u1 = User.objects.create_user(
            username="abdullah", email="abdullah@gmail.com", password="123456"
        )
        u2 = User.objects.create_user(
            username="bob", email="bob@gmail.com", password="123456"
        )
        u3 = User.objects.create_user(
            username="carol", email="carol@gmail.com", password="123456"
        )
        u4 = User.objects.create_user(
            username="dinah", email="dinah@gmail.com", password="123456"
        )
        BookUser.objects.create(rating=3, book=cls.book, user=u1)
        BookUser.objects.create(rating=4, book=cls.book, user=u2)
        BookUser.objects.create(rating=5, book=cls.book, user=u3)
        BookUser.objects.create(rating=3, book=cls.book, user=u4)

    def test_prevents_case_sensitive_duplicates(self):
        book, created = Book.objects.get_or_create(
            title="The Road", author="Cormac MacCarthy"
        )
        self.assertEqual(book.title, "The Road")
        self.assertEqual(created, False)

    def test_get_user_rating(self):
        user = User.objects.get(username="abdullah")
        self.assertEqual(self.book.get_user_detail(user).rating, 3)

    def test_get_average_rating(self):
        self.assertEqual(self.book.get_average_rating(), 3.75)

    def test_get_reader_count(self):
        self.assertEqual(self.book.get_reader_count(), 4)


class MyBooksViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        b1 = Book.objects.create(title="The Road", author="Cormac MacCarthy")
        b2 = Book.objects.create(title="The Grapes of Wrath", author="John Steinbeck")
        b3 = Book.objects.create(title="1984", author="George Orwell")
        b4 = Book.objects.create(title="Ulysses", author="James Joyce")

        u1 = User.objects.create_user(
            username="abdullah", email="abdullah@gmail.com", password="123456"
        )
        u2 = User.objects.create_user(
            username="bob", email="bob@gmail.com", password="123456"
        )

        BookUser.objects.create(rating=3, book=b1, user=u1)
        BookUser.objects.create(rating=4, book=b2, user=u1)
        BookUser.objects.create(rating=5, book=b3, user=u1)
        BookUser.objects.create(rating=3, book=b3, user=u2)
        BookUser.objects.create(rating=3, book=b4, user=u2)

    def test_login_redirect(self):
        response = self.client.get(reverse("books:books"))
        self.assertEqual(response.status_code, 302)

    def test_user_list(self):
        self.client.login(username="abdullah", password="123456")
        response = self.client.get(reverse("books:books"))

        self.assertQuerysetEqual(
            response.context["book_list"],
            [
                "<Book: The Road - Cormac MacCarthy>",
                "<Book: The Grapes of Wrath - John Steinbeck>",
                "<Book: 1984 - George Orwell>",
            ],
            ordered=False,
        )
        self.client.logout()
        self.client.login(username="bob", password="123456")
        response = self.client.get(reverse("books:books"))

        self.assertQuerysetEqual(
            response.context["book_list"],
            ["<Book: Ulysses - James Joyce>", "<Book: 1984 - George Orwell>",],
            ordered=False,
        )


class DashboardViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        b1 = Book.objects.create(title="The Road", author="Cormac MacCarthy")
        b2 = Book.objects.create(title="The Grapes of Wrath", author="John Steinbeck")
        b3 = Book.objects.create(title="1984", author="George Orwell")
        b4 = Book.objects.create(title="Ulysses", author="James Joyce")
        b5 = Book.objects.create(title="Lolita", author="Vladimir Nabokov")
        b6 = Book.objects.create(title="The Catcher in the Rye", author="JD Salinger")
        b7 = Book.objects.create(title="To Kill a Mockingbird", author="Harper Lee")
        b8 = Book.objects.create(title="The Lord of the Rings", author="JRR Tolkien")
        b9 = Book.objects.create(title="Brave New World", author="Aldous Huxley")
        b10 = Book.objects.create(title="Invisible Man", author="Ralph Ellison")
        time.sleep(0.01)
        b11 = Book.objects.create(title="Jane Eyre", author="Charlotte Bronte")
        time.sleep(0.01)
        b12 = Book.objects.create(title="Pride and Prejudice", author="Jane Austen")
        time.sleep(0.01)
        b13 = Book.objects.create(title="Lord of the Flies", author="William Golding")
        time.sleep(0.01)
        b14 = Book.objects.create(title="Heart of Darkness", author="Joseph Conrad")
        time.sleep(0.01)
        b15 = Book.objects.create(title="War and Peace", author="Leo Tolstoy")

        users = [
            User.objects.create_user(
                username="abdullah", email="abdullah@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="bob", email="bob@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="carol", email="carol@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="dinah", email="dinah@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="earl", email="earl@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="frank", email="frank@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="greta", email="greta@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="helen", email="helen@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="irene", email="irene@gmail.com", password="123456"
            ),
            User.objects.create_user(
                username="jason", email="jason@gmail.com", password="123456"
            ),
        ]

        BookUser.objects.create(rating=4, book=b1, user=users[0])
        # 4

        BookUser.objects.create(rating=3, book=b2, user=users[0])
        BookUser.objects.create(rating=2, book=b2, user=users[1])
        BookUser.objects.create(rating=3, book=b2, user=users[2])
        # 2.67

        BookUser.objects.create(rating=3, book=b3, user=users[0])
        BookUser.objects.create(rating=1, book=b3, user=users[1])
        BookUser.objects.create(rating=4, book=b3, user=users[2])
        BookUser.objects.create(rating=3, book=b3, user=users[3])
        # 2.75

        BookUser.objects.create(rating=3, book=b7, user=users[0])
        BookUser.objects.create(rating=2, book=b7, user=users[1])
        BookUser.objects.create(rating=5, book=b7, user=users[2])
        BookUser.objects.create(rating=3, book=b7, user=users[3])
        BookUser.objects.create(rating=5, book=b7, user=users[4])
        # 3.6

        BookUser.objects.create(rating=5, book=b14, user=users[3])
        BookUser.objects.create(rating=4, book=b14, user=users[4])
        # 4.5

        BookUser.objects.create(rating=3, book=b10, user=users[0])
        BookUser.objects.create(rating=3, book=b10, user=users[1])
        BookUser.objects.create(rating=3, book=b10, user=users[2])
        BookUser.objects.create(rating=3, book=b10, user=users[3])
        BookUser.objects.create(rating=3, book=b10, user=users[4])
        BookUser.objects.create(rating=3, book=b10, user=users[5])
        # 3.0

    def test_most_read_list(self):
        response = self.client.get(reverse("books:dashboard"))

        self.assertQuerysetEqual(
            response.context["dashboard_lists"]["most_read"],
            [
                "<Book: Invisible Man - Ralph Ellison>",
                "<Book: To Kill a Mockingbird - Harper Lee>",
                "<Book: 1984 - George Orwell>",
                "<Book: The Grapes of Wrath - John Steinbeck>",
                "<Book: Heart of Darkness - Joseph Conrad>",
            ],
            ordered=True,
        )

    def test_top_rated_list(self):
        response = self.client.get(reverse("books:dashboard"))

        self.assertQuerysetEqual(
            response.context["dashboard_lists"]["top_rated"],
            [
                "<Book: Heart of Darkness - Joseph Conrad>",
                "<Book: The Road - Cormac MacCarthy>",
                "<Book: To Kill a Mockingbird - Harper Lee>",
                "<Book: Invisible Man - Ralph Ellison>",
                "<Book: 1984 - George Orwell>",
            ],
            ordered=True,
        )

    def test_just_added_list(self):
        response = self.client.get(reverse("books:dashboard"))

        self.assertQuerysetEqual(
            response.context["dashboard_lists"]["just_added"],
            [
                "<Book: War and Peace - Leo Tolstoy>",
                "<Book: Heart of Darkness - Joseph Conrad>",
                "<Book: Lord of the Flies - William Golding>",
                "<Book: Pride and Prejudice - Jane Austen>",
                "<Book: Jane Eyre - Charlotte Bronte>",
            ],
            ordered=True,
        )
