# Use Python 3.11 slim image (compatible with Render's platform)
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
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
# bot.py will automatically detect and use Render's PORT environment variable
# Use shell form to ensure environment variables are passed through
CMD sh -c 'uv run bot.py --host 0.0.0.0'
