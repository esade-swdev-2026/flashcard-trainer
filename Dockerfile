FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /bin/uv
RUN useradd --create-home app && mkdir -p /app/data && chown app:app /app/data

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md LICENSE ./
COPY src ./src
RUN uv sync --locked --no-dev

USER app
WORKDIR /app/data
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["flashcard-trainer"]
CMD ["--help"]