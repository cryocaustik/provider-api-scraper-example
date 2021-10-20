# Provider API Scraper Example

Example of scraping a paginated API endpoint and dumping the data into a DB.

## Pre-requisits

- [Python >= 3.9](https://python.org)
- [Pipenv](https://pypi.org/project/pipenv/)

## Setup

```sh
# install python dependencies
pipenv install

# copy and update env variables
cp .env.example .env

# initialize venv
pipenv shell

# execute script
python scrape_providers.py
```