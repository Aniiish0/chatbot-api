import json
import os
import shutil

from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

# Define the schema for the knowledge base index
schema = Schema(question=TEXT(stored=True), answer=TEXT(stored=True))


def get_index(directory='index_directory', new=False):
    """
    This function retrieves or creates a Whoosh index for the knowledge base.

    Parameters:
    new (bool): A flag indicating whether to create a new index. If True, the existing index directory will be removed if it exists. Default is False.

    Returns:
    ix (whoosh.index.Index): The Whoosh index object for the knowledge base.
    """

    # Remove the existing index directory if new flag is set to True and it exists
    if new and os.path.exists(directory):
        shutil.rmtree(directory)

    # Check if the directory exists
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(">>> Directory '{directory}' created.".format(directory=directory))

    # Check if the index exists within the directory
    if exists_in(directory):
        print(">>> Index exists. Opening index...")
        ix = open_dir(directory)
    else:
        print(">>> Index does not exist. Creating new index...")
        ix = create_in(directory, schema)

    return ix

def read_json(file_path):
    """
    This function reads a JSON file and returns its contents.

    Parameters:
    file_path (str): The path to the JSON file to be read.

    Returns:
    dict or None: The JSON data as a Python dictionary, or None if an error occurs.
    If a FileNotFoundError is raised, it prints "File not found."
    If a JSONDecodeError is raised, it prints "Error decoding JSON."
    """
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
    """
    This function adds a list of entries to the Whoosh index.

    Parameters:
    entries (list): A list of dictionaries, where each dictionary represents an entry with 'question' and 'answer' keys.

    Returns:
    None: This function does not return any value. It adds documents to the index.

    The function first retrieves or creates a new Whoosh index using the `get_index` function with the `new` parameter set to True.
    Then, it opens a writer for the index and iterates over the entries. For each entry, it adds a document to the index using the 'question' and 'answer' fields.
    Finally, it commits the changes to the index.
    """
    ix = get_index(new=True)
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
    """
    This function searches the Whoosh index for a given query and returns the corresponding answer.

    Parameters:
    query (str): The search query string.

    Returns:
    str: The answer to the search query, or a message indicating that no answer was found.

    The function first retrieves the existing Whoosh index using the `get_index` function.
    It then opens a searcher for the index using a context manager (`with ix.searcher() as searcher`).
    The query is parsed using a QueryParser with the 'question' field and the index schema.
    The searcher then performs the search using the parsed query and retrieves the results.

    If any results are found, the function returns the answer from the first result.
    If no results are found, it returns a message indicating that no answer was found.
    """
    ix = get_index()
    with ix.searcher() as searcher:
        query = QueryParser("question", ix.schema).parse(query)
        results = searcher.search(query)

        print(">>> results:", results)
        if results:
            return results[0]["answer"]
        else:
            return "Sorry, I couldn't find an answer to your question."
