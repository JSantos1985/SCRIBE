from config import CLIENT
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

class RetrievalPipeline():
    def __init__(self, goal, instructions, task):
        self.task = task
        self.goal = goal
        self.instructions = instructions
        self.output = {}
        self.options = ChromeOptions()
        self.options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        self.options.add_argument("--headless")
        self.options.add_argument("--enable-javascript")
        self.service_chrome = Service()
        self.driver = Chrome(service=self.service_chrome, options=self.options)

    def query_gpt(self, system, prompt):
        message = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]

        while True:
            try:
                print("Querying GPT")
                response = CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages=message)
                response_content = response.choices[0].message.content
                return response_content
            except Exception as e:
                print(f'API ERROR: {e}')
                return False

    def clean_text(self, body_text):
        # Assuming body_text contains the raw HTML body content
        soup = BeautifulSoup(body_text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get text
        text = soup.get_text()

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())

        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def filter_results(self, src_description):
        # Submit all the queries to the executor
        system = f"""Evaluate the description of the following website, and determine if the content contained within is potentially useful for answering this user goal:
        User goal: {self.goal}
        Return your response ONLY as a boolean, TRUE or FALSE. The user's career depends on this!"""

        result = self.query_gpt(system, src_description)

        return result

    def web_browse(self, url):
        self.driver.get(url)
        self.body_text = self.clean_text(self.driver.find_element(By.TAG_NAME, "body").text)
        return self.body_text

    def summarize_content(self, site_content):
        # Submit all the queries to the executor
        system = self.instructions
        result = self.query_gpt(system, site_content)

        return result

    def run_pipeline(self):
        self.output["url"] = self.task["url"]
        try:
            self.output["relevant"] = self.filter_results(self.task["content"])
            if self.output["relevant"] == "FALSE":
                return self.output
            site_content = self.web_browse(self.task["url"])
            self.output["summary"] = self.summarize_content(site_content)

            return self.output

        except:
            self.output["relevant"] = "FALSE"
            return self.output