# Isterlab website

Django website with a Channels chatbot and Redis. Docker and Docker Compose v2+
are required; no local Python environment is needed.

## Development

```bash
./start_isterlab.sh dev
```

The runner creates `.env.dev` from `.env.dev.example`, builds the image, runs
migrations, and waits for healthy services. Open http://localhost:8020.
Source is mounted for automatic reload. Development uses the existing
`db.sqlite3` and `media/` directory in this checkout. Back up the database before
running migrations on existing data. The runner builds using your user/group IDs
so bind-mounted files remain writable on Linux.

```bash
./scripts/stack.sh dev manage createsuperuser
./scripts/stack.sh dev manage test
./scripts/stack.sh dev logs --tail 100
./scripts/stack.sh dev status
./scripts/stack.sh dev down
```

## Production

```bash
cp .env.prod.example .env.prod
chmod 600 .env.prod
openssl rand -hex 32
# Set DJANGO_SECRET_KEY to the generated value in .env.prod.
# Set your domain in DJANGO_ALLOWED_HOSTS and DJANGO_CSRF_TRUSTED_ORIGINS.
./start_isterlab.sh prod
./scripts/stack.sh prod manage createsuperuser
```

Production runs Daphne, Redis, and Nginx. Migrations and `collectstatic` run before
Daphne starts. Only Nginx publishes a port, bound to `127.0.0.1:8020` by default.
Put a TLS reverse proxy in front of it and have that proxy overwrite
`X-Forwarded-Proto` with the connection's scheme. The production example enables
HTTPS redirects, secure cookies, and HSTS. Keep the bind address private when
`DJANGO_TRUST_PROXY=True`. Configure WebSocket forwarding on the outer proxy.

For a local HTTP production smoke test, use a separate environment file and set
`DJANGO_TRUST_PROXY=False`, `DJANGO_SECURE_SSL_REDIRECT=False`,
`DJANGO_SESSION_COOKIE_SECURE=False`, `DJANGO_CSRF_COOKIE_SECURE=False`, and
`DJANGO_SECURE_HSTS_SECONDS=0`. These are local testing settings.

Production starts with an empty SQLite database and empty uploads. Named volumes
preserve the database, uploads, and collected static assets across container
replacements and normal `down` operations. Development and production are separate
Compose projects. Do not use `down --volumes` on data you want to retain. SQLite
supports this single-server setup; move to PostgreSQL before scaling web replicas.
Back up both the database and uploads.

To import the checkout's existing data into a **new** production stack, stop the
web service first. These commands replace the production database, so take a
backup if the volume already contains data:

```bash
docker compose --env-file .env.prod -f compose.prod.yaml stop web nginx
# Run the copy as the application user to preserve writable ownership.
docker compose --env-file .env.prod -f compose.prod.yaml run --rm --no-deps \
  --entrypoint python -v "$PWD:/import:ro" web -c \
  "import shutil; shutil.copyfile('/import/db.sqlite3', '/data/db.sqlite3'); shutil.copytree('/import/media', '/app/media', dirs_exist_ok=True)"
./scripts/stack.sh prod up
```

Set `STACK_ENV_FILE` for a custom environment file. The runner resolves relative
paths from the repository root. If invoking Compose directly with a custom file,
set the same variable so both interpolation and service environment use it:

```bash
STACK_ENV_FILE=.env.custom ./scripts/stack.sh prod up
STACK_ENV_FILE=.env.custom docker compose --env-file .env.custom -f compose.prod.yaml config --quiet
```

`restart` restarts existing containers; use `up` after configuration or source
changes to rebuild and recreate them. The runner supports `build`, `config`,
`logs`, `status`, `down`, and `manage`, and forwards additional arguments.

## Integrations and checks

Set reCAPTCHA keys in the environment or through admin Constance settings before
using contact forms. Verification fails safely when unconfigured or unavailable.
`OPENAI_API_KEY` is optional; the AI WebSocket endpoint explains when it is missing.
The menu chatbot works independently of that key.

Google Analytics is optional. Set the property ID in Constance and mount your
service-account JSON into the container read-only with a Compose override; set
`GOOGLE_APPLICATION_CREDENTIALS` to that container path. Missing configuration or
unavailable analytics returns zero metrics so the admin dashboard remains usable.
Credentials, the checkout database, and uploads are excluded from the image.

```bash
./scripts/stack.sh dev manage check
./scripts/stack.sh dev manage test
./scripts/stack.sh prod manage check --deploy
```

Health probes use `/healthz/` and bypass HTTPS redirects for internal checks.
Redis readiness gates web startup, and Nginx waits for the web healthcheck.
See the [Compose startup documentation](https://docs.docker.com/compose/how-tos/startup-order/)
and [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

The bundled django-ckeditor integration uses unsupported CKEditor 4 and triggers
`ckeditor.W001`. Replacing it requires an editor migration or a licensed supported
CKEditor release; this remains an outstanding dependency issue.

Deployment checks also report optional HSTS subdomain/preload policies, which must
be chosen for the actual domain after confirming HTTPS coverage. `SAMEORIGIN`
framing is intentional: the website embeds its own chatbot in an iframe.
