import config
import sys
from functions import search_google, retrieve_summaries, launch_editor_agent

def generate_report(src_query, goal, instructions):
    src_results = search_google(src_query)
    summary_chunks, results_count, relevant_count = retrieve_summaries(goal, instructions, src_results)
    launch_editor_agent(goal, summary_chunks, results_count, relevant_count)

if __name__ == '__main__':

    """ 
    EXAMPLE INPUTS
    goal = "Compile a guide on the best general builds in Baldur's Gate 3, detailing each build's components, strengths, and weaknesses, and include any available community feedback or multimedia resources."
    
    src_query = {
      "q": "Baldur's Gate 3 best builds guide -filetype:pdf",
      "num": 10
    }
    
    instructions = "From this website, retrieve summaries of information on the best builds."
    """

    if len(sys.argv) > 1:
      goal = sys.argv[1]
      src_query = sys.argv[2]
      instructions = sys.argv[3]
    else:
      print("Usage: python main.py <goal> '<src_query>' '<instructions>'")
      sys.exit(1)

    print("Goal:", goal)
    print("Source Query:", src_query)
    print("Instructions:", instructions)

    generate_report(src_query, goal, instructions)