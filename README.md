# Aforro Backend Assignment

## Overview

This project is a backend system built using Django and Django REST Framework.
It implements a store-based product inventory and order management system with search, caching, and asynchronous processing.

---

## Features

* Product & Category management
* Store & Inventory system
* Order creation with stock validation
* Product search with filters & pagination
* Autocomplete suggestions API
* Redis caching for performance optimization
* Celery for asynchronous task processing
* Dockerized setup for easy deployment
* Seed data generation
* Unit tests

---

## Tech Stack

* Python
* Django & Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker

---

## Setup Instructions

### Using Docker (Recommended)

```bash
docker-compose up --build
```

This will start:

* Django server
* PostgreSQL database
* Redis
* Celery worker

---

### Run Seed Data

```bash
docker-compose exec web python manage.py seed_data
```

---

## API Endpoints

### Create Order

POST /orders/

Request:

```json
{
  "store_id": 1,
  "items": [
    {"product_id": 1, "quantity_requested": 2}
  ]
}
```

Response:

```json
{
  "message": "Order confirmed",
  "order_id": 1,
  "status": "CONFIRMED"
}
```

---

### Store Orders

GET /stores/<store_id>/orders/

---

### Store Inventory

GET /stores/<store_id>/inventory/

---

### Product Search

GET /api/search/products/?q=phone&min_price=100&max_price=1000

---

### Autocomplete

GET /api/search/suggest/?q=pho

---

## Caching Strategy

* Redis is used to cache product search results
* Cache key is generated using request query parameters
* Cache timeout: 5 minutes
* Cache invalidation: cleared on product/inventory updates

---

## Celery (Async Tasks)

* Redis used as message broker
* Background task:

  * Order confirmation handler

Run worker:

```bash
docker-compose up celery
```

---

## Running Tests

```bash
docker-compose exec web python manage.py test
```

---

## Data Seeding

Generates:

* 10+ categories
* 1000+ products
* 20+ stores
* Inventory with 300+ products per store

---

## Design Decisions

* Used `transaction.atomic()` for safe order processing
* Used `select_for_update()` to prevent race conditions
* Used `select_related()` to avoid N+1 queries
* Used `annotate()` for aggregation
* Used Redis caching to improve search performance

---

## Scalability Considerations

* Can integrate full-text search (Elasticsearch)
* Can use Redis for rate limiting
* Can add async email notifications
* Can scale using multiple Celery workers

---

## Author

Mohanraj
