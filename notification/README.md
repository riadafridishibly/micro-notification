## Dealing with Time
DateTime is stored in UTC. We need to exclude today from the query. So what is essentially done is created a datetime object at the beginning of a day.

```python
from datetime import datetime
start_of_the_day = datetime.combine(datetime.utcnow(), datetime.min.time())
```
Any date less than `start_of_the_day` is considered **not today**. I might be wrong. But this is the current IDEA.


## How to deal with `Not Found`?
The following lookup should be happened in another table to check whether the driver exists with the particular id.

```python
query = Order.query.filter(Order.supply_id == supply_id).count()
if query == 0:
    return {'status': 'Not Found'}, 404
```

## Check if the driver was assigned to at least 100 rides
I think there's a better way to do this. What if we keep a counter!

```python
query = Order.query.filter(Order.supply_id == supply_id)\
    .order_by(Order.timestamp.desc())\
    .filter(Order.timestamp < start_of_current_day)\
    .count()

if query < 100:
    # if the driver yet to be assigned 100 rides,
    # then the completion rate 0.85
    return notify_dict(85)
```

## Final Query
```python

query = Order.query.filter(Order.supply_id == supply_id)\
    .order_by(Order.timestamp.desc())\
    .filter(Order.timestamp < start_of_current_day)\
    .limit(100)\
    .from_self()\
    .filter(Order.status == COMPLETED)\
    .count()
```


## Query Optimization
I don't think the query used here is anywhere near optimized. Complicated counter may solve the problem! But before measuring performance I don't think it's a good idea to optimize.
