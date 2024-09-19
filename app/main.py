from app.utils.web_scraper import WebScraper, HackerNewsStrategy
from fastapi import FastAPI
from contextlib import asynccontextmanager

CRAWL_URL = "https://news.ycombinator.com"
web_scraper = WebScraper(CRAWL_URL)
data = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global data
    web_scraper.get_page()
    data = web_scraper.parse_data( HackerNewsStrategy() )
    yield
    data = None

app = FastAPI(lifespan=lifespan)

@app.get("/refresh")
def refresh():
    global data
    web_scraper.get_page()
    data = web_scraper.parse_data( HackerNewsStrategy() )
    return { "message": "success" }

@app.get("/")
def read_root():
    global data
    return {"data": data}
