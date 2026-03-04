import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from book_library.models import Book

User = get_user_model()


@pytest.fixture
def api_urls():
    class URLs:
        token_obtain = reverse('token_obtain_pair')
        token_refresh = reverse('token_refresh')
        book_list = reverse('book-list')

        def book_detail(self, pk):
            return reverse('book-detail', kwargs={'pk': pk})

    return URLs()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    password = "admin123"
    user = User.objects.create_user(
        username="admin",
        password=password,
        is_staff=True
    )
    user.raw_password = password
    return user


@pytest.fixture
def regular_user():
    password = "user123"
    user = User.objects.create_user(
        username="user",
        password=password,
        is_staff=False
    )
    user.raw_password = password
    return user


@pytest.fixture
def authenticate(api_urls):
    def _authenticate(user):
        client = APIClient()
        response = client.post(api_urls.token_obtain, {
            "username": user.username,
            "password": user.raw_password
        }, format="json")
        assert response.status_code == 200, f"Помилка аутентифікації: {response.data}"
        token = response.data["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client

    return _authenticate


@pytest.fixture
def book_id(admin_user):
    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        genre="Fiction",
        publication_year=2024,
        user=admin_user
    )
    return book.id
