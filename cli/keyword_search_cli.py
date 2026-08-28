import argparse
import json
from typing import Any

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            with open("data/movies.json") as dataFile:
                data = json.load(dataFile)
            print(f"Searching for: {args.query}")
            matches = searchFetchKeyWord(keyword=args.query, movieData= data)
            for i in range(len(matches)):
                print(f"{i+1}. {matches[i]}")
        case _:
            parser.print_help()

def searchFetchKeyWord(keyword: str, movieData:dict, limit:int = 5) ->list[str]:
    matches: list[str] = []
    for movie in movieData["movies"]:
        title = movie.get("title","")
        if keyword in title:
            matches.append(title)
        if len(matches) >= limit:
            break
    return matches


if __name__ == "__main__":
     main()
