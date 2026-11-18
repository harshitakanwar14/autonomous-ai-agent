
from tools.web_search import search_web

queries = [
    "AI automation in finance and accounting",
    "AI automation in human resources",
    "AI automation in manufacturing operations"
]

for query in queries:

    print("\n" + "=" * 50)
    print("QUERY:", query)
    print("=" * 50)

    try:

        result = search_web(
            query=query,
            max_results=3
        )

        for item in result["results"]:

            print("\nTitle:", item["title"])
            print("URL:", item["url"])
            print("Description:", item["snippet"])

    except Exception as error:

        print("\nSearch failed:", error)
