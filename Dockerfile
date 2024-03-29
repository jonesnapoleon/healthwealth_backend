FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
RUN pip install pipenv

WORKDIR /code
COPY . /code

RUN pipenv install --system

CMD ["/code/startup.sh"]

