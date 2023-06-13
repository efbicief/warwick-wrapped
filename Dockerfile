FROM python:3.9

RUN pip install pipenv
WORKDIR /app
COPY . .
RUN pipenv install --system
CMD gunicorn app:app -b 0.0.0.0:8080