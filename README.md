# Notification Service

## IMPORTANT
In `db/init.sql` file the the first line is `DROP DATABASE IF EXISTS test;`. Which will remove database every time the container is built. Comment this if you don't want a fresh start every time.


## How to run!
Run the following command.
```sh
docker-compose up
```

But currently the database is empty. To insert some data you can run `populate_db.py` and currently it requires `urllib3`. It'll add some data to the database by using a development api.

Now you're good to go.

## Showing Result
Using [http](https://httpie.io/) it's easy to send request and see response.

```sh
$ http GET localhost:5000/api/supply/1
HTTP/1.0 200 OK
Content-Length: 93
Content-Type: application/json
Date: Sat, 28 Nov 2020 19:23:57 GMT
Server: Werkzeug/1.0.1 Python/3.9.0

{
    "completion_rate": 0.85,
    "message": "Please complete more to get more requests."
}
```


## Using development API
Getting all values that has specific **supply id**.
```sh
$ http GET localhost:5000/api/dev/supply/1
HTTP/1.0 200 OK
Content-Length: 619
Content-Type: application/json
Date: Sat, 28 Nov 2020 19:25:11 GMT
Server: Werkzeug/1.0.1 Python/3.9.0

[
    {
        "id": 1,
        "order_id": "AAAA",
        "status": true,
        "supply_id": 1,
        "timestamp": "Thu Nov 26 19:22:10 2020"
    },
    {
        "id": 2,
        "order_id": "BBBB",
        "status": true,
        "supply_id": 1,
        "timestamp": "Wed Nov 25 19:22:10 2020"
    },
    {
        "id": 3,
        "order_id": "CCCC",
        "status": true,
        "supply_id": 1,
        "timestamp": "Tue Nov 24 19:22:10 2020"
    },
    {
        "id": 4,
        "order_id": "DDDD",
        "status": true,
        "supply_id": 1,
        "timestamp": "Mon Nov 23 19:22:10 2020"
    }
]

```

## Running the test

Run this command first,
```sh
docker-compose up
```
Then
```sh
docker-compose exec notification-service pytest -v tests/
```