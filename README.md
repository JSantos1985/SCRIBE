# SCRIBE: Systematic Content Review and Intelligence Briefing Engine

SCRIBE is a Python-based tool inspired by [gpt-researcher](https://github.com/assafelovic/gpt-researcher) designed to automate the process of generating comprehensive reports on a wide array of topics. By leveraging advanced AI agents for web scraping and information retrieval, SCRIBE compiles key insights and information into a cohesive Markdown document. This tool is ideal for researchers, content creators, and anyone looking to synthesize detailed reports from web-based sources. It is designed to have minimal dependencies to facilitate integration into other projects.

## Features

- **Automated Web Scraping**: Utilizes SERP API to conduct targeted web searches based on user-defined queries.
- **Intelligent Summarization**: Employs AI agents to extract and summarize essential information from web pages, guided by user-provided instructions.
- **Report Generation**: Compiles the gathered information into a well-organized report, formatted in Markdown for easy sharing and further editing.

## Installation

First, ensure that you have Python 3.6 or newer installed. Then, clone this repository and install the required dependencies:

```
git clone https://github.com/JSantos1985/SCRIBE
cd SCRIBE
pip install -r requirements.txt
```

## Usage

SCRIBE requires three main inputs to generate a report:

1. **src_query**: A JSON-formatted search query for the SERP API.
2. **goal**: A description of the report's objective.
3. **instructions**: Specific guidelines for what the AI agents should focus on during website information retrieval.

Run SCRIBE from the command line by providing the necessary arguments:

```
python main.py '{"q": "Your search query"}' "Your report goal" "Your retrieval instructions"
```

Ensure you replace the placeholders with your actual search query, goal, and instructions.

## Output

The generated report will be saved as a docx file in the current directory, with a unique name to prevent overwrites. This Markdown file can easily be converted to other formats, shared, or published as needed.

## Contributing

We welcome contributions to SCRIBE, whether they involve new features, improvements, or bug fixes. Please fork the repository and submit your pull requests for review.

## License

SCRIBE is released under the [MIT License](LICENSE).