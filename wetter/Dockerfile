# syntax=docker/dockerfile:1.4
# FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
FROM python:3.12.2-slim as builder

WORKDIR /GIREA

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /GIREA
RUN --mount=type=cache,target=/root/.cache/pip \
    # pip3 install --upgrade pip \
    pip3 install -r requirements.txt

COPY . /GIREA

ENTRYPOINT ["python3"]
CMD ["main.py"]

# FROM builder as dev-envs
FROM python:3.12.2-slim

# RUN <<EOF
# apk update
# apk add git
# EOF

# RUN <<EOF
# addgroup -S docker
# adduser -S --shell /bin/bash --ingroup docker vscode
# EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
