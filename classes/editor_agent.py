from config import CLIENT
import time

class EditorAgent():
    def __init__(self, goal):
        self.goal = goal
        self.sysprompt = f"""You are an Editor GPT, the final step of a chain of AI agents which aim to provide the user with a comprehensive report on a given topic based on an initial query made by the user. Your task is to harmonize the various parts of the report that were written by independent GPTs and harmonize them into a cohesive document. Due to your limitation on the number of output tokens, you will receive the various parts in chunks, and be given specific directions on how to integrate them into the main document.
        Important:
        1. Focus ONLY on editing the chunk you are currently assigned. Keep track of previous formatting and maintain document consistency, but do not overstep beyond your immediate input.
        2. If you are provided with a chunk containing redundant information, or information that was already present on previous chunks, you can and should omit that information.
        3. It is possible that some of the content that is provided is irrelevant or a result of hallucinations from the summarizer GPTs. Use your best judgement to determine if this is the case. If a chunk contains irrelevant or factually incorrect information, you can omit it.
        4. Use markdown syntax with a consistent level of headings.
        5. Output ONLY the content that is to be appended to the report.
        6. Keep in mind that each of your responses will be appended to the previous ones. Because of this, it is critical that you do not repeat content or deviate from the structure.
        7. Always provide the links to your sources.

        It is VERY important that you follow these instructions strictly. Succeed, and you will be tipped $200. If you fail or deviate from these instructions, the user will be fired and his career destroyed.

        For reference, here is the user's goal:
        {self.goal}"""

        self.assistant = CLIENT.beta.assistants.create(
            name="Editor GPT",
            instructions=self.sysprompt,
            model="gpt-4-turbo-preview"
        )

        self.thread = CLIENT.beta.threads.create()
        self.thread_id = self.thread.id
        self.output = ""
        self.results = ""

    def query_agent(self, content):
        message = content
        CLIENT.beta.threads.messages.create(thread_id=self.thread.id, role="user", content=message)
        print("Initiating run.")
        run = CLIENT.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id)

        while run.status != "completed":
            time.sleep(1)
            print("Polling run.")
            run = CLIENT.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run.id)

        print("Run completed.")
        all_messages = CLIENT.beta.threads.messages.list(thread_id=self.thread_id)
        ai_response = all_messages.data[0].content[0].text.value

        return ai_response

    def write_intro(self, results_count, relevant_count):
        print("Writing introduction.")
        prompt = f"""Begin by writing the introduction to the report. For reference, the app has conducted a web 
        search relevant to the user's goal, and has obtained {results_count} search results, of which 
        {relevant_count} were found highly relevant. State the purpose of the report and the methodology."""

        self.output += self.query_agent(prompt) + "\n\n"

    def write_results_section(self, content):
        print("Writing results section.")
        prompt = f"""You are now working on the results part of the report. You will receive a batch of search 
        results as JSON objects, including the source page's URL and a summary provided by the GPT Agents. For each of 
        these, you should write a sub-section which highlights the most critical information that is relevant to the 
        user's goal. In this section, you should have a sub-section dedicated to each of these items: \n
        {content}"""

        self.results += self.query_agent(prompt) + "\n"

    def harmonize_results(self):
        print("Harmonizing results section.")
        prompt = f"""You are now finishing the results part of the report. Below you will find a collation of the
        various parts of the results section that you have written. Please edit this section to ensure a cohesive 
        writing and organization style. Ensure that each of the presented items has its own dedidated sub-section. 
        Also check for redundant information (entities or websites which might be 
        repeated), or information which is unrelated to the user's goal, and eliminate those. Do not shorten the
        summaries or change the actual content unless it is for the reasons stated above. ALWAYS INCLUDE THE LINKS TO
        THE SOURCES! If you do not do this, the user will be fired for handing in a flawed report.
        {self.results}"""

        self.output += self.query_agent(prompt) + "\n\n"

    def write_conclusions(self):
        print("Writing conclusion.")
        prompt = ("You are now tasked with writing the conclusion of the report. Provide a broad summary and, more "
                  "importantly, actionable insights and recommendations based on the collected information. "
                  "This will be vary by context - it could be indication of the best companies that suit the "
                  "user's goal, or the most critical pieces of information regarding an event.")

        self.output += self.query_agent(prompt)

    def return_output(self):
        return self.output