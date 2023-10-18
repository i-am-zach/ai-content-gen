# AI Content Generation Tool

The AI Content Generation Tool handles the End-To-End creation of blog content curation from research to publish.

This code repository contains a data pipeline which does the following:
1. Sources data from RSS feeds
2. Prompts an LLM to filter which articles are relevant
3. Scrapes the relevant articles for their text content with Selenium
4. *Optionally*, summarizes the articles in the style of the Morning Brew.

The data pipeline is managed through [Prefect](https://www.prefect.io/).

# Quick Start

## Virtual Environment

To get started, first initialize your Python environment with poetry.

```bash
poetry init
```

Install the required packages.
```bash
poetry install
```

## Configuring Your Environment

The tool uses the OpenAI GPT API to (a) classify articles as interesting and (b) summarize articles in an interesting and engaging style. 

## Running Your Flow with Prefect

Prefect organizes data pipelines into flows and tasks. You can read more about them [here](https://docs.prefect.io/2.13.7/concepts/flows/). To execute our data pipeline, we need to create a deployment (which contains a flow) with Prefect and execute the flow. 

There are two ways to host prefect, locally and managed cloud. To get the prefect server started locally, run:

```bash
prefect server start
```

If you want to execute a data collection pipeline, run 
```bash
prefect deployment run 'interesting-articles-flow/interesting_articles_deployment'
```

Then go to your Prefect dashboard (if local, then [http://localhost:4200/](http://localhost:4200)) and view the flow run.

