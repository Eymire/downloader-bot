FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/

RUN apt update \
    && apt install -y --no-install-recommends ffmpeg \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY /src/ ./

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "entrypoint.sh" ]

CMD [ "uv", "run", "main.py" ]
