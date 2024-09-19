# Hacker News Scraper

This is a web app that scrapes [Hacker News](https://news.ycombinator.com/) and displays it with a couple of filters.

## Stack 
It uses FastAPI and Pydantic to handle the HTTP requests; BeautifulSoup to web scrape the Hacker News page and Jinja2 for templating.

## High Level Architecture
![HackerNewsCrawl](https://github.com/user-attachments/assets/967ab6ae-38ae-4c87-947f-c507a9ff5f8d)


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
In development mode run and visit http://localhost:8000
```
  fastapi dev app/main.py
```

In production mode and visit http://localhost:8000
```
  fastapi run
```


## Running with Docker
To run the app with docker simply build the image and create a container, after the container is running you may visit http://localhost:8000
```
  docker build -t hn-scrape .
  docker run -d --name hn-scrape -p 8000:80 hn-scrape
```

## Testing
Simply use the default FastAPI 
```
  pytest
```
