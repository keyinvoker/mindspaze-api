import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def clean_text(text: str) -> str:
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [token.lower() for token in tokens if token.isalpha()]
    cleaned_tokens = [token for token in cleaned_tokens if token not in stop_words]
    cleaned_tokens = list(set(cleaned_tokens))
    cleaned_text = ' '.join(cleaned_tokens)
    
    return cleaned_text
