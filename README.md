# Collection Manager

A full-stack application for managing personal collections of any type — action figures, trading cards, comics, vinyl, and more.

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework, PostgreSQL
- **Frontend:** Vue 3, Vite, Pinia, Tailwind CSS
- **Auth:** OAuth 2.0 (Google + GitHub) via django-allauth + JWT
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

2. Fill in your OAuth credentials in `.env`. You'll need:
   - [Google OAuth App](https://console.cloud.google.com/) — set redirect URI to `http://localhost:5173/auth/callback/google`
   - [GitHub OAuth App](https://github.com/settings/developers) — set callback URL to `http://localhost:5173/auth/callback/github`

3. Start all services:
```bash
   docker compose up --build
```

4. In a separate terminal, create a superuser:
```bash
   docker compose exec backend python manage.py createsuperuser --settings=collection_manager.settings.development
```

5. Access the app:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/
   - Django Admin: http://localhost:8000/admin/

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/collections/` | List your collections |
| POST | `/api/collections/` | Create a collection |
| GET | `/api/collections/{id}/` | Get collection + items |
| PATCH | `/api/collections/{id}/` | Update collection |
| DELETE | `/api/collections/{id}/` | Delete collection |
| GET | `/api/collections/{id}/stats/` | Collection stats |
| GET | `/api/collections/{id}/items/` | List items |
| POST | `/api/collections/{id}/items/` | Add item |
| GET | `/api/collections/{id}/items/{itemId}/` | Get item |
| PATCH | `/api/collections/{id}/items/{itemId}/` | Update item |
| DELETE | `/api/collections/{id}/items/{itemId}/` | Delete item |
| POST | `/api/auth/google/` | Google OAuth login |
| POST | `/api/auth/github/` | GitHub OAuth login |
| POST | `/api/auth/token/refresh/` | Refresh JWT |
| GET | `/api/auth/me/` | Current user |
| POST | `/api/auth/logout/` | Logout + blacklist token |

## Collection Item Fields

Each item in a collection supports: `name`, `version`, `description`, `price_paid`, `current_value`, `manufacturer`, `originating_property`, `status`, `image`, `acquired_at`, `notes`.

## Project Structure
```
collection-manager/
├── backend/          # Django API
├── frontend/         # Vue 3 SPA
├── docker-compose.yml
├── .env.example
└── .github/workflows/ci.yml
```

## Roadmap

- [ ] Public collection sharing
- [ ] CSV import/export
- [ ] Barcode scanning for item lookup
- [ ] Price tracking over time
- [ ] Collection comparison / analytics dashboard
