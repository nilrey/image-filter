# Dockerfile
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка Python зависимостей
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install clearml-agent
RUN clearml-agent --version

# Рабочая директория
WORKDIR /workspace

# Копирование скриптов
COPY . /workspace/

ENTRYPOINT ["clearml-agent", "execute"]

CMD ["--id"]