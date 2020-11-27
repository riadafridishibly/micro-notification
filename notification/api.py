from app import create_app
from app import db
from app.models import Order


app = create_app()


@app.route('/')
def hello_world():
    return '<h1>Yep! Up and running...</h1>'


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order}


if __name__ == '__main__':
    # TODO: use gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
