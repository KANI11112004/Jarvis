from googlesearch import search

def google_search(query, num_results=5):
    results = list(search(query, num_results=num_results))
    return results

query = "Who is Adarsha Ranjan Datta?"
search_results = google_search(query)

for i, result in enumerate(search_results, 1):
    print(f"{i}. {result}")
