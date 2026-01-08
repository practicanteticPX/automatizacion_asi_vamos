FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpng-dev \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar worker
COPY worker.py .

# Hacer ejecutable
RUN chmod +x worker.py

# Punto de entrada
ENTRYPOINT ["python", "worker.py"]