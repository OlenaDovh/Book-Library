import pytest

@pytest.mark.django_db
@pytest.mark.parametrize("user_type, expected_status", [
    ("admin", 201),
    ("regular", 201),
    ("anonymous", 401),
])
def test_create_book(user_type, expected_status, admin_user, regular_user, authenticate, api_client, api_urls):
    if user_type == "admin":
        client = authenticate(admin_user)
    elif user_type == "regular":
        client = authenticate(regular_user)
    else:
        client = api_client

    payload = {
        "title": f"Book by {user_type}",
        "author": "Author",
        "genre": "Genre",
        "publication_year": 2024
    }

    response = client.post(api_urls.book_list, payload, format="json")

    assert response.status_code == expected_status