from serpapi import GoogleSearch

def search_google(src_query):
    search = GoogleSearch(src_query)

    src_results_list = []
    results = search.get_dict()

    for result in results["organic_results"]:
        src_results_list.append({
            "url": result["link"],
            "content": result["snippet"]
        })

    return src_results_list