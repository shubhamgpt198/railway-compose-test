# railway-compose-test

Dummy **frontend + backend** app for checking a compose deploy. It is **not** openOES.

| Path | What |
| --- | --- |
| `docker-compose.yml` | root compose file (`api` + `web`) |
| `backend/` | Python JSON API |
| `frontend/` | static HTML behind nginx; `/api` is proxied to `api:8000` |

Build context is the **repo root** for both images. Do not set a Railway/OpenDeploy root directory to `backend` or `frontend`.

## Local

```bash
docker compose up --build
```

- Frontend: http://localhost:8080
- Backend direct: http://localhost:8001/api/hello
- Health: http://localhost:8001/api/health

The page should say **Backend: connected** and show `hello from the backend`. Each click logs the request in the page and in `docker compose logs`:

```bash
docker compose logs -f api web
```

API lines look like `[api 2026-09-05T10:30:00.000000Z] GET /api/hello from 172.18.0.3 -> 200`.

## Railway / OpenDeploy

| Field | Value |
| --- | --- |
| Root directory | **leave empty** |
| Build | Auto, or Docker Compose |
| Compose file | `docker-compose.yml` or leave empty — **do not type `-f`** |
| Compose service | `web` |
| Web container port | `80` |
| API container port | `8000` |

`web` is first so a blank compose-service field still publishes the site. nginx proxies `/api` to hostname `api` port `8000`. If the host renames services, update `frontend/nginx.conf`.
