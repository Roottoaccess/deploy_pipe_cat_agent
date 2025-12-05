# Use Python 3.11 slim image (compatible with Render's platform)
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv - download and extract, find binary regardless of directory structure
RUN cd /tmp && \
    curl -LsSf https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz -o uv.tar.gz && \
    tar -xzf uv.tar.gz && \
    find . -name "uv" -type f -executable -exec mv {} /usr/local/bin/uv \; && \
    chmod +x /usr/local/bin/uv && \
    rm -rf /tmp/uv* /tmp/*.tar.gz

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Set working directory
WORKDIR /app

# Copy the application code and project config
COPY ./bot.py bot.py
COPY ./pyproject.toml pyproject.toml

# Expose the port the bot runs on (default 7860, Render will override with PORT env var)
EXPOSE 7860

# Run the bot using uv
# Use shell form to interpolate PORT env var (Render provides this)
# Default to 7860 if PORT is not set (for local development)
CMD sh -c 'uv run bot.py --host 0.0.0.0 --port ${PORT:-7860}'
