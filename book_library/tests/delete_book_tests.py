import pytest


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, expected_status", [
    ("admin", 200),
    ("regular", 403),
    ("anonymous", 401),
])
def test_delete_book(user_type, expected_status, admin_user, regular_user, authenticate, api_client, api_urls, book_id):
    # admin_client = authenticate(admin_user)
    # book_res = admin_client.post(api_urls.book_list,
    #                              {"title": "To be deleted",
    #                               "author": "A",
    #                               "genre": "G",
    #                               "publication_year": 2000})

    client = api_client
    if user_type == "admin":
        client = authenticate(admin_user)
    elif user_type == "regular":
        client = authenticate(regular_user)

    response = client.delete(api_urls.book_detail(book_id))

    assert response.status_code == expected_status