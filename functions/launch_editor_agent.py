from classes import EditorAgent
from .markdown_to_docx import markdown_to_docx

def launch_editor_agent(goal, summary_chunks, results_count, relevant_count):
    """
    Launch the Editor agent.

    Parameters:
    - goal (str): The user goals.
    - summary_chunks (list): A list of JSON strings obtained from aggregate_summaries()
    - instructions (str): The system prompt for the agents.
    - results_count (int): The number of results found
    - relevant_count (int): The number of relevant results
    """

    editor = EditorAgent(goal)
    editor.write_intro(results_count, relevant_count)

    for summary_chunk in summary_chunks:
        editor.write_results_section(summary_chunk)

    editor.harmonize_results()
    editor.write_conclusions()
    report = editor.return_output()

    markdown_to_docx(report)