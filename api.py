from flask import Flask, request, jsonify

from feed_or_search import search_index
from preprocess import preprocess_question

# Initialize Flask app
app = Flask(__name__)


@app.route("/ask", methods=["GET"])
def ask_question():
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
    app.run(debug=True, port=3000)
