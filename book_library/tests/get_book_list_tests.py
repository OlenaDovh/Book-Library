import pytest


@pytest.mark.django_db
def test_pagination(regular_user, authenticate, api_urls):
    client = authenticate(regular_user)

    for i in range(11):
        client.post(api_urls.book_list, {
            "title": f"Book {i}",
            "author": "Author",
            "genre": "Genre",
            "publication_year": 2020
        })

    response = client.get(api_urls.book_list, format="json")
    assert response.status_code == 200
    assert len(response.data["results"]) == 10

    next_page_url = response.data.get("next")
    assert next_page_url is not None

    response_page_2 = client.get(next_page_url, format="json")

    assert response_page_2.status_code == 200
    assert len(response_page_2.data["results"]) == 1
    assert response_page_2.data["next"] is None