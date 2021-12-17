import json
import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework import status
from store.serializers import PublisherSerializer

# @pytest.mark.django_db
# @patch('store.views.increment_access_counter')
# def test_get_publishers__negative(mocked_increment_access_counter, client, publisher):
#     mocked_increment_access_counter.return_value = False
#     response = client.get(f'/store/publishers/{publisher.pk}/')
#
#     assert response.status_code == status.HTTP_200_OK
#     # assert response.status_code == 400
#     # assert mocked_increment_access_counter.called
#     # mocked_increment_access_counter.assert_called_once_with('publisher', publisher.pk)


@pytest.mark.django_db
def test_get_publishers__positive(client):
    response = client.get(f'/store/publishers/')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_publisher__positive(client, publisher):
    response = client.get(f'/store/publishers/{publisher.pk}/')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_publisher__positive(client):
    publisher_name = 'Родина'
    publisher_address = "Владивосток"
    data = json.dumps({'name': publisher_name, 'address': publisher_address})
    response = client.post(f'/store/publishers/', data, content_type='application/json')
    created_publisher = dict(PublisherSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_201_CREATED
    assert created_publisher['name'] == publisher_name


@pytest.mark.django_db
def test_put_publisher__positive(client, publisher):
    publisher_name = "Новая книга"
    publisher_address = "Москва"
    data = json.dumps({'id': publisher.pk, 'name': publisher_name, 'address': publisher_address})
    response = client.put(f'/store/publishers/' + str(publisher.pk) + '/', data, content_type='application/json')
    updated_publisher = dict(PublisherSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert updated_publisher['name'] == publisher_name


@pytest.mark.django_db
def test_patch_publisher__positive(client, publisher):
    publisher_name = "Другая новая книга"
    data = json.dumps({'name': publisher_name})
    response = client.patch(f'/store/publishers/' + str(publisher.pk) + '/', data, content_type='application/json')
    updated_publisher = dict(PublisherSerializer().to_internal_value(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert updated_publisher['name'] == publisher_name
