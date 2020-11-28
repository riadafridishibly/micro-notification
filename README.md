# Notification Service

## How to run!
Run the following first.
```sh
docker-compose up
```

We need to apply the migrations for the first time. To do this run the following while the previous command completed.

```sh
docker-compose exec notification-service flask db upgrade
```

Now you're good to go.

## Running the test

Run this command first,
```sh
docker-compose up
```
Then
```sh
docker-compose exec notification-service pytest -v tests/
```