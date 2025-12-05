FROM dailyco/pipecat-base:latest

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
# The bot.py will automatically use PORT env var if provided by Render
CMD ["uv", "run", "bot.py", "--host", "0.0.0.0", "--port", "7860"]
