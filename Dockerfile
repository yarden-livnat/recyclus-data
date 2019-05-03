
FROM python:3.6-alpine

RUN apk update && apk add bash && rm -rf /var/cache/apk/*

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -U pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["./manage.py", "run"]

EXPOSE 5020



