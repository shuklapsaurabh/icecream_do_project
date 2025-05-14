import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Flavor, Order

@pytest.mark.django_db
@patch('api.views.process_payment.delay')
def test_create_order(mock_process_payment):
    user = User.objects.create_user(username='testuser', password='testpass')
    flavor = Flavor.objects.create(name='Vanilla')

    client = APIClient()
    token = client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    data = {'flavor': flavor.id, 'quantity': 2}
    print(f"Input data for create_order: {data}")
    response = client.post('/api/orders/', data)
    print(f"Response status: {response.status_code}, data: {response.data}")
    assert response.status_code == 200
    assert 'order_id' in response.data
    mock_process_payment.assert_called_once()

@pytest.mark.django_db
def test_add_flavor():
    client = APIClient()
    user = User.objects.create_user(username='flavoruser', password='flavorpass')
    token = client.post('/api/token/', {'username': 'flavoruser', 'password': 'flavorpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    data = {'name': 'Chocolate'}
    print(f"Input data for add_flavor: {data}")
    response = client.post('/api/flavors/add/', data)
    print(f"Response status: {response.status_code}, data: {response.data}")
    assert response.status_code == 201
    assert response.data['name'] == 'Chocolate'

@pytest.mark.django_db
def test_list_flavors():
    client = APIClient()
    user = User.objects.create_user(username='listflavoruser', password='listflavorpass')
    token = client.post('/api/token/', {'username': 'listflavoruser', 'password': 'listflavorpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    Flavor.objects.create(name='Strawberry')
    Flavor.objects.create(name='Mint')

    print("Requesting list_flavors")
    response = client.get('/api/flavors/')
    print(f"Response status: {response.status_code}, data: {response.data}")
    assert response.status_code == 200
    assert len(response.data) >= 2
    flavor_names = [flavor['name'] for flavor in response.data]
    assert 'Strawberry' in flavor_names
    assert 'Mint' in flavor_names

@pytest.mark.django_db
def test_list_orders():
    client = APIClient()
    user = User.objects.create_user(username='listorderuser', password='listorderpass')
    token = client.post('/api/token/', {'username': 'listorderuser', 'password': 'listorderpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    flavor = Flavor.objects.create(name='Pistachio')

    from api.models import Order
    Order.objects.create(user=user, flavor=flavor, quantity=3)

    print("Requesting list_orders")
    response = client.get('/api/my-orders/')
    print(f"Response status: {response.status_code}, data: {response.data}")
    assert response.status_code == 200
    assert len(response.data) >= 1
    assert response.data[0]['flavor'] == flavor.id
    assert response.data[0]['quantity'] == 3
    
@pytest.mark.django_db
def test_order_stats():
    user = User.objects.create_user(username='statuser', password='statpass')
    flavor1 = Flavor.objects.create(name='Vanilla')
    flavor2 = Flavor.objects.create(name='Chocolate')

    Order.objects.create(user=user, flavor=flavor1, quantity=3)
    Order.objects.create(user=user, flavor=flavor1, quantity=2)
    Order.objects.create(user=user, flavor=flavor2, quantity=2)

    client = APIClient()
    token = client.post('/api/token/', {'username': 'statuser', 'password': 'statpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
    print("Requesting order_stats")
    response = client.get('/api/stats/')
    print(f"Response status: {response.status_code}, data: {response.data}")
    assert response.status_code == 200

    data = response.data
    flavor_totals = {item['flavor__name']: item['total_qty_ordered'] for item in data}
    
    print(f"Flavor totals: {flavor_totals}")
    assert flavor_totals.get('Vanilla') == 5
    assert flavor_totals.get('Chocolate') == 2