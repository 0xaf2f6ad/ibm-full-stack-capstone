FROM python:3.10-slim as base

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app/

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

FROM base as development

EXPOSE 8000

CMD ["/bin/sh", "./start.sh", "dev"]

FROM base as production

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "./start.sh", "prod"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
