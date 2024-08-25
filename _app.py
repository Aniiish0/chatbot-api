from flask import Flask, request, jsonify
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import spacy
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize spaCy for text preprocessing
nlp = spacy.load("en_core_web_sm")

# Define the schema for the knowledge base index
schema = Schema(question=TEXT(stored=True), answer=TEXT(stored=True))

# Create index directory if it doesn't exist
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

# Create or open the index
if not os.path.exists("indexdir/index"):
    ix = create_in("indexdir", schema)
else:
    ix = open_dir("indexdir")


# Function to add documents to the index
def add_to_index(entries):
    writer = ix.writer()
    for entry in entries:
        writer.add_document(question=entry["question"], answer=entry["answer"])
    writer.commit()


# Example knowledge base
knowledge_base = [
    {"question": "What is Flask?", "answer": "Flask is a lightweight WSGI web application framework in Python."},
    {"question": "What is an API endpoint?",
     "answer": "An API endpoint is a URL where an API can be accessed by a client."},
    {"question": "What is machine learning?",
     "answer": "Machine learning models are algorithms that learn from data to make predictions or decisions."}
]

# Index the knowledge base
add_to_index(knowledge_base)


# Function to preprocess the question using spaCy
def preprocess_question(question):
    doc = nlp(question)
    return " ".join([token.lemma_ for token in doc if not token.is_stop])


# Function to search the index
def search_index(query):
    with ix.searcher() as searcher:
        query = QueryParser("question", ix.schema).parse(query)

        print(">>> Query:", query)

        results = searcher.search(query)

        print(">>> Results:", results)

        if results:
            return results[0]["answer"]
        else:
            return "Sorry, I couldn't find an answer to your question."


@app.route('/ask', methods=['GET'])
def ask_question():
    question = request.args.get('question')
    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Preprocess the question
    processed_question = preprocess_question(question)

    print(">>> Processed question:", processed_question)

    # Search for the answer
    answer = search_index(processed_question)

    return jsonify({"question": question, "answer": answer})


if __name__ == '__main__':
    app.run(debug=True, port=3001)