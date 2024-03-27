import json
from .estimate_tokens import estimate_tokens

def aggregate_summaries(summaries_list, token_limit=1000):
    """
    Aggregates summaries into JSON strings, each under a specified token limit.

    Parameters:
    - summaries_list (list): A list of dictionaries, each with 'url', and 'summary' keys.
    - token_limit (int): The maximum number of tokens allowed per aggregated string.

    Returns:
    - list: A list of JSON strings, each containing aggregated summaries and staying under the token limit.
    """
    aggregated_jsons = []
    current_batch = []
    current_tokens = 0

    for summary in summaries_list:
        # Convert the summary dict to JSON and estimate its token count
        summary_json = json.dumps(summary)
        summary_tokens = estimate_tokens(summary_json)

        # Check if adding this summary JSON would exceed the token limit
        if current_tokens + summary_tokens > token_limit:
            # If so, start a new batch for the next set of summaries
            aggregated_jsons.append(json.dumps(current_batch))
            current_batch = [summary]  # Start new batch with this summary
            current_tokens = summary_tokens
        else:
            # Otherwise, add this summary to the current batch
            current_batch.append(summary)
            current_tokens += summary_tokens

    # Don't forget to add the last batch if it's not empty
    if current_batch:
        aggregated_jsons.append(json.dumps(current_batch))

    return aggregated_jsons