FROM python:3.9-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=api.py
ENV PYTHONPATH=/usr/src/app

CMD ["python", "api.py"]
