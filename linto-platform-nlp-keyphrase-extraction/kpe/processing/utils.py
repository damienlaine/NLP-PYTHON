from typing import Dict, Any

from spacy.tokens import Doc

def get_data(doc: Doc) -> Dict[str, Any]:
    """Extract the data to return from the REST API given a Doc object. Modify
    this function to include other data."""
    keyphrases = [
        {
            "text": keyphrase[0],
            "score": keyphrase[1]
        }
        for keyphrase in doc._.keyphrases
    ]
    return {"text": doc.text, "keyphrases": keyphrases}
    