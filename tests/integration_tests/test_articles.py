import pytest
import json
from rest_framework import status
from store.serializers import ArticleSerializer


@pytest.mark.django_db
def test_get_articles_by_journal_id__positive(client, journal):
    response = client.get(f"/store/journals/{journal.pk}/articles/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_articles__positive(client):
    response = client.get("/store/articles/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_article__positive(client, article):
    response = client.get(f"/store/articles/{article.pk}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_article__positive(client, journal, author):
    article_name = "Главное событие недели"
    data = json.dumps(
        {"name": article_name, "journal": journal.pk, "authors": [author.pk]}
    )
    response = client.post("/store/articles/", data, content_type="application/json")
    created_article = dict(ArticleSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_201_CREATED
    assert created_article["name"] == article_name
    assert created_article["journal"].name == journal.name


@pytest.mark.django_db
def test_put_article__positive(client, article, journal, author):
    article_name = "Новое событие недели"
    data = json.dumps(
        {
            "id": article.pk,
            "name": article_name,
            "journal": journal.pk,
            "authors": [author.pk],
        }
    )
    response = client.put(
        f"/store/articles/{str(article.pk)}/",
        data,
        content_type="application/json",
    )
    updated_article = dict(ArticleSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert updated_article["name"] == article_name


@pytest.mark.django_db
def test_patch_article__positive(client, article):
    article_name = "Другое событие недели"
    data = json.dumps({"name": article_name})
    response = client.patch(
        f"/store/articles/{str(article.pk)}/",
        data,
        content_type="application/json",
    )
    updated_article = dict(ArticleSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert updated_article["name"] == article_name
