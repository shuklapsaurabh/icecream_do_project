import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Flavor

@pytest.mark.django_db
def test_create_order():
    user = User.objects.create_user(username='testuser', password='testpass')
    flavor = Flavor.objects.create(name='Vanilla')

    client = APIClient()
    token = client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = client.post('/api/orders/', {'flavor': flavor.id, 'quantity': 2})
    assert response.status_code == 200
    assert 'order_id' in response.data