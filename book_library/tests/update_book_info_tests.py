import pytest


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, expected_status", [
    ("admin", 200),
    ("regular", 200),
    ("anonymous", 401),
])
def test_update_book_info(user_type, expected_status, admin_user, regular_user, authenticate, api_client, api_urls,
                          book_id):
    client = api_client
    if user_type == "admin":
        client = authenticate(admin_user)
    elif user_type == "regular":
        client = authenticate(regular_user)

    new_title = "To be or not to be"

    response = client.patch(api_urls.book_detail(book_id),
                            {"title": new_title}, format="json")

    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.data["title"] == new_title
