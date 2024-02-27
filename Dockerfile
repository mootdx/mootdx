ARG PYTHON_VERSION=3.8-slim

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
# RUN apk add openssl-dev make autoconf automake gcc g++ zlib-dev linux-headers git libffi-dev libevent

COPY ./requirements.txt .
COPY ./tests/requirements.txt ./requirements.dev

# Create Python Dependency and Sub-Dependency Wheels.
#  py3-pandas py3-numpy py3-click py3-schedule
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt -r requirements.dev
# RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.dev -i https://mirrors.ustc.edu.cn/pypi/web/simple
# RUN pip wheel --wheel-dir /usr/src/app/wheels -i https://mirrors.ustc.edu.cn/pypi/web/simple 'mootdx[all]'
RUN rm -rf /usr/src/app/wheels/setuptools*

RUN pip install 'mootdx[cli]'
RUN mootdx bestip -v

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
# RUN apk add --no-cache zlib-dev bash

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/
COPY --from=python-build-stage /root/.mootdx/config.json  /root/.mootdx/config.json

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels/
RUN pip install --no-cache-dir poetry
