import argparse
import json
import string

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
            query_raw = args.query
            query_processed = processSearchQuery(query=query_raw )
            print(f"Searching for: {query_raw}")
            matches = searchFetchKeyWord(keyword=query_processed, movieData= data, limit=LIMIT)
            for i in range(len(matches)):
                print(f"{i+1}. {matches[i]}")
        case _:
            parser.print_help()


def processSearchQuery(query):
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

def tokenizeAndCompare(keyword, title):
    keyword_unique_tokens = set(keyword.split())
    title_unique_tokens = set(title.split())
    substing_flag = False
    for title_token in title_unique_tokens:
        for kw_token in keyword_unique_tokens:
            if kw_token in title_token:
                substing_flag = True
                break
    return substing_flag

    #comon_tokens = keyword_unique_tokens.intersection(title_unique_tokens)
    #if comon_tokens:
        #return True
    #return False


def loadData(filepath):
    with open(file=filepath) as dataFile:
         data = json.load(dataFile)
         return data
def searchFetchKeyWord(keyword: list[str], movieData:dict[str,dict], limit:int = 5) ->list[str]:
    matches: list[str] = []
    for movie in movieData["movies"]:
        title = dropPunctuation(movie.get("title","").lower())
        title = title.replace("  "," ")
        if tokenizeAndCompare(keyword=keyword,  title=title):
            matches.append(movie.get("title",""))
        if len(matches) >= limit:
            break
    return matches




if __name__ == "__main__":
     main()
