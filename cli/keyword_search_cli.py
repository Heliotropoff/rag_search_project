import argparse
import json
import string
from nltk.stem import PorterStemmer
import pickle

STEMMER = PorterStemmer()
FILEPATH = "data/movies.json"
LIMIT = 5

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

def get_stopword_tokens(stopword_file_path):
    with open(stopword_file_path) as sw_file:
        sw_string_raw = sw_file.read()
        sw_string = normalise_term_string(sw_string_raw)
        sw_list = sw_string.splitlines()
        sw_set = set(sw_list)
        return sw_set
STOPWORDS = get_stopword_tokens(stopword_file_path="data/stopwords.txt")



def tokenize(term):
    return set(term.split())

def remove_stopwords(term_token_set):
    return term_token_set - STOPWORDS

def stem_tokens(tokens):
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(STEMMER.stem(token))
    return set(stemmed_tokens)

def tokenize_text(text):
    text_string = normalise_term_string(text)
    text_tokens = tokenize(text_string)
    text_tokens = remove_stopwords(text_tokens)
    text_tokens = stem_tokens(text_tokens)
    return text_tokens

def loadData():
    with open(file=FILEPATH) as dataFile:
         data = json.load(dataFile)
         return data

def searchFetchKeyWord(search_term_tokens: set[str], movieData:dict[str,dict],limit:int = 5) ->list[str]:
    matches: list[str] = []
    for movie in movieData["movies"]:
        title_raw = movie.get("title","")
        title_tokens = tokenize_text(title_raw)
        common_stems = search_term_tokens.intersection(title_tokens)
        if common_stems:
            matches.append(movie.get("title",""))
        if len(matches) >= limit:
            break
    return matches



def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build movie index")

    args = parser.parse_args()

    match args.command:
        case "search":
            data:dict[str,dict] = loadData()
            query_raw = args.query
            query_tokens = tokenize_text(query_raw)
            print(f"Searching for: {query_raw}")
            matches = searchFetchKeyWord(search_term_tokens=query_tokens, movieData= data, limit=LIMIT)
            for i in range(len(matches)):
                print(f"{i+1}. {matches[i]}")
        case "build":
            build_command()
        case _:
            parser.print_help()


class InvertedIndex:
    def __init__(self):
        self.index: dict[str,set] = dict()
        self.docmap: dict[int,dict] = dict()

    def __add_document(self, doc_id, text):
        text_tokens = tokenize_text(text)
        for token in text_tokens:
            if not self.index.get(token,False):
                self.index[token] = set([doc_id])
            else:
                self.index[token].add(doc_id)

    def get_documents(self, term):
        docs = self.index.get(term,"")
        return sorted(docs)

    def build(self):
        data = loadData()
        for movie in data["movies"]:
            movie_id = movie.get("id")
            title_and_description_string = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id=movie_id,text=title_and_description_string)
            self.docmap = self.docmap[movie_id] = movie


    def save(self):
        index_filepath = "cache/index.pkl"
        docmap_filepath = "cache/docmap.pkl"
        with open(index_filepath,"wb") as index_file:
            pickle.dump(obj=self.index, file=index_file)
        with open(docmap_filepath, "wb") as docmap_file:
            pickle.dump(obj=self.docmap,file=docmap_file)

def build_command():
    movie_index = InvertedIndex()
    movie_index.build()
    movie_index.save()
    docs = movie_index.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")



if __name__ == "__main__":
     main()
