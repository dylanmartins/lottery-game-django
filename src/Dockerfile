FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=core.settings

RUN apt-get clean && apt-get update

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD python manage.py runserver 0.0.0.0:8000