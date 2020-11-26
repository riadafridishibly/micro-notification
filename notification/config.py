import os


class Config:
    """
    Default configuration for the application
    """
    APP_NAME = 'notification'
    # SECRET_KEY = '!very-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL',
            'mysql+pymysql://root:password@localhost:3306/test'
        )
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

del os