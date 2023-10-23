#!/usr/bin/python3
"""
The Flask framework web application
Start the app and klistens on 0.0.0.0, port 5000

Routes: /hbnb
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays the main HBnB filters HTML page."""
    db_states = storage.all("State")
    db_amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html",
                           states=db_states, amenities=db_amenities, places=places)


@app.teardown_appcontext
def teardown(exc):
    """Remove current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
