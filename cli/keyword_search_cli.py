import argparse
from lib.keyword_search import *
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

    tf_idf_parser = subparsers.add_parser("tfidf", help="Get tf-idf value for a given document and term")
    tf_idf_parser.add_argument("doc_id", type=int, help="Document id where we count tf-idf")
    tf_idf_parser.add_argument("term", type=str, help="The term we want a tf-idf count for")

    bm25_idf_parser = subparsers.add_parser("bm25idf", help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument("term", type=str, help="Term to get BM25 IDF score for")

    bm25_tf_parser = subparsers.add_parser("bm25tf", help="Get BM25 TF score for a given document ID and term")
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument("k1", type=float, nargs="?", default=BM25_K1, help="Tunable BM25 K1 parameter")
    bm25_tf_parser.add_argument("b", type=float, nargs="?", default=BM25_B, help = "Tubable BM25 b parameter")

    bm25search_parser = subparsers.add_parser("bm25search", help="Search movies using full BM25 scoring")
    bm25search_parser.add_argument("query", type=str, help="Search query")
    bm25search_parser.add_argument("limit", type=int, nargs="?", default=5, help = "Optional argument to control number of returned results")



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
            matches = fetch_query_matches(search_term_tokens=query_tokens, movieData= movie_index, limit=LIMIT)
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
        case "tfidf":
            movie_index = InvertedIndex()
            try:
                movie_index.load()
            except Exception as e:
                print(e)
                sys.exit(1)
            doc_id = args.doc_id
            term = args.term
            term_frequeny = movie_index.get_tf(doc_id=doc_id, term=term)
            term_token = single_term_tokenizer(term=term)
            document_term_frequency = len(movie_index.get_documents(term=term_token))
            total_documents_count = len(movie_index.docmap)
            inverse_document_frequency = math.log((total_documents_count + 1) / (document_term_frequency + 1))
            tf_idf_value = term_frequeny * inverse_document_frequency
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf_value:.2f}")
        case "bm25idf":
            bm25idf =bm25_idf_command(query_text=args.term)
            print(f"BM25 IDF score of '{args.term}': {bm25idf:.2f}")
        case "bm25tf":
            doc_id = args.doc_id
            term = args.term
            k1 = args.k1
            b = args.b
            bm25tf = bm25_tf_command(doc_id=doc_id,term=term, k1=k1, b=b)
            print(f"BM25 TF score of '{args.term}' in document '{args.doc_id}': {bm25tf:.2f}")
        case "bm25search":
            query = args.query
            limit = args.limit
            movie_index = InvertedIndex()
            try:
                movie_index.load()
            except Exception as e:
                print(e)
                sys.exit(1)
            relevant_docs_and_scores = movie_index.bm25_search(query=query, limit=limit)
            results = []
            for doc_id, doc_socre in relevant_docs_and_scores.items():
                title = movie_index.docmap[doc_id]["title"]
                score = doc_socre
                results.append(f"({doc_id}) {title} - Score: {score:.2f}")
            for result in results:
                print(result)




        case _:
            parser.print_help()


if __name__ == "__main__":
     main()
