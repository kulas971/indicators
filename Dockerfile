FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install -r /requirements.txt

RUN mkdir /indicators
COPY ./indicatorsproject /indicatorsproject/
WORKDIR /indicatorsproject





RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

EXPOSE 8000

CMD ["entrypoint.sh"]
