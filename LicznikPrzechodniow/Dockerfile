FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HOME=/tmp

WORKDIR /app

# OpenCV imports these libraries even when the preview is disabled.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.docker.txt ./
RUN python -m pip install --no-cache-dir -r requirements.docker.txt

COPY main.py ./

ENTRYPOINT ["python", "main.py", "--backend", "any", "--no-display"]
CMD ["--help"]
