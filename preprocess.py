import spacy

# Initialize spaCy for text preprocessing
nlp = spacy.load("en_core_web_sm")


# Function to preprocess the question using spaCy
def preprocess_question(question):
    doc = nlp(question)
    return " ".join([token.lemma_ for token in doc if not token.is_stop])
