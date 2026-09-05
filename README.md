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

The **Call log** on the page is written by JavaScript in the browser. It does **not** go to Docker. Container logs are only what nginx and the API print:

```bash
docker compose logs -f api web
```

- `api`: `[api …] received GET /api/hello … -> 200`
- `web`: `[web …] GET /api/hello -> 200 upstream=172.x.x.x:8000`

A **502** on the page with nothing in `api` logs means nginx never reached the backend. Check the `web` service log for `upstream=` / connect errors.

## Railway / OpenDeploy

| Field | Value |
| --- | --- |
| Root directory | **leave empty** |
| Build | Auto, or Docker Compose |
| Compose file | `docker-compose.yml` or leave empty — **do not type `-f`** |
| Compose service | `web` |
| Web container port | `80` locally, or `8080` if that is what nginx should listen on |
| API container port | must match the API process (`8000` default, or `8001` if you set `PORT_API=8001`) |

If the page shows **HTTP 502**, nginx cannot reach the API. The web service proxies `/api` to `api:$PORT_API` (default `api:8000`). Host ports (8080 / 8001) are only for the browser; inside the compose network the API is still hostname `api`.

`web` is first so a blank compose-service field still publishes the site. nginx proxies `/api` to hostname `api` port `8000`. If the host renames services, update `frontend/nginx.conf`.
