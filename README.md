# 🍦 Ice Cream Distribution API

A Python(Django) based REST API to manage ice cream flavors, place orders, and view analytics. Built with Django REST Framework and Celery for background payment processing.

---

## ✨ Features

* JWT Authentication
* Flavor Management (Add/List)
* Order Creation with Background Payment Simulation
* Order Analytics Dashboard

---

## 📁 Project Structure

```
.
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
├── postman_collection
│   ├── DeepOp_Icecream_API_Collection.postman_collection.json
├── icecream
│   ├── __init__.py
│   ├── celery.py
│   ├── settings.py
│   └── urls.py
├── staticfiles/
│   └── rest_framework/
├── .env
├── .env.example
├── db.sqlite3
├── docker-compose.yml
├── dockerfile
├── dump.rdb
├── manage.py
├── requirements.txt
├── venv/
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shuklapsaurabh/icecream_do_project.git
cd icecream-api
```

### 2. Create/Verify `.env` File

```
DJANGO_SETTINGS_MODULE=icecream.settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND='django-db'
```

### 3. Build and Run with Docker

```bash
docker compose build
docker compose up
```

### 4. Apply Migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

---


## API Endpoints

> ⚠️ All protected endpoints require JWT authentication using a Bearer Token obtained from the login endpoint.

#### Postman Collection path 

```
icecream_do_project >> postman_collection >> .json file
```

## 🔗 Base URL

```
http://127.0.0.1:8000
```

### 🔑 Auth

### Generate Token

#### POST `/api/token/`

Obtain JWT access token for authenticated requests.

#### Request

Content-Type: `application/x-www-form-urlencoded`

| Parameter | Type | Example   |
|-----------|------|-----------|
| username  | text | `admin`   |
| password  | text | `Test@1234` |

#### Response

```json
{
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>"
}
```

---

### 🍦 Flavors

#### POST `/api/flavors/add/`

Add a new flavor (Auth required).

#### Auth

Bearer Token: `{{access_token}}`  
Content-Type: `application/x-www-form-urlencoded`

#### Request

| Parameter | Type | Example  |
|-----------|------|----------|
| name      | text | Choclate  |

#### Response

```json
{
    "id": 2,
    "name": "Choclate"
}
```

#### GET `/api/flavors/`

List all available flavors.

#### Auth

Bearer Token: `{{access_token}}`

#### Response

```json
{
    "id": 1,
    "name": "Vanilla"
},
{
    "id": 2,
    "name": "Choclate"
},
```

---

### 🍨 Orders

#### POST `/api/orders/`

Create an order (Auth required).

#### Auth

Bearer Token: `{{access_token}}`  
Content-Type: `application/x-www-form-urlencoded`

#### Request

| Parameter | Type | Description      |
|-----------|------|------------------|
| quantity  | text | Quantity to order |
| flavor    | text | Flavor ID         |

```json
{
  "quantity": 1,
  "flavor": 2
}
```

#### Response

```json
{
    "status": "Order placed",
    "order_id": 1
}
```

#### GET `/api/orders/`

List all orders for the logged-in user.

#### Auth

Bearer Token: `{{access_token}}`

#### Response

```json
[
    {
        "id": 1,
        "quantity": 2,
        "status": "pending",
        "created_at": "2025-05-13T10:22:06.428877Z",
        "user": 1,
        "flavor": 1
    },
    {
        "id": 2,
        "quantity": 1,
        "status": "pending",
        "created_at": "2025-05-13T10:41:36.955378Z",
        "user": 1,
        "flavor": 2
    }
]
```

---

### 📊 Analytics

#### GET `/api/stats/`

Get total quantity ordered per flavor.

#### Auth

Bearer Token: `{{access_token}}`

#### Response

```json
[
    {
        "flavor__name": "Choclate",
        "total_qty_ordered": 4
    },
    {
        "flavor__name": "Vanilla",
        "total_qty_ordered": 1
    }
]
```

---

## 📊 Tech Stack

* Python 3.11
* Django 5.2.1
* Django REST Framework
* Celery + Redis
* SQLite (default, switchable)

---


