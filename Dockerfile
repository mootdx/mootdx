FROM python:3.8
ENV PYTHONUNBUFFERED 1

#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
# RUN apk add py3-pandas

#RUN apk add --no-cache --virtual .build-deps openssl-dev make autoconf automake gcc g++ postgresql-dev zlib-dev
#RUN apk add --no-cache supervisor py3-lxml libevent py3-pillow python3-dev py3-gevent py3-psycopg2 py3-crypto libpng-dev jpeg-dev
#RUN apk add --no-cache py3-pip py3-psutil py3-gunicorn py3-redis

COPY ./requirements.txt /requirements.txt
COPY ./tests/requirements.txt /requirements.dev
# COPY ./entrypoint.sh /entrypoint.sh

# RUN /usr/local/bin/pip install -U pip setuptools_scm meinheld uvicorn -i https://mirrors.aliyun.com/pypi/simple/
RUN /usr/local/bin/pip install -r /requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN /usr/local/bin/pip install -r /requirements.dev -i https://mirrors.aliyun.com/pypi/simple/

# RUN sed -i 's/\r//' /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# RUN apk del .build-deps
RUN mkdir /app

WORKDIR /app
VOLUME /app

#Add target/release.tgz /app/
#COPY ../environ/env.docker /app/.env

# COPY ./requirements.in /tmp/requirements.in
# RUN /usr/bin/pip install -r /tmp/requirements.in -i https://mirrors.aliyun.com/pypi/simple/ && rm /tmp/requirements.in
# RUN /usr/bin/pip install nanoid -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

#ENTRYPOINT ["/entrypoint.sh"]
