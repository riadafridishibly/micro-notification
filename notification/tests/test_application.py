from app.models import Order
from app import create_app, db
import sqlalchemy
import os
import flask_migrate
import flask_restful
import pytest

# ----------------- DATA BASE URI ----------------------
DB_BASE_URI = 'mysql+pymysql://root:password@db:3306'
DB_NAME = 'test2'


# ----------------- TEST CONFIG ------------------------
class TestConfig:
    """
    Test configuration for the application
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        DB_BASE_URI + '/' + DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# ----------------- DATABASE SPECIFIC -------------------

def test_db_connection():
    engine = sqlalchemy.create_engine(DB_BASE_URI)
    try:
        engine.connect()
    except sqlalchemy.exc.OperationalError:
        pytest.fail('DB connection failed')

# ------------------ HELPER FUNCTIONS -------------------


@pytest.fixture
def cursor():
    engine = sqlalchemy.create_engine(DB_BASE_URI)
    conn = engine.connect()
    yield conn
    # finally drop the db
    drop_db(conn)
    conn.close()


def drop_db(cursor):
    cursor.execute(f'DROP DATABASE IF EXISTS {DB_NAME};')


def create_db(cursor):
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME};')
    cursor.execute(f'USE {DB_NAME}')


def drop_and_create(cursor):
    drop_db(cursor)
    create_db(cursor)


def get_db_list(cursor):
    res = cursor.execute('SHOW DATABASES;')
    databases = {d[0] for d in res}
    return databases

# ---------------------- TESTS ----------------------
# ------------- DATABASE SPECIFIC TESTS -------------


def test_db_not_in_server(cursor):
    """Checks no database named `DB_NAME` in server
    """
    drop_db(cursor)
    databases = get_db_list(cursor)
    assert DB_NAME not in databases


def test_db_created(cursor):
    """Create database in server
    """
    drop_and_create(cursor)
    databases = get_db_list(cursor)
    return DB_NAME in databases


def test_db_migration(cursor):
    drop_and_create(cursor)

    app = create_app(TestConfig)
    with app.app_context():
        flask_migrate.upgrade()

    res = cursor.execute('SHOW TABLES;')
    tables = {t[0] for t in res}
    assert 'order' in tables


def test_db_insert(cursor):
    drop_and_create(cursor)
    app = create_app(TestConfig)

    with app.app_context():
        flask_migrate.upgrade()
        o = Order(id=0, supply_id=1, order_id='ABCD', status=False)
        db.session.add(o)
        db.session.commit()
        res = Order.query.all()

    assert len(res) == 1 and res[0].order_id == 'ABCD'


# ------------- APPLICATION SPECIFIC TESTS -------------

def test_api_get_req(cursor):
    drop_and_create(cursor)

    app = create_app(TestConfig)
    api = flask_restful.Api(app)

    from api import NotificationAPI

    api.add_resource(NotificationAPI, '/api/supply/<int:supply_id>')

    with app.test_client() as client:
        with app.app_context():
            # populate db
            flask_migrate.upgrade()
            o = Order(id=0, supply_id=1, order_id='ABCD', status=False)
            db.session.add(o)
            db.session.commit()
        resp = client.get('/api/supply/1')

    assert resp.status_code == 200 and resp.json['completion_rate'] == 0.85
