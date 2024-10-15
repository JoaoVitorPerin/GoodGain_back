# STAGE 1: Build
FROM python:3.12-slim AS build

# Diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copia os arquivos de dependências (requirements.txt)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# STAGE 2: Run
FROM python:3.12-slim

# Define o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copia as dependências instaladas na fase de build
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copia o código da aplicação para o contêiner
COPY . .

# Variáveis de ambiente necessárias para o Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Exemplo de configuração para usar PostgreSQL (ajustar conforme necessário)
ENV DB_HOST=aws-0-sa-east-1.pooler.supabase.com
ENV DB_NAME=postgres
ENV DB_USER=postgres.yplatbhotdufskjaiich
ENV DB_PASSWORD=vUsNlDt6tWxrBXt3
ENV DB_PORT=6543
# Expor a porta 8000 (padrão do Django)
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
