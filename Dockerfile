# Dockerfile
FROM python:3.11-slim

# Установка системных зависимостей (однократно)
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка Python зависимостей (однократно)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Рабочая директория
WORKDIR /workspace

# Копирование скриптов (опционально)
COPY . /workspace/

# Команда по умолчанию будет переопределяться ClearML
CMD ["python"]