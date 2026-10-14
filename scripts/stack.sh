#!/usr/bin/env bash
set -Eeuo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

usage() {
    cat <<'HELP'
Usage: ./scripts/stack.sh [dev|prod] [up|down|restart|logs|status|build|config|manage] [arguments...]
Defaults: dev up. Up builds and starts in the background, waiting for healthchecks.
Examples:
  ./scripts/stack.sh dev up
  ./scripts/stack.sh prod up
  ./scripts/stack.sh prod manage createsuperuser
  ./scripts/stack.sh dev manage test
  ./scripts/stack.sh prod logs --tail 100
Set STACK_ENV_FILE to use a different environment file.
HELP
}
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then usage; exit 0; fi
mode="${1:-dev}"
action="${2:-up}"
if (( $# > 0 )); then shift; fi
if (( $# > 0 )); then shift; fi
case "$mode" in dev|prod) ;; *) usage >&2; exit 2 ;; esac
case "$action" in up|down|restart|logs|status|build|config|manage) ;; *) usage >&2; exit 2 ;; esac
command -v docker >/dev/null || { echo 'Docker is required.' >&2; exit 1; }
docker compose version >/dev/null || { echo 'Docker Compose v2 or newer is required.' >&2; exit 1; }
export STACK_ENV_FILE="${STACK_ENV_FILE:-.env.$mode}"
export APP_UID="${APP_UID:-$(id -u)}"
export APP_GID="${APP_GID:-$(id -g)}"
if [[ ! -f "$STACK_ENV_FILE" ]]; then
    if [[ "$mode" == dev ]]; then
        (umask 077; cp .env.dev.example "$STACK_ENV_FILE")
        echo "Created $STACK_ENV_FILE from the development example."
    else
        echo "Copy .env.prod.example to $STACK_ENV_FILE and configure the secret and domain first." >&2
        exit 1
    fi
fi
compose=(docker compose --env-file "$STACK_ENV_FILE" -f "compose.$mode.yaml")
case "$action" in
    up) "${compose[@]}" up --build --detach --wait --wait-timeout 180 "$@" ;;
    down) "${compose[@]}" down "$@" ;;
    restart) "${compose[@]}" restart "$@" ;;
    logs) "${compose[@]}" logs --follow "$@" ;;
    status) "${compose[@]}" ps "$@" ;;
    build) "${compose[@]}" build "$@" ;;
    config) "${compose[@]}" config "$@" ;;
    manage)
        (( $# > 0 )) || { echo 'Provide a Django management command.' >&2; exit 2; }
        "${compose[@]}" exec web python manage.py "$@"
        ;;
esac
