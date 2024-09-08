from flask import Flask
from flask_cors import CORS

from apis.health_check import health_check
from apis.ask import ask_question

from constants import APP_PORT

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/health-check', methods=['GET'])
def health_check_get():
    return health_check()

@app.route("/ask", methods=["GET"])
def ask_get():
    return ask_question()


if __name__ == "__main__":
    app.run(debug=True, port=APP_PORT)
