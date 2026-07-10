#!/bin/sh

python3 /app/health.py &

exec turnserver -c /etc/coturn/turnserver.conf -o
