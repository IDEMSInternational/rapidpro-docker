# RapidPro in Docker

## Getting started

Prepare the dot env file and provide missing values.
```
cp env.example .env
```

Start supporting services.
```
docker compose up -d dynamo elastic minio postgres valkey
```

Run database migration on relational database.
```
docker compose run --rm rapidpro python manage.py migrate --no-input
```

Run database migration on DynamoDB.
```
docker compose run --rm rapidpro python manage.py migrate_dynamo
```

Start courier, mailroom and rapidpro.
```
docker compose up -d courier mailroom rapidpro
```

Start everything else.
```
docker compose up -d
```

Copy static files for RapidPro web UI, making them available to the proxy.
```
docker compose exec rapidpro cp -aT /rapidpro/sitestatic /opt/idems/static
```
