from flask import Flask
import threading
app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'<h1>Yep! Up and running... {threading.current_thread().name}</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
