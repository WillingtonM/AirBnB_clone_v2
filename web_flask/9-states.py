#!/usr/bin/python3
"""
The Flask framework web application
Start the app and klistens on 0.0.0.0, port 5000

Routes: /
"""

import models
from models import storage
from flask import Flask, render_template

app = Flask("__name__")


@app.teardown_appcontext
def refresh(exception):
        """Remove current SQLAlchemy session."""
        storage.close()


@app.route("/states", strict_slashes=False)
def route_states():
        pep_fix = models.dummy_classes["State"]
        data_all = storage.all(cls=pep_fix)
        db_states = data_all.values()
        return render_template('7-states_list.html', states_list=db_states)


@app.route("/states/<id>", strict_slashes=False)
def route_city():
        pep_fix = models.dummy_classes["State"]
        data_all = storage.all(cls=pep_fix)
        db_states = data_all.values()
        return render_template('8-cities_by_states.html', states_list=db_states)


if __name__ == "__main__":
        app.run()
