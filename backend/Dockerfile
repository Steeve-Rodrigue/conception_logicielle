# ---------- Builder ----------
FROM ghcr.io/astral-sh/uv:python3.13-trixie AS builder
WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

# ---------- Runtime ----------
FROM ghcr.io/astral-sh/uv:python3.13-trixie
WORKDIR /code
COPY --from=builder /build/.venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY src/ ./src/
COPY data/ ./data/
CMD ["python", "-m", "src.api"]