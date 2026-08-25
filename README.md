# shop_api

Minimal Django project exposing API endpoints for Category, Product, and Review.

Endpoints:

- `GET /api/v1/categories/` — list categories
- `GET /api/v1/categories/<id>/` — retrieve category
- `GET /api/v1/products/` — list products
- `GET /api/v1/products/<id>/` — retrieve product
- `GET /api/v1/reviews/` — list reviews
- `GET /api/v1/reviews/<id>/` — retrieve review

Quick start:

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```
