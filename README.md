# Collection Manager

A full-stack application for managing personal collections of any type — action figures, trading cards, comics, vinyl, and more.

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework, PostgreSQL
- **Frontend:** Vue 3, Vite, Pinia, Tailwind CSS
- **Auth:** Username + password with Django session authentication
- **Infrastructure:** Docker Compose, GitHub Actions CI

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)

### Setup

1. Clone the repo and copy the env file:
```bash
   cp .env.example .env
```

2. Fill in your `.env` values (at minimum set a strong `SECRET_KEY`).

3. Install frontend dependencies to generate `package-lock.json`:
```bash
   cd frontend && npm install && cd ..
```

4. Start all services:
```bash
   docker compose up --build
```

5. In a separate terminal, run migrations:
```bash
   docker compose run --rm backend python manage.py makemigrations accounts --settings=collection_manager.settings.development
   docker compose run --rm backend python manage.py makemigrations collections --settings=collection_manager.settings.development
   docker compose run --rm backend python manage.py migrate --settings=collection_manager.settings.development
```

6. Create a superuser for the Django admin:
```bash
   docker compose run --rm backend python manage.py createsuperuser --settings=collection_manager.settings.development
```

7. Access the app:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/
   - Django Admin: http://localhost:8000/admin/

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | — |
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:5173` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated CSRF trusted origins | `http://localhost:5173` |
| `DB_NAME` | PostgreSQL database name | `collection_manager` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `postgres` |
| `DB_HOST` | PostgreSQL host | `db` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `VITE_API_URL` | Backend API base URL (frontend) | `http://localhost:8000` |

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/csrf/` | Get CSRF token |
| POST | `/api/auth/register/` | Register new account |
| POST | `/api/auth/login/` | Log in |
| POST | `/api/auth/logout/` | Log out |
| GET | `/api/auth/me/` | Get current user |
| PATCH | `/api/auth/me/` | Update profile |
| POST | `/api/auth/password/` | Change password |
| GET | `/api/collections/` | List your collections |
| POST | `/api/collections/` | Create a collection |
| GET | `/api/collections/{id}/` | Get collection + items |
| PATCH | `/api/collections/{id}/` | Update collection |
| DELETE | `/api/collections/{id}/` | Delete collection |
| GET | `/api/collections/{id}/stats/` | Collection value stats |
| GET | `/api/collections/{id}/items/` | List items |
| POST | `/api/collections/{id}/items/` | Add item |
| GET | `/api/collections/{id}/items/{itemId}/` | Get item |
| PATCH | `/api/collections/{id}/items/{itemId}/` | Update item |
| DELETE | `/api/collections/{id}/items/{itemId}/` | Delete item |

## Collection Item Fields

Each item in a collection supports: `name`, `version`, `description`, `price_paid`, `current_value`, `manufacturer`, `originating_property`, `status`, `image`, `acquired_at`, `notes`.

## Authentication

The app uses Django's built-in session authentication. On login, Django sets a signed session cookie that is sent automatically with every subsequent request. CSRF protection is enforced on all mutating endpoints — the frontend fetches a CSRF token on first use and attaches it via the `X-CSRFToken` header.

## Project Structure
```
collection-manager/
├── backend/
│   ├── apps/
│   │   ├── accounts/       # Auth — register, login, logout, profile
│   │   └── collections/    # Collections + items CRUD
│   ├── collection_manager/ # Django project config + settings
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios instance + endpoint modules
│   │   ├── components/     # NavBar, CollectionCard, ItemCard
│   │   ├── router/         # Vue Router with auth guards
│   │   ├── stores/         # Pinia — auth + collections state
│   │   └── views/          # Login, Dashboard, Collection, ItemForm
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Roadmap

- [ ] Public collection sharing
- [ ] CSV import/export
- [ ] Barcode scanning for item lookup
- [ ] Price tracking over time
- [ ] Collection comparison / analytics dashboard
