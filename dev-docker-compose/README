# Development Environment (Docker Compose)

This directory contains a Docker Compose setup for local development
of `fichub.net`. It launches PostgreSQL, Elasticsearch, a fake Alexandria
API, migration/index bootstrap jobs, and the Flask application with source
code mounted for hot reloading.

## Prerequisites

- Docker Engine (Docker Desktop)
- `make` (optional; used for building frontend assets)

## Setup

1. Configure credentials in `dev-docker-compose/authentications.py`.

   ```sh
   cd dev-docker-compose
   cp authentications.ex.py authentications.py   # if you need a fresh local copy
   ```

2. `rl_conf.dev.py` is mounted as `src/fichub_net/rl_conf.py` automatically,
   so no separate copy step is required.

3. Optionally populate `authentications.py` with real credentials. Leaving the
   default redacted values is fine when using the fake Alexandria service.

4. Build frontend assets if you plan to modify the UI:

   ```sh
   make frontend    # run from the project root
   ```

## Running the services

Start everything in detached mode (first run should include `--build`):

```sh
docker compose up -d --build
```

The following services are included:

- `db` - PostgreSQL 14.8
- `es` - Elasticsearch 8.8.0
- `es-init` - one-shot Elasticsearch index bootstrap (`uv run ./src/fichub_net/es.py`)
- `app-migrate` - one-shot DB migration job (`uv run ./src/fichub_net/db.py migrate`)
- `ax` - local HTTP server for fake Alexandria responses from `tests/dat/ax`
- `app` - Flask development server (`flask run --debug --host 0.0.0.0`)

If code changes are not reflected, rebuild the image:

```sh
docker compose build
```

To restart only the application container:

```sh
docker compose restart app
```

Access the running site at `http://localhost:59294/`.

### Testing with Fake Alexandria

The fake Alexandria service serves responses based on files in
`tests/dat/ax`. A sample story with URL ID `foo` is available for quick
validation.

> **Note:** `Dockerfile.dev` installs Calibre and sets `JANUS_USE_LOCAL_CALIBRE=true`,
> so local MOBI/PDF conversion is available in this dev setup.
