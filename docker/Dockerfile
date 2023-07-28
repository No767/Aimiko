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

WORKDIR /Aiko

COPY /pyproject.toml /Aiko/
COPY /poetry.lock /Aiko/

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

WORKDIR /Aiko
COPY /bot/aikobot.py /Aiko/bot/
COPY /bot/aikocore.py /Aiko/bot/
# COPY /Migrations /Aiko/Migrations
COPY /bot/cogs /Aiko/bot/cogs
COPY /bot/libs /Aiko/bot/libs/
# COPY /migrations-runner.py /Aiko/migrations-runner.py
COPY /docker/start.sh /Aiko/start.sh
COPY /docker/wait-for /Aiko/wait-for

COPY --from=builder /Aiko/requirements.txt /Aiko/requirements.txt

RUN adduser --disabled-password --gecos "" aiko \
  && chown -R aiko:aiko /Aiko \
  && chmod +x /Aiko/start.sh \
  && chmod +x /Aiko/wait-for

USER aiko

ENV PATH="${PATH}:/home/aiko/.local/bin"

RUN pip install --user -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/Aiko/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Aiko"
LABEL org.opencontainers.image.description="A multipurpose Discord bot built for the Trans Gayming community"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Aiko"
