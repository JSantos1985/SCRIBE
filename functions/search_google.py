from serpapi import GoogleSearch

def search_google(src_query):
    """
    Conducts a Google Search using the SERP API.

    Parameters:
    - src_query (dictionary): a SERP API formatted search query
    """

    search = GoogleSearch(src_query)

    src_results_list = []
    results = search.get_dict()

    for result in results["organic_results"]:
        src_results_list.append({
            "url": result["link"],
            "content": result["snippet"]
        })

    return src_results_list