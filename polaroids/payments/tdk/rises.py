import logging

import dotenv

from flask import Flask
from polaroids.payments.tdk import prime


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

app = Flask(__name__)

logger.info("NEW INSTANCE is created")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return path


app.add_url_rule("/payments", methods=["POST"], view_func=prime.payment)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)

app = Flask(__name__)

