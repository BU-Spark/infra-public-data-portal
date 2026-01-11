#!/bin/sh
set -e

CONFIG_FILE=${CKAN_INI:-/srv/app/config/ckan.ini}

# 1) Generate ckan.ini if missing
if [ ! -f "$CONFIG_FILE" ]; then
  echo "[start_ckan.sh] Generating ckan.ini..."
  ckan generate config "$CONFIG_FILE" || {
    echo "[start_ckan.sh] Failed to generate config"
    exit 1
  }
fi

# 2) Initialize CKAN (DB, sysadmin user, plugins, etc.)
echo "[start_ckan.sh] Running prerun.py..."
python3 /srv/app/prerun.py || echo "[start_ckan.sh] prerun.py failed, continuing..."

# 3) Run any additional init scripts
if [ -d "/docker-entrypoint.d" ]; then
  for f in /docker-entrypoint.d/*; do
    case "$f" in
      *.sh)
        echo "[start_ckan.sh] Running init file $f"
        . "$f"
        ;;
      *.py)
        echo "[start_ckan.sh] Running init file $f"
        python3 "$f"
        ;;
      *)
        echo "[start_ckan.sh] Ignoring $f (not an sh or py file)"
        ;;
    esac
  done
fi

# 4) uWSGI options
UWSGI_OPTS="--plugins http,python \
--socket /tmp/uwsgi.sock \
--wsgi-file /srv/app/wsgi.py \
--module wsgi:application \
--http 0.0.0.0:${CKAN_PORT:-5000} \
--master --enable-threads \
--lazy-apps \
-p ${UWSGI_PROCESSES:-2} \
-L -b 32768 --vacuum \
--harakiri ${UWSGI_HARAKIRI:-60}"

echo "[start_ckan.sh] Starting supervisord and uWSGI..."

# 5) Launch supervisord in the foreground (it will daemonize uWSGI)
exec supervisord --nodaemon --configuration /etc/supervisord.conf &

# 6) Replace this shell with uWSGI
exec uwsgi $UWSGI_OPTS
