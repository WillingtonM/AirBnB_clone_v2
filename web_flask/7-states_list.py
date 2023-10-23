#!/usr/bin/python3
"""
The Flask framework web application
Start the app and klistens on 0.0.0.0, port 5000

Routes: /states_list
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """ Remove current SQLAlchemy session"""
    if storage is not None:
        storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays HTML page with list of all State objects in DBStorage"""
    db_data = storage.all(State)
    return render_template('7-states_list.html', total=db_data.values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
