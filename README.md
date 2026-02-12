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

Create storage buckets.
```
docker compose exec minio bash -eu -c 'mc alias set local http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD; readarray -d "," -t BUCKETS <<< ${DEFAULT_BUCKETS}; for b in ${BUCKETS[@]}; do mc mb -p local/${b}; done'
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

In a web browser, visit https://localhost/accounts/signup/ and sign up. The verification email should be delivered to mailpit - the inbox is accessible via https://localhost:8025/ . Click on the confirmation link in the email to finish the sign up process.

## Stopping and starting

After completing the first-time setup described above, it should be possible to stop all services at once with:
```
docker compose down
```

To start all services again:
```
docker compose up -d
```
