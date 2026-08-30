import string
from nltk.stem import PorterStemmer
import json
import pickle
import pprint
FILEPATH = "data/movies.json"
STEMMER = PorterStemmer()

def dropPunctuation(str_with_punctuation):
    punctuationChars = string.punctuation
    spaceReplacementString = " " * len(punctuationChars)
    punctReplacementMap = str.maketrans(punctuationChars, spaceReplacementString)
    str_WITHOUT_punctuation = str_with_punctuation.translate(punctReplacementMap)
    return str_WITHOUT_punctuation


def normalise_term_string(query):
    p_query = query.lower()
    p_query = dropPunctuation(p_query)
    p_query = p_query.replace("  ", " ")
    return p_query


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

def searchFetchKeyWord(search_term_tokens: set[str], movieData,limit:int = 5) ->list[dict]:
    matches: dict[int,None] = {}
    matched_movies: list[dict[str,int|str]] = []
    for term in search_term_tokens:
        if len(matches) >= limit:
            break
        docs = movieData.get_documents(term)
        for doc in docs:
            if len(matches) < limit:
                matches[doc] = None
            else:
                break
    for match in list(matches): #extracting keys, the insertion order is preserved here
        movie_doc = movieData.docmap[match]
        matched_movies.append(movie_doc)
    return matched_movies

class InvertedIndex:
    def __init__(self):
        self.index: dict[str,set] = dict()
        self.docmap: dict[int,dict] = dict()
        self.__index_filepath = "cache/index.pkl"
        self.__docmap_filepath = "cache/docmap.pkl"

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
            self.docmap[movie_id] = movie


    def save(self):
        with open(self.__index_filepath,"wb") as index_file:
            pickle.dump(obj=self.index, file=index_file)
        with open(self.__docmap_filepath, "wb") as docmap_file:
            pickle.dump(obj=self.docmap,file=docmap_file)

    def load(self):
        with open(self.__index_filepath, "rb") as index_file:
            self.index = pickle.load(file=index_file)
        with open(self.__docmap_filepath,"rb") as docmap_file:
            self.docmap = pickle.load(file=docmap_file)


def build_command():
    movie_index = InvertedIndex()
    movie_index.build()
    movie_index.save()
