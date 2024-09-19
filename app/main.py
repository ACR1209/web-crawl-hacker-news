from app.utils.web_scraper import WebScraper, HackerNewsStrategy
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.models.story import Story
from pydantic_settings import BaseSettings
from app.utils.words import within_word_range

class Settings(BaseSettings):
    ENVIRONMENT: str

CRAWL_URL = "https://news.ycombinator.com"
web_scraper = WebScraper(CRAWL_URL)
data = None

settings = Settings( ENVIRONMENT="production")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global data
    if settings.ENVIRONMENT == "test": 
        data = None 
    else:
        web_scraper.get_page()
        data = web_scraper.parse_data( HackerNewsStrategy() )
    yield
    data = None

app = FastAPI(lifespan=lifespan)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/refresh")
def refresh():
    global data
    if settings.ENVIRONMENT == "test":
        # mock data
        data = [
            Story(title="Pivotal Tracker will shut down", comments=50, points=91, rank=1),
            Story(title="Show HN: Chili. Rust port of Spice, a low-overhead parallelization library", comments=8, points=74, rank=2),
            Story(title="Drift towards danger and the normalization of deviance (2017)", comments=19, points=52, rank=3),
            Story(title="Diatom Arrangements", comments=6, points=35, rank=4),
            Story(title="I Revived 3-Axis CNC Mill G-Code Simulator", comments=6, points=61, rank=5),
            Story(title="Show HN: A CLI tool I made to self-host any app with two commands on a VPS", comments=0, points=21, rank=6),
            Story(title="Is Tor still safe to use?", comments=442, points=659, rank=7),
            Story(title="Seeing Like a Network", comments=0, points=7, rank=8),
            Story(title="The making of Four Laps – a looping video about looping videos (2021)", comments=6, points=34, rank=9),
            Story(title="Human genome stored on 'everlasting' memory crystal", comments=2, points=16, rank=10),
            Story(title="Ask HN: How to roll out an internal UI component library", comments=17, points=9, rank=11),
            Story(title="Geometric Search Trees", comments=8, points=76, rank=12),
            Story(title="Moshi: A speech-text foundation model for real time dialogue", comments=49, points=301, rank=13),
            Story(title="A Cyborg Manifesto (1991) [pdf]", comments=0, points=7, rank=14),
            Story(title="Support for IPv6", comments=42, points=54, rank=15),
            Story(title="J2ME-Loader: J2ME emulator for Android devices", comments=41, points=81, rank=16),
            Story(title="Ruby-SAML pwned by XML signature wrapping attacks", comments=66, points=136, rank=17),
            Story(title="A high-performance, zero-overhead, extensible Python compiler using LLVM", comments=76, points=212, rank=18),
            Story(title="Show HN: ts-remove-unused – Remove unused code from your TypeScript project", comments=48, points=91, rank=19),
            Story(title="Show HN: I've Built an Accounting System", comments=21, points=115, rank=20),
            Story(title="Ask HN: My son might be blind – how to best support", comments=98, points=262, rank=21),
            Story(title="OpenTelemetry and vendor neutrality: how to build an observability strategy", comments=28, points=119, rank=22),
            Story(title="Lichess: Post-Mortem of Our Longest Downtime", comments=16, points=80, rank=23),
            Story(title="Text makeup – a tool to decode and explore Unicode strings", comments=8, points=88, rank=24),
            Story(title="Show HN: I made crowdwave – imagine Twitter/Reddit but every post is a voicemail", comments=97, points=180, rank=25),
            Story(title="Aliens and the Enlightenment", comments=36, points=37, rank=26),
            Story(title="Organic thermoelectric device can harvest energy at room temperature", comments=5, points=13, rank=27),
            Story(title="Meticulous (YC S21) is hiring to eliminate UI tests", comments=0, points=0, rank=28),
            Story(title="Netflix's Key-Value Data Abstraction Layer", comments=3, points=33, rank=29),
            Story(title="Holding a Program in One's Head (2007)", comments=87, points=101, rank=30)]
    else:
        web_scraper.get_page()
        data = web_scraper.parse_data( HackerNewsStrategy() )
    return { "message": "success" }

@app.get("/data")
def get_data(order_by: str | None = "rank", count_words_min: int | None = 0, count_words_max: int | None = None):
    return {"data": filter_data(order_by=order_by, count_words_min=count_words_min, count_words_max=count_words_max)}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, order_by: str | None = "rank", count_words_min: int | None = 0, count_words_max: int | None = None):
    return templates.TemplateResponse(request=request, name="index.html", context={"data": filter_data(order_by=order_by, count_words_min=count_words_min, count_words_max=count_words_max)})

def filter_data(order_by: str = "rank", count_words_min: int = 0, count_words_max: int = None)->list[Story]:
    global data

    if not data:  
        return []

    if order_by not in {"rank", "points", "comments"}:
        order_by = "rank"

    count_words_min = max(0, count_words_min)

    if count_words_max is not None and count_words_min > count_words_max:
        count_words_min, count_words_max = count_words_max, count_words_min

    filtered_data = [story for story in data if within_word_range(story, count_words_min=count_words_min, count_words_max=count_words_max)]

    sorting_key = {"rank": lambda story: story.rank,
                   "points": lambda story: story.points,
                   "comments": lambda story: story.comments}.get(order_by)

    return sorted(filtered_data, key=sorting_key, reverse=(order_by != "rank"))
