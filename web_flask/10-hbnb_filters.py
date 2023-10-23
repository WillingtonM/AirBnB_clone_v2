#!/usr/bin/python3
"""
The Flask framework web application
Start the app and klistens on 0.0.0.0, port 5000

Routes: /hbnb_filters
"""

from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays main HBnB filters HTML page."""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """Remove current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")