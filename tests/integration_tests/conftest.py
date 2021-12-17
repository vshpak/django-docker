import pytest
from rest_framework.test import APIClient

from store.models import Publisher, Book, Journal, Article
from django.contrib.auth import get_user_model


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create(username='test_user')


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(login='test_user')
    return client


@pytest.fixture
def publisher():
    return Publisher.objects.create(name='Лабиринт', address='Тверь')


@pytest.fixture
def book(publisher):
    return Book.objects.create(name='Война и мир', publisher=publisher)


@pytest.fixture
def journal(publisher):
    return Journal.objects.create(name='Светские хроники', publisher=publisher)


@pytest.fixture
def article(journal):
    return Article.objects.create(name='Новости минувшей недели', journal=journal)


