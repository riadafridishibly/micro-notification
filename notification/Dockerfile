FROM python:3.9-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

ENTRYPOINT ["sh", "./entrypoint.sh"]