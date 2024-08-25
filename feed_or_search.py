import json
import os

from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

# Define the schema for the knowledge base index
schema = Schema(question=TEXT(stored=True), answer=TEXT(stored=True))


def get_index():
    index_dir = "indexdir"

    # Check if the directory exists
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        print(">>> Directory 'indexdir' created.")

    # Check if the index exists within the directory
    if exists_in(index_dir):
        print(">>> Index exists. Opening index...")
        ix = open_dir(index_dir)
    else:
        print(">>> Index does not exist. Creating new index...")
        ix = create_in(index_dir, schema)

    return ix

def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None

def head_data(list_data, n_head = 3):
    return list_data[:min(len(knowledge_base), n_head)]

# Function to add documents to the index
def add_to_index(entries):
    ix = get_index()
    writer = ix.writer()
    for entry in entries:
        writer.add_document(question=entry["question"], answer=entry["answer"])
    writer.commit()


if __name__ == "__main__":
    # Read the knowledge base from the JSON file
    knowledge_base = read_json("knowledge_base.json")
    print(">>> Knowledge base preview:", head_data(knowledge_base))

    # Index the knowledge base
    add_to_index(knowledge_base)


# Function to search the index
def search_index(query):
    ix = get_index()
    with ix.searcher() as searcher:
        query = QueryParser("question", ix.schema).parse(query)
        results = searcher.search(query)

        print(">>> results:", results)
        if results:
            return results[0]["answer"]
        else:
            return "Sorry, I couldn't find an answer to your question."
