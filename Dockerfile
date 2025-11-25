FROM python:3.11.3-alpine3.18

LABEL maintainer="faletacleison@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

# Instalar dependências do sistema
RUN apk add --no-cache \
    netcat-openbsd \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Criar virtualenv
RUN python -m venv /venv

# Criar usuário antes de dar chown
RUN adduser -D -H duser

# Copiar requirements
COPY djangoapp/requirements.txt /tmp/requirements.txt

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copiar app e scripts
COPY djangoapp /djangoapp
COPY scripts /scripts

# Criar estrutura de pastas e ajustar permissões
RUN mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /data && \
    chown -R duser:duser /djangoapp && \
    chown -R duser:duser /scripts && \
    chown -R duser:duser /venv && \
    chmod -R +x /scripts

USER duser

WORKDIR /djangoapp

EXPOSE 8000

CMD ["/scripts/commands.sh"]
