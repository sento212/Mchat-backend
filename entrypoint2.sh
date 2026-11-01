#!/bin/bash

# Start HAProxy in the background
haproxy -f /etc/haproxy/haproxy.cfg &

# Run Supervisor in the foreground (PID 1) to keep the container alive
exec supervisord -c /etc/supervisor/supervisord.conf