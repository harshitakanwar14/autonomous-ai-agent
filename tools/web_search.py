
from ddgs import DDGS


# Try different search providers independently.
# This avoids relying on one provider for every query.
SEARCH_BACKENDS = [
    "bing",
    "brave",
    "duckduckgo",
    "yahoo"
]


def search_web(query: str, max_results: int = 5):

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    max_results = max(1, min(int(max_results), 8))

    errors = []

    for backend in SEARCH_BACKENDS:

        try:
            print(f"[WEB SEARCH] Trying {backend}...")

            with DDGS(timeout=12) as ddgs:

                results = ddgs.text(
                    query=query.strip(),
                    region="in-en",
                    max_results=max_results,
                    backend=backend
                )

            if results:

                formatted_results = []

                for item in results:

                    formatted_results.append({
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "snippet": item.get("body", "")
                    })

                print(
                    f"[WEB SEARCH] Found "
                    f"{len(formatted_results)} results "
                    f"using {backend}."
                )

                return {
                    "query": query,
                    "backend": backend,
                    "total_results": len(formatted_results),
                    "results": formatted_results
                }

            errors.append(f"{backend}: Empty results")

        except Exception as error:

            errors.append(
                f"{backend}: {str(error)[:250]}"
            )

            print(
                f"[WEB SEARCH] {backend} failed. "
                "Trying another provider..."
            )

    raise RuntimeError(
        "All search providers failed:\n"
        + "\n".join(errors)
    )
