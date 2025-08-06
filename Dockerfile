# → Base Python 3.12 slim (Debian Bookworm)
FROM python:3.12-slim-bookworm

# Créer un utilisateur non-root
RUN useradd wagtail

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

# Installer paquets système (build C, Python headers, Postgres, JPEG, Zlib, WebP, HEIF, CFFI)
RUN apt-get update --yes --quiet \
 && apt-get install --yes --quiet --no-install-recommends \
      build-essential \
      python3-dev \
      libffi-dev \
      pkg-config \
      libpq-dev \
      libjpeg62-turbo-dev \
      zlib1g-dev \
      libwebp-dev \
      libheif-dev \
      libde265-dev \
      libx265-dev \
      libaom-dev \
 && rm -rf /var/lib/apt/lists/*

# Installer Gunicorn
RUN pip install --no-cache-dir "gunicorn==20.0.4"

# Copier et installer les dépendances Python
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source et passer en non-root
COPY --chown=wagtail:wagtail . .
USER wagtail

# Collectstatic puis démarrage
RUN python manage.py collectstatic --noinput --clear
CMD set -xe \
 && python manage.py migrate --noinput \
 && gunicorn formation_wushu.wsgi:application
