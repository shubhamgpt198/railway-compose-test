#!/bin/sh
set -eu
PORT="${PORT:-80}"
sed "s/LISTEN_PORT/${PORT}/" /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf
exec nginx -g "daemon off;"
