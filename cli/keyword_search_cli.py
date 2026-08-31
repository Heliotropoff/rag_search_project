import argparse
from helpers.keyword_search import *
import sys
import math
LIMIT = 5


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build movie index")

    tf_parser = subparsers.add_parser("tf", help="Get the term frequency in the document")
    tf_parser.add_argument("doc_id", type=int, help= "Document id for which we are checking the term count")
    tf_parser.add_argument("term", type=str, help="Term we want to get a count of")

    idf_parser = subparsers.add_parser("idf", help="Get the term inverse document frequency")
    idf_parser.add_argument("term", type=str, help="Term for which we want to get an idf value")


    args = parser.parse_args()

    match args.command:
        case "search":
            movie_index = InvertedIndex()
            try:
                movie_index.load()
            except Exception as e:
                print(e)
                sys.exit(1)
            #data:dict[str,dict] = loadData()
            query_raw = args.query
            query_tokens = tokenize_text(query_raw)
            print(f"Searching for: {query_raw}")
            matches = searchFetchKeyWord(search_term_tokens=query_tokens, movieData= movie_index, limit=LIMIT)
            for i in range(len(matches)):
                print(f"{i+1}. Title: {matches[i].get("title")}, ID: {matches[i].get("id")}")
        case "build":
            build_command()
        case "tf":
            movie_index = InvertedIndex()
            try:
                movie_index.load()
            except Exception as e:
                print(e)
                sys.exit(1)
            doc_id = args.doc_id
            term = args.term
            term_token = single_term_tokenizer(term=term)
            term_count_per_doc = movie_index.get_tf(doc_id=doc_id,term=term_token)
            #print(movie_index.term_frequencies[doc_id])
            print(term_count_per_doc)
        case "idf":
            movie_index = InvertedIndex()
            try:
                movie_index.load()
            except Exception as e:
                print(e)
                sys.exit(1)
            term = args.term
            term_token = single_term_tokenizer(term=term)
            associated_documents_count = len(movie_index.get_documents(term=term_token))
            total_documents_count = len(movie_index.docmap)
            term_idf_value = math.log((total_documents_count + 1) / (associated_documents_count + 1))
            print(f"Inverse document frequency of '{args.term}': {term_idf_value:.2f}")
        case _:
            parser.print_help()


if __name__ == "__main__":
     main()
