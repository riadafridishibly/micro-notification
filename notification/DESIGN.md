# Problem 1
The real challenge is making all the project parts work in unison. Docker made it lot easier. It starts fast! The host computer doesn't need to deal with all those dependency problems.

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
|---|---|---|
| 1 | 18595 | 25 |

Now the formula becomes,

```python
from datetime import datetime
# diff gives timedelta object
today_day_number = (datetime.today() - datetime(1970, 1, 1)).days

assigned_days -= (today_day_number - written_at)
```

If the `assigned_days` become negative or zero then the driver at **driver_id** has no day left.