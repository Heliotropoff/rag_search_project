import argparse
from helpers.keyword_search import *
import sys
LIMIT = 5


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build movie index")

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
        case _:
            parser.print_help()


if __name__ == "__main__":
     main()
