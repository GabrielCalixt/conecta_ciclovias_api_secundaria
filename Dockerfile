# Imagem base: Python 3.14 (mesma versão do ambiente de desenvolvimento), variante slim (menor)
FROM python:3.14-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia primeiro só o requirements.txt: se ele não mudar, o Docker reaproveita
# a camada de instalação e o build fica muito mais rápido
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Porta em que a API secundária escuta
EXPOSE 8000

# 0.0.0.0 é obrigatório: faz a API aceitar conexões vindas de fora do container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
