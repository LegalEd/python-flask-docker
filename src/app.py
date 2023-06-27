import csv
import random
from flask import current_app
import json
from jsonschema import validate

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


# {
#     "id": "4376c65d2f232afbe9b882a35baa4f6fe8667c4e684749af565f981833ed6a65",
#     "pubkey": "6e468422dfb74a5738702a8823b9b28168abab8655faacb6853cd0ee15deee93",
#     "created_at": 1673347337,
#     "kind": 1,
#     "tags": [
#         ["e", "3da979448d9ba263864c4d6f14984c423a3838364ec255f03c7904b1ae77f206"],
#         ["p", "bf2376e17ba4ec269d10fcc996a4746b451152be9031fa48e74553dde5526bce"]
#     ],
#     "content": "Walled gardens became prisons, and nostr is the first step towards tearing down the prison walls.",
#     "sig": "908a15e46fb4d8675bab026fc230a0e3542bfade63da02d542fb78b2a8513fcd0092619a2c8c1221e581946e0191f2af505dfdf8657a414dbca329186f009262"
# }

json_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "pubkey": {"type": "string"},
        "created_at": {"type": "number"},
        "kind": {"type": "number"},
        "tags": {"type": "array"},
        "content": {"type": "string"},
        "sig": {"type": "string"},
    }
}


@sock.route("/nostr")
def nostr(sock):
    while True:
        data = sock.receive()
        try:
            json_data = json.loads(data)
            # raise error if invalid
            validate(instance=json_data, schema=json_schema)
            sock.send(json_data)

        except Exception as e:
            sock.send(f"error {e}")
            current_app.logger.info(f"error: {e}")


@app.route("/random_joke")
def random_joke():

    with open("/app/src/jokes.csv", "r") as file:
        reader = csv.reader(file)
        jokes = list(reader)
        random_joke = random.choice(jokes)[0]
    return random_joke


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
