FROM python:3.14-trixie AS builder

ARG RAPIDPRO_TAG
ENV RAPIDPRO_TAG=${RAPIDPRO_TAG:-main}

RUN apt-get update && apt-get install --yes --no-install-recommends libgdal36 nodejs npm
RUN pip install --no-cache-dir uv
ENV PATH="/rapidpro/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
RUN npm install -g n && n 20
RUN npm install -g yarn less

WORKDIR /rapidpro
RUN wget -O - "https://github.com/nyaruka/rapidpro/archive/${RAPIDPRO_TAG}.tar.gz" | tar -xzf - --strip-components=1
RUN uv sync --frozen --no-dev --no-install-project
# regex is imported by temba but only declared transitively via a dev dependency, so install the locked version
RUN uv pip install "regex==$(grep -A1 '^name = "regex"$' uv.lock | sed -n 's/^version = "\(.*\)"$/\1/p')"
RUN yarn install
COPY ./contact_delete.py ./middleware.py /rapidpro/idems/
COPY ./settings.py /rapidpro/temba/
RUN python manage.py collectstatic --no-input

FROM python:3.14-slim-trixie
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
