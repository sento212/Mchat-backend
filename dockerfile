FROM python:3.12.4

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirement.txt

#buat flask
# RUN pip install gunicorn

# EXPOSE 8000

# CMD [ "python", "main.py" ]
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["gunicorn","--bind","0.0.0.0:8000","app:app"]

RUN pip install supervisor

RUN apt-get update && apt-get install -y supervisor && apt-get install -y haproxy

COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

COPY haproxy.cfg /etc/haproxy/haproxy.cfg

EXPOSE 8080

# RUN service haproxy restart

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# RUN supervisord -c /etc/supervisor/supervisord.conf

# CMD ["python", "-m", "websockets", "ws://localhost:8080/"]
# python -m websockets ws://localhost:8080/
