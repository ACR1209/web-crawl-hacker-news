# Hacker News Scraper

This is a web app that scrapes [Hacker News](https://news.ycombinator.com/) and displays it with a couple of filters.

## Stack 
It uses FastAPI and Pydantic to handle the HTTP requests; BeautifulSoup to web scrape the Hacker News page and Jinja2 for templating.

## Installation

To install first is recommended to create a virtual enviroment 
```
  python -m venv .venv
```
Then activate the virtual enviroment
```
  // Linux
  source .venv/bin/activate
  // Windows Powershell
  .venv\Scripts\Activate.ps1
  // Windows Bash
  source .venv/Scripts/activate
```
Lastly install the modules using
```
  pip install -r .\requirements.txt
```

## Running the app
In development mode
```
  fastapi dev app/main.py
```

In production mode
```
  fastapi run
```

## Testing
Simply use the default FastAPI 
```
  pytest
```
