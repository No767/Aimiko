####################################################################################################
## Builder image
####################################################################################################
FROM python:3.11-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Aimiko

COPY /pyproject.toml /Aimiko/
COPY /poetry.lock /Aimiko/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

####################################################################################################
## Final image
####################################################################################################
FROM python:3.11-slim-bookworm

RUN apt update \
  && apt install -y --no-install-recommends \
  tini \
  bash \
  netcat-traditional \
  libopus-dev \
  libffi-dev \
  libsodium-dev \
  git

WORKDIR /Aimiko
COPY /bot/aimikobot.py /Aimiko/bot/
COPY /bot/aimikocore.py /Aimiko/bot/
# COPY /Migrations /Aimiko/migrations
COPY /bot/cogs /Aimiko/bot/cogs
COPY /bot/libs /Aimiko/bot/libs/
# COPY /migrations-runner.py /Aimiko/migrations-runner.py
COPY /docker/start.sh /Aimiko/start.sh
COPY /docker/wait-for /Aimiko/wait-for

COPY --from=builder /Aimiko/requirements.txt /Aimiko/requirements.txt

RUN adduser --disabled-password --gecos "" aimiko \
  && chown -R aimiko:aimiko /Aimiko \
  && chmod +x /Aimiko/start.sh \
  && chmod +x /Aimiko/wait-for

USER aimiko

ENV PATH="${PATH}:/home/aimiko/.local/bin"

RUN pip install --user -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/Aimiko/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Aimiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built for the Trans Gayming community"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Aimiko"
