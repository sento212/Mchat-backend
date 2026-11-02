#!/bin/sh

# 1. Ensure correct permissions for the SSH key
chmod 600 /app/python

# 2. Start the SSH tunnel in the background (&)
# This forwards local port 5432 inside the container to the remote PostgreSQL server
ssh -v \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -i /app/python \
    -N -L 0.0.0.0:5432:127.0.0.1:5432 www_intermoon7030@34.45.217.161 &

# Give the tunnel a couple of seconds to establish connection
sleep 2

exec "$@"
# 3. Start your Python application
# exec python main.py