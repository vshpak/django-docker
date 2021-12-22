import json
import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_publishers__positive(client):
    response = client.get("/store/publishers/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_publisher__positive(client, publisher):
    response = client.get(f"/store/publishers/{publisher.pk}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_publisher__positive(client):
    publisher_name = "Родина"
    publisher_address = "Владивосток"
    data = json.dumps({"name": publisher_name, "address": publisher_address})
    response = client.post("/store/publishers/", data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == publisher_name


@pytest.mark.django_db
def test_put_publisher__positive(client, publisher):
    publisher_name = "Новая книга"
    publisher_address = "Москва"
    data = json.dumps(
        {"id": publisher.pk, "name": publisher_name, "address": publisher_address}
    )
    response = client.put(
        f"/store/publishers/{str(publisher.pk)}/",
        data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == publisher_name


@pytest.mark.django_db
def test_patch_publisher__positive(client, publisher):
    publisher_name = "Другая новая книга"
    data = json.dumps({"name": publisher_name})
    response = client.patch(
        f"/store/publishers/{str(publisher.pk)}/",
        data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == publisher_name


@pytest.mark.django_db
def test_delete_publisher__positive(client, publisher):
    response = client.delete(f"/store/publishers/{publisher.pk}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
