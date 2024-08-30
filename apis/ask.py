from flask import request, jsonify

from helpers.feed_or_search import search_index
from helpers.preprocess import preprocess_question


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