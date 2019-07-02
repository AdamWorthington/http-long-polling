FROM python:2.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "-k", "gevent", "-t", "10", "app:app"]
