from concurrent.futures import ThreadPoolExecutor, as_completed
from .execute_pipeline import execute_pipeline
from .aggregate_summaries import aggregate_summaries

def retrieve_summaries(goal, instructions, src_results_list):
    """
    Parallel launch the summary retrieval pipeline. Returns a list of summary chunks, the count of results, and
    the count of relevant results.

    Parameters:
    - goal (str): The user goals.
    - instructions (str): The system prompt for the agents.
    - src_results_list (list): A list of Google search results obtained from the SERP API.
    """

    summaries_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit pipeline execution jobs
        futures = [executor.submit(execute_pipeline, goal, instructions, result) for result in src_results_list]

        # Wait for all futures to complete and print their results
        for future in as_completed(futures):
            completed_task = future.result()
            if completed_task["relevant"] == "TRUE":
                summaries_list.append(completed_task)

    results_count = len(src_results_list)
    relevant_count = len(summaries_list)
    summary_chunks = aggregate_summaries(summaries_list)

    return summary_chunks, results_count, relevant_count