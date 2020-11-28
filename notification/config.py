import os

DB_BASE_URI = 'mysql+pymysql://root:password@db:3306'
DB_NAME = 'mydb'


class Config:
    """
    Default configuration for the application
    """
    APP_NAME = 'notification'
    # SECRET_KEY = '!very-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        DB_BASE_URI + '/' + DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


del os
