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

Copy static files for RapidPro web UI, making them available to the proxy.
```
docker compose exec rapidpro cp -aT /rapidpro/sitestatic /opt/idems/static
```

Start everything else.
```
docker compose up -d
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

## Removing contacts

A script for deleting contacts and all data related to them is included here. For the script to work, the following conditions must be met:

- A contact group called "deletion request" must exist
- A contact field called "deletion request time" of type "Date & Time" must exist

The script will look for all active contact groups, with the name above, across all workspaces. Before deleting any contacts who are members of these groups, the script will extract the value of the "deletion request time" field for each contact, for reporting purposes.

A report, in CSV format, will output to stdout, example below.

```
Workspace,Anonomous UUID,Request Type,Request Received,Request Completion,Related emails deleted,Partners notified of dataset update
Company,2fcf265b-9f57-4fa5-8b07-5a52908c73c5,Deletion,2026-04-29T20:26:00+00:00,2026-04-29T20:36:16.450741,N/A,Pending
```

The recommended way to run the script is given below.

```
cat rapidpro/contact_delete.py | docker compose exec -T rapidpro python manage.py shell
```

A dry run can be achieved by commenting the line that performs the deletion i.e., `contact.release(...)`.
