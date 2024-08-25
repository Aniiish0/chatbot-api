import json
import os

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser


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
    writer = ix.writer()
    for entry in entries:
        writer.add_document(question=entry["question"], answer=entry["answer"])
    writer.commit()


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


if __name__ == "__main__":
    # Read the knowledge base from the JSON file
    knowledge_base = read_json("knowledge_base.json")
    print(">>> Knowledge base preview:", head_data(knowledge_base))

    # Index the knowledge base
    add_to_index(knowledge_base)


# Function to search the index
def search_index(query):
    with ix.searcher() as searcher:
        query = QueryParser("question", ix.schema).parse(query)
        results = searcher.search(query)
        if results:
            return results[0]["answer"]
        else:
            return "Sorry, I couldn't find an answer to your question."
