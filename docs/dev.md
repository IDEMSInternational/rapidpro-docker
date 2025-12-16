# Set up a development environment

The instructions below will help to set up a container image with development tools and other dependencies that can be used to develop the Rapidpro web application. The idea is to run the tools within the container, but keep the source code on the host file system (though mounted on the container).

Copy the example '.env'.
```
cp env.example .env
```

Copy the development override configuration.
```
cp docker-compose.dev.yml docker-compose.override.yml
```

Build the development-focused container image.
```
docker compose build rapidpro
```

Start a bash shell in the RapidPro container and install dependencies.
```
docker compose run --rm rapidpro bash -c 'poetry install && yarn install'
```

Start the database.
```
docker compose up -d postgres
```

Run the database migration.
```
docker compose run --rm rapidpro poetry run python manage.py migrate
```

Generate static assets (JS, CSS, etc).
```
docker compose run --rm poetry run python manage.py collectstatic
```

Start the server.
```
docker compose up -d rapidpro
```

Sign-up requires the key-value store and an SMTP server to receive notification emails. Start up Valkey and Mailpit.
```
docker compose up -d valkey mail
```
