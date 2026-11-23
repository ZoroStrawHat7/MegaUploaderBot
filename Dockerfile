FROM python:3.11-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATA_DIR=/data

RUN apt-get update && apt-get install -y --no-install-recommends \
    megatools ffmpeg ca-certificates gcc python3-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p /data/downloads

CMD ["python", "start.py"]
