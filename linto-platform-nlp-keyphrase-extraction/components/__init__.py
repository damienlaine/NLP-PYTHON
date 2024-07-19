import spacy
from spacy.language import Language
from typing import List, Union, Tuple
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from thinc.api import Config
from components.keyphrase_extractor import KeyphraseExtractor

# Load components' defaut configuration
config = Config().from_disk("components/config.cfg")

@Language.factory("kpe", default_config=config["components"]["kpe"])
def make_keyphrase_extractor(
    nlp: Language,
    name: str,
    model: SentenceTransformer,
    candidates: List[str] = None,
    keyphrase_ngram_range: Tuple[int, int] = (1, 1),
    stop_words: Union[str, List[str]] = None,
    top_n: int = 5,
    min_df: int = 1,
    use_maxsum: bool = False,
    use_mmr: bool = False,
    diversity: float = 0.5,
    nr_candidates: int = 20,
    vectorizer: CountVectorizer = None,
    highlight: bool = False,
    seed_keywords: List[str] = None
    ):

    kwargs = locals()
    del kwargs['nlp']
    del kwargs['name']
    del kwargs['model']

    return KeyphraseExtractor(model, **kwargs)

