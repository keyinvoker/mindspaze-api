import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer

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


# # Create a parser and tokenizer for the cleaned text
# parser = PlaintextParser.from_string(cleaned_text, Tokenizer('english'))

# # Initialize the summarizer
# summarizer = LsaSummarizer()

# # Summarize the text with a ratio of 0.3 (30% of the original text)
# summary = summarizer(parser.document, 0.3)

# # Print the summarized text
# for sentence in summary:
#     print(sentence)
