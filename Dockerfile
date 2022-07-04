FROM alpine

RUN apk add python3-dev py3-pandas py3-numpy py3-pip py3-cryptography
RUN pip install mootdx pytest

