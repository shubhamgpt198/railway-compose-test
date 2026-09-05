#!/bin/sh
set -eu
# Prefer the web/api-specific ports so a shared PORT from the host
# (often the frontend) does not move the backend off its listen port.
LISTEN_PORT="${PORT_WEB:-${PORT:-80}}"
API_HOST="${API_HOST:-api}"
API_PORT="${PORT_API:-${API_PORT:-8000}}"
API_UPSTREAM="${API_HOST}:${API_PORT}"
echo "[web] listen ${LISTEN_PORT}; proxy /api -> http://${API_UPSTREAM}" >&2
sed \
  -e "s/LISTEN_PORT/${LISTEN_PORT}/" \
  -e "s/API_UPSTREAM/${API_UPSTREAM}/" \
  /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf
exec nginx -g "daemon off;"
