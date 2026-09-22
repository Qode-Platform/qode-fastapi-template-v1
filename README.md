# FastAPI template

Provisioned from [`Qode-Platform/fleet-template-v1`](https://github.com/Qode-Platform/fleet-template-v1) — the fleet
lifecycle contract (`bin/`, `fleet.conf`, deploy workflows) with a
FastAPI starter laid on top.

## Origin

    hand-written (no official generator) — 'Bigger Applications' layout

Generated 2026-09-21 on Node v22.12.0 / Python 3.12.3. **Dependencies were
never installed and this has never been built or run.** Boot it once before
trusting it.

## Fleet lifecycle

`fleet.conf` drives every script in `bin/`:

| step | command |
|---|---|
| install | `python3 -m venv .venv && .venv/bin/pip install --upgrade pip -r requirements.txt` |
| build | `(none)` |
| start | `.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

    ./bin/run       # install, build, start in the foreground
    ./bin/start     # start from existing build artifacts
    ./bin/restart   # rebuild and restart
    ./bin/stop      # stop whatever holds the port

Listens on `$PORT` (default `8000`); health check hits `/healthz`.

## BASE_PATH

The fleet injects `BASE_PATH` (`/direct/<agent>:<port>`) and nginx forwards
that prefix **unchanged** — so this app serves every route and asset under
it. An empty or unset value means standalone mode: serve at the host root.

- Every route hangs off one APIRouter(prefix=BASE_PATH); docs/openapi URLs carry it too.
- `HEALTH_PATH` in `fleet.conf` stays un-prefixed; the fleet prepends `$BASE_PATH` itself.
- A value like `direct/x:3000/` is normalised to `/direct/x:3000`.
- Verified here: 6 tests pass, covering root mode, prefixed mode and a sloppy `direct/x/` value.

---

# FastAPI scaffold

Hand-written — FastAPI ships no project generator. Layout follows the
"Bigger Applications" page of the official docs.

    python -m venv .venv && . .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload     # http://127.0.0.1:8000/docs
    pytest

- `app/main.py` wires routers and owns the lifespan hook.
- `app/routers/` — one module per resource.
- `app/models.py` — Pydantic schemas (not ORM models).
- `app/config.py` — env-driven settings, cached.

## Rule: everything under BASE_PATH

The fleet serves this app behind a proxy at `BASE_PATH=/direct/<agent>:<port>`, and the
prefix is forwarded **unchanged** — it is NOT stripped before it reaches the app. So every
route, every redirect, every asset URL and the docs/OpenAPI URLs must carry `$BASE_PATH`.

Never hard-code a leading-slash path in a response, a `RedirectResponse`, or a template.
`RedirectResponse("/items")` and `href="/docs"` point at the proxy's root and 404.

Use this template's own mechanism:

- `app/base_path.py` normalises `$BASE_PATH`; `app/main.py` creates **one**
  `APIRouter(prefix=BASE_PATH)` and every other router is included into it. Adding a
  resource means `root.include_router(...)` — never a second prefix.
- `docs_url`, `redoc_url` and `openapi_url` are set with the prefix on the `FastAPI()`
  constructor. Keep them that way.
- Build outgoing URLs from `BASE_PATH` (e.g. `f"{BASE_PATH}/items"`), or from
  `request.url_for(...)`, which already accounts for the mount.
- `HEALTH_PATH` in `fleet.conf` stays un-prefixed; the fleet prepends `$BASE_PATH` itself.
