from classes import RetrievalPipeline

def execute_pipeline(goal, instructions, src_result):
    """
    Execute the summary retrieval pipeline.

    Parameters:
    - goal (str): The user goals.
    - instructions (str): The system prompt for the agents.
    - src_result (dict): A dictionary containing information about a website ("content" and "url" keys).
    """

    pipeline_instance = RetrievalPipeline(goal, instructions, src_result)
    return pipeline_instance.run_pipeline()