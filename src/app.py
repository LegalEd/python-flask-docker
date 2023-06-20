import csv
import random

from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@app.route("/")
def index():
    return render_template("index.html")


@sock.route("/echo")
def echo(sock):
    while True:
        data = sock.receive()
        sock.send(data)


@app.route("/random_joke")
def random_joke():
    with open("src/jokes.csv", "r") as file:
        reader = csv.reader(file)
        jokes = list(reader)
        random_joke = random.choice(jokes)[0]
    return random_joke

  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

