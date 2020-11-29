# Notification Service

## IMPORTANT
In `db/init.sql` file the the first line is `DROP DATABASE IF EXISTS mydb;`. Which will remove `mydb` database every time the container is built. Comment this out if you don't want a fresh start every time.

## Attached Files

- [DESIGN.md](./notification/DESIGN.md)
- [Dealing Wih Time And Query](./notification/README.md)

## How to run!
For the first time **database** need to be initialized first. To do this run,

```sh
docker-compose up db
```

When the initialization is done, stop the process with (`CTRL-C`) and then run the following command.
```sh
docker-compose up
```

The issue with `database` init can be solved by a `wait-for-it.sh` script.

Currently the database is empty. To insert some data you can run `populate_db.py` and currently it requires `urllib3`. It'll add some data to the database by using a development api.

Now you're good to go.

## Showing Result
Using [http](https://httpie.io/) it's easy to send request and see response.

```sh
$ http GET localhost:5000/api/supply/1
HTTP/1.1 200 OK
Connection: close
Content-Length: 93
Content-Type: application/json
Date: Sun, 29 Nov 2020 08:25:01 GMT
Server: gunicorn/20.0.4

{
    "completion_rate": 0.85,
    "message": "Please complete more to get more requests."
}

```


## Using development API
Getting all values that has specific **supply id**.
```sh
$ http GET localhost:5000/api/dev/supply/1
HTTP/1.1 200 OK
Connection: close
Content-Length: 619
Content-Type: application/json
Date: Sun, 29 Nov 2020 07:44:27 GMT
Server: gunicorn/20.0.4

[
    {
        "id": 1,
        "order_id": "AAAA",
        "status": true,
        "supply_id": 1,
        "timestamp": "Fri Nov 27 07:44:02 2020"
    },
    {
        "id": 2,
        "order_id": "BBBB",
        "status": true,
        "supply_id": 1,
        "timestamp": "Thu Nov 26 07:44:02 2020"
    },
    {
        "id": 3,
        "order_id": "CCCC",
        "status": true,
        "supply_id": 1,
        "timestamp": "Wed Nov 25 07:44:02 2020"
    },
    {
        "id": 4,
        "order_id": "DDDD",
        "status": true,
        "supply_id": 1,
        "timestamp": "Tue Nov 24 07:44:02 2020"
    }
]

```

## Running the test

If the database is not initialized, then follow the [How To Run](#how-to-run). Then run this,

```sh
docker-compose up
```
Run the tests
```sh
docker-compose exec notification-service pytest -v tests/
```