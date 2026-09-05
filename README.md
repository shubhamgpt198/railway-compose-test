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

The page should say **Backend: connected** and show `hello from the backend`.

## Railway / compose host

| Field | Value |
| --- | --- |
| Root directory | **leave empty** |
| Compose file | `docker-compose.yml` |

Public site is the **web** service (nginx). The API is reached as hostname `api` on port `8000` on the private network. If the host renames services, update `frontend/nginx.conf` (`proxy_pass http://api:8000`).
