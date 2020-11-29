# Problem 1
The real challenge is making all the project parts work in unison. Docker made it lot easier. It starts fast! The host computer doesn't need to deal with all those dependency problems.

Other than that, it's quite straight forward. We need an API where the user can call it with only a supply id which is in this case an integer (long). The user will call the API like this `http://some-ip:some-port/api/supply/<supply_id>`. Then the application will reply with a JSON. It'll have two field. In this case the **completion rate** and a **message**. There're fixed messages for this.

The application is implemented with [flask](https://flask.palletsprojects.com/en/1.1.x/). To provide a REST api for this application [Flask Restful](https://flask-restful.readthedocs.io/en/latest/) package is used.

Here's a top level overview:
- Client make a request.
- The application accept the request.
- It searches the database.
- Count the number of rides completed by the user.
- And finally returns message according to the given criteria.

The database currently has only one table. The model can be found in `app/models.py` file.


# Problem 2

There's no direct relation between remaining active days and completion rate. Because of the following scenario. If the assigned active days for the first case is **X** and for the next day even though the completion rate is same but the active days now become **(X - 1)**.

```
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1]  = Total Complete: 5    <- prev state
    1 < [1, 1, 0, 0, 0, 0, 0, 1, 1, 1]  = Total Complete: 5    <- curr state
    ^                               ^
    |                               |
poped item                     new inserted
```
To solve the problem we need another table with 3 columns.

| driver_id | written_at - days from a fixed day, ex: (1/1/1970) | assigned_days |
|:---:|:---:|:---:|
| 1 | 18595 | 25 |

Now the formula becomes,

```python
from datetime import datetime
# diff gives timedelta object
today_day_number = (datetime.today() - datetime(1970, 1, 1)).days

assigned_days -= (today_day_number - written_at)
```

If the `assigned_days` become negative or zero then the driver at **driver_id** has no day left.