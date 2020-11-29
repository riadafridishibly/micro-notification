#!/usr/bin/env bash
flask db upgrade
gunicorn --bind 0.0.0.0:5000 --workers 4 api:app