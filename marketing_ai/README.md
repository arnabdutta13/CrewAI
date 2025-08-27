# MarketingAi Crew

Welcome to the MarketingAi Crew project, powered by [crewAI](https://crewai.com). 

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Install fpdf2. This is required for generating the pdf

```bash
pip install fpdf2
```

Next, navigate to your project directory (marketing_ai) and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Note that the application uses SerperDevAPI for the web search. Ensure that you have a API key for [Serper](https://serpapi.com/)** 

**Add your `OPENAI_API_KEY` and `SERPER_API_KEY` into the `.env` file**


## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the marketing-ai Crew, assembling the agents and assigning them tasks as defined in your configuration.

This application will run the create an `output` folder under the project directory.
You can find 3 json files in this folder: `trends.json`, `strategy.json` and `campaigns.json`. 
These files are the outputs of the agents at each stage.
The `campaigns.pdf` file with the output of a research on LLMs is also generated in the `output` folder.
The PDF report provides the details of the campaign.

## Understanding the Marketing AI Crew

The marketing-ai Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in the crew.

