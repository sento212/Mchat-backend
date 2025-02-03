FROM python:3.12.4

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirement.txt

# EXPOSE 8000

CMD [ "python", "main.py" ]
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD python main.py
