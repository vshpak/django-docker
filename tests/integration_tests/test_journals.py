import json
import pytest
from rest_framework import status
from store.serializers import JournalSerializer


@pytest.mark.django_db
def test_get_journals__positive(client):
    response = client.get("/store/journals/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_journal__positive(client, journal):
    response = client.get(f"/store/journals/{journal.pk}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_journal__positive(client, publisher):
    journal_name = "Серый лед"
    data = json.dumps(
        {"name": journal_name, "article_set": [], "publisher": publisher.pk}
    )
    response = client.post("/store/journals/", data, content_type="application/json")
    created_journal = dict(JournalSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_201_CREATED
    assert created_journal["name"] == journal_name
    assert created_journal["publisher"].name == publisher.name


@pytest.mark.django_db
def test_put_journal__positive(client, journal):
    journal_name = "Новый журнал"
    data = json.dumps(
        {
            "id": journal.pk,
            "name": journal_name,
            "publisher": journal.publisher.pk,
            "article_set": [],
        }
    )
    response = client.put(
        f"/store/journals/{str(journal.pk)}/",
        data,
        content_type="application/json",
    )
    updated_journal = dict(JournalSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert updated_journal["name"] == journal_name


@pytest.mark.django_db
def test_patch_journal__positive(client, journal):
    journal_name = "Другой новый журнал"
    data = json.dumps({"name": journal_name})
    response = client.patch(
        f"/store/journals/{str(journal.pk)}/",
        data,
        content_type="application/json",
    )
    updated_journal = dict(JournalSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert updated_journal["name"] == journal_name


@pytest.mark.django_db
def test_delete_journal__positive(client, journal):
    response = client.delete(f"/store/journals/{journal.pk}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT