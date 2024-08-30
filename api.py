from flask import Flask, request, jsonify

from constants import APP_PORT
from feed_or_search import search_index
from preprocess import preprocess_question

# Initialize Flask app
app = Flask(__name__)

@app.route('/health-check', methods=['GET'])
def health_check():
    """
    This function handles the '/health-check' endpoint, which accepts a GET request.
    It returns a JSON response indicating that the server is running and ready to answer questions.

    Returns:
    dict: A JSON response indicating the server's status.
    """
    return jsonify({"status": "Server is running."}), 200

@app.route("/ask", methods=["GET"])
def ask_question():
    """
    This function handles the '/ask' endpoint, which accepts a GET request with a 'question' parameter.
    It processes the question, searches for an answer in the index, and returns the question and answer as a JSON response.

    Parameters:
    question (str): The question to be asked. This is obtained from the 'question' parameter in the GET request.

    Returns:
    dict: A JSON response containing the question and answer. If no question is provided, an error message is returned.
    """
    question = request.args.get("question")
    print(">>> Question", question)
    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Preprocess the question
    processed_question = preprocess_question(question)
    print(">>> Processed question:", processed_question)

    # Search for the answer
    answer = search_index(processed_question)

    return jsonify({"question": question, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True, port=APP_PORT)
