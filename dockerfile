FROM python:3.12.4


RUN apt-get update && apt-get install -y --no-install-recommends openssh-client && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirement.txt

# RUN chmod +x entrypoint.sh



##### Fix Windows line endings and make the entrypoint executable, only run in windows #######
# RUN sed -i 's/\r$//' python && chmod 600 python \
#     && sed -i 's/\r$//' entry_point.sh && chmod +x entry_point.sh
# ENTRYPOINT ["./entry_point.sh"]

######## pilih salah satu okay #########


####### buat flask #######

# RUN pip install gunicorn
# EXPOSE 5000

##### testing main backend #######
# CMD ["python", "app.py"]

##### running deplyment #######
# CMD ["gunicorn","--bind","0.0.0.0:5000","app:app"]


########  buat websocket #######


RUN pip install supervisor

RUN pip install websocket-client 

RUN apt-get update && apt-get install -y supervisor && apt-get install -y haproxy

COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

COPY haproxy.cfg /etc/haproxy/haproxy.cfg

EXPOSE 8080

##### deployment #####
# RUN service haproxy restart
# CMD ["/app/entrypoint2.sh"]

###### for testing #######
CMD ["python", "main.py"]
