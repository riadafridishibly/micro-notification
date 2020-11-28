# This script adds entries to database.
# just for TESTING purpose

import json
import urllib3
from datetime import datetime, timedelta

REQ_URL = 'http://localhost:5000/api/dev/supply/1'
REQ_METHOD = 'POST'


def post(supply_id: int, order_id: str,
         status: bool, timestamp: 'datetime.timestamp'):
    encoded_body = json.dumps({
        'supply_id': supply_id,
        'order_id': order_id,
        'status': status,
        'timestamp': timestamp,
    })

    http = urllib3.PoolManager()

    r = http.request(
        'POST',
        REQ_URL,
        headers={'Content-Type': 'application/json'},
        body=encoded_body)

    print(r.data)


post(1, 'AAAA', True, (datetime.now() - timedelta(days=2)).timestamp())
post(1, 'BBBB', True, (datetime.now() - timedelta(days=3)).timestamp())
post(1, 'CCCC', True, (datetime.now() - timedelta(days=4)).timestamp())
post(1, 'DDDD', True, (datetime.now() - timedelta(days=5)).timestamp())
