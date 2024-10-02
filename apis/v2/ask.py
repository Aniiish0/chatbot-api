from flask import request, jsonify
from scipy.spatial.distance import cosine
import ollama
import json
from sentence_transformers import SentenceTransformer
import os
import logging

# Disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load the knowledge base
def load_knowledge_base():
    try:
        with open("knowledge_base.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Knowledge base not found.")
        return []


# Function to generate embeddings for each question in the knowledge base
def generate_embeddings_for_questions():
    for item in knowledge_base:
        item["embedding"] = model.encode(item["question"])


# Load knowledge base and generate embeddings
knowledge_base = load_knowledge_base()
generate_embeddings_for_questions()


# Semantic search function (using cosine similarity)
def find_similar_question(question):
    question_embedding = model.encode(question)

    closest_question = None
    highest_similarity = -1

    for item in knowledge_base:
        similarity = 1 - cosine(question_embedding, item["embedding"])
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_question = item

    # Only return the closest match if it exceeds the similarity threshold
    return closest_question if highest_similarity > 0.8 else None

def ask():
    data = request.args
    question = data.get("question")
    fallback = data.get("fallback")
    if not question:
        return jsonify({"error": "No question provided."}), 400

    # First, try to find a semantically similar question in the knowledge base
    similar_question = find_similar_question(str(question))

    if similar_question:
        return jsonify(
            {
                "question": question,
                "answer": similar_question["answer"],
            }
        )

    if fallback and str(fallback).upper() == "LLM":
        # If no similar question is found, query the Ollama model
        ollama_answer = query_ollama(question)
        return jsonify({"question": question, "answer": ollama_answer})

    return jsonify(
        {"question": question, "answer": "Sorry, I don't have context on this."}
    )


# Ollama Model Query
def query_ollama(question):
    try:
        response = ollama.generate(
            model="nemotron-mini", prompt=question  # Specify the model here
        )
        return response.get("response", "Sorry, the LLM server faced an error in responding!")
    except Exception as e:
        logging.error("Error querying Ollama: {error}".format(error=e))
        return "Sorry, the LLM server is not available right now!"
