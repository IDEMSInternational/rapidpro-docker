FROM python:3.12-trixie AS builder

ARG RAPIDPRO_TAG
ENV RAPIDPRO_TAG=${RAPIDPRO_TAG:-main}

RUN apt-get update && apt-get install --yes --no-install-recommends libgdal36 nodejs npm
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/rapidpro/.venv/bin:/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN npm install -g n && n 20
RUN npm install -g yarn less

WORKDIR /rapidpro
RUN wget -O - "https://github.com/nyaruka/rapidpro/archive/${RAPIDPRO_TAG}.tar.gz" | tar -xzf - --strip-components=1
# Overwrite API files
COPY ./views.py /rapidpro/temba/api/v2/views.py
COPY ./fields.py /rapidpro/temba/api/v2/fields.py
COPY ./urls.py /rapidpro/temba/api/v2/urls.py
COPY ./serializers.py /rapidpro/temba/api/v2/serializers.py
RUN poetry install --no-root
RUN yarn install
COPY ./middleware.py /rapidpro/idems/
COPY ./settings.py /rapidpro/temba/
RUN python manage.py collectstatic --no-input

FROM python:3.12-slim-trixie
EXPOSE 8000
ENV PORT=8000 \
    PATH="/rapidpro/.venv/bin:$PATH"
RUN apt-get update && apt-get install --yes --no-install-recommends \
      ffmpeg \
      libgdal36 \
      libmagic1t64 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /rapidpro
COPY --from=builder /rapidpro /rapidpro
CMD ["gunicorn", "temba.wsgi:application"]
