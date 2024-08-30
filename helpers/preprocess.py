import spacy

# Initialize spaCy for text preprocessing
nlp = spacy.load("en_core_web_sm")


# Function to preprocess the question using spaCy
def preprocess_question(question):
    """
    Preprocesses a given question by lemmatizing the tokens and removing stop words using spaCy.

    Parameters:
    question (str): The input question to be preprocessed.

    Returns:
    str: The preprocessed question after lemmatization and stop words removal.
    """
    doc = nlp(question)
    return " ".join([token.lemma_ for token in doc if not token.is_stop])
