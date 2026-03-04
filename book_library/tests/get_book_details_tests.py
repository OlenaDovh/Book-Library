import pytest


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, expected_status", [
    ("admin", 200),
    ("regular", 200),
    ("anonymous", 403),
])
def get_book_details(user_type, expected_status, admin_user, regular_user, authenticate, api_urls, api_client, book_id):
    client = api_client
    if user_type == "admin":
        client = authenticate(admin_user)
    elif user_type == "regular":
        client = authenticate(regular_user)

    response = client.get(api_urls.book_detail(book_id))

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.data["id"] == book_id
        assert "title" in response.data
        assert "author" in response.data
        assert "genre" in response.data
        assert "publication_year" in response.data
