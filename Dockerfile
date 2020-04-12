FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 8000

CMD ["python marketplace/manage.py runserver]