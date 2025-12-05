# Use Python 3.11 slim image (compatible with Render's platform)
FROM python:3.11-slim

# Install system dependencies (minimal - no OpenGL needed for LiveKit)
# Add ffmpeg for audio processing (fixes pydub warning)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg \
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

# Set working directory first
WORKDIR /app

# Copy project files first (needed for uv sync)
COPY ./pyproject.toml pyproject.toml
COPY ./uv.lock uv.lock

# Install dependencies using the lockfile (creates venv at .venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# Copy the application code
COPY ./main.py main.py
COPY ./agent.py agent.py
COPY ./static ./static

# Expose the port the server runs on (default 7860, Render will override with PORT env var)
EXPOSE 7860

# Run the FastAPI server using uv run (automatically uses the virtual environment)
# Use shell form to ensure environment variables are passed through
CMD sh -c 'uv run main.py'
