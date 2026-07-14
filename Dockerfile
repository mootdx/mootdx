ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION} AS builder
WORKDIR /build
COPY pyproject.toml README.md LICENSE ./
COPY mootdx ./mootdx
RUN python -m pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:${PYTHON_VERSION}
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels
ENTRYPOINT ["mootdx"]
CMD ["--help"]
