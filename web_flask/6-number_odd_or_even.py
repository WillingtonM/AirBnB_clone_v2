#!/usr/bin/python3
"""
The Flask framework web application
Start the app and klistens on 0.0.0.0, port 5000

Routes: /
        /hbnb
        /c/<text>
        /python/(<text>
        /number
        /number_template
        /number_odd_or_even
"""
from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """Returns/Displays hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNB():
    """Returns/Displays HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def text(text):
    """Returns/Displays text given"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python/', defaults={'text': 'is_cool'})
@app.route('/python/<text>', strict_slashes=False)
def display(text):
    """Display “Python” followed by the value of the <text>"""
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def num_display(n):
    """Display “n is a number” only if integer"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_html(n):
    """display HTML is "n" is a number only"""
    return render_template('5-number.html', name=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def num_html_even_odd(n):
    """Displays an HTML page only if <n> is even|odd."""
    return render_template('6-number_odd_or_even.html', name=n)


if __name__ == "__main__":
    app.run()
