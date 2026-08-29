import argparse
import json
import string
from nltk.stem import PorterStemmer

FILEPATH = "data/movies.json"
LIMIT = 5

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            data:dict[str,dict] = loadData(filepath=FILEPATH)
            sw = get_stopword_tokens(stopword_file_path="data/stopwords.txt")
            stemmer = PorterStemmer()
            query_raw = args.query
            query_processed = normalise_term_string(query=query_raw )
            query_tokens = tokenize_text(query_processed, sw,  stemmer)
            print(f"Searching for: {query_raw}")
            matches = searchFetchKeyWord(search_term_tokens=query_tokens, movieData= data, limit=LIMIT, stopWords=sw, stemmer=stemmer)
            for i in range(len(matches)):
                print(f"{i+1}. {matches[i]}")
        case _:
            parser.print_help()


def normalise_term_string(query):
    p_query = query.lower()
    p_query = dropPunctuation(p_query)
    p_query = p_query.replace("  ", " ")
    return p_query

def dropPunctuation(str_with_punctuation):
    punctuationChars = string.punctuation
    spaceReplacementString = " " * len(punctuationChars)
    punctReplacementMap = str.maketrans(punctuationChars, spaceReplacementString)
    str_WITHOUT_punctuation = str_with_punctuation.translate(punctReplacementMap)
    return str_WITHOUT_punctuation

def tokenize(term):
    return set(term.split())

def get_stopword_tokens(stopword_file_path):
    with open(stopword_file_path) as sw_file:
        sw_string_raw = sw_file.read()
        sw_string = normalise_term_string(sw_string_raw)
        sw_list = sw_string.splitlines()
        sw_set = set(sw_list)
        return sw_set

def remove_stopwords(term_token_set, stopwords_token_set):
    return term_token_set - stopwords_token_set

def stem_tokens(tokens, stemmer):
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(stemmer.stem(token))
    return set(stemmed_tokens)

def tokenize_text(text, stopwords, stemmer):
    text_tokens = tokenize(text)
    text_tokens = remove_stopwords(text_tokens, stopwords)
    text_tokens = stem_tokens(text_tokens, stemmer)
    return text_tokens

def loadData(filepath):
    with open(file=filepath) as dataFile:
         data = json.load(dataFile)
         return data

def searchFetchKeyWord(search_term_tokens: set[str], movieData:dict[str,dict], stopWords:set[str], stemmer, limit:int = 5) ->list[str]:
    matches: list[str] = []
    for movie in movieData["movies"]:
        title_raw = movie.get("title","")
        title = normalise_term_string(title_raw)
        title_tokens = tokenize_text(title, stopWords, stemmer)
        common_stems = search_term_tokens.intersection(title_tokens)
        if common_stems:
            matches.append(movie.get("title",""))
        if len(matches) >= limit:
            break
    return matches



class InvertedIndex:
    def __init__(self):
        self.index: dict[str,set] = dict()
        self.docmap: dict[str,dict] = dict()

    def __add_document(self, doc_id, text):
        text_tokens = tokenize(text)

    def get_documents(self, term):
        pass

    def build(self):
        pass



if __name__ == "__main__":
     main()
