import requests
import bs4
from abc import ABC, abstractmethod
from app.models.story import Story



# This allows to add different parsing strategies for different websites if needed
class ParseStrategy(ABC):
    @abstractmethod
    def parse(self, data: bs4.BeautifulSoup):
        pass

class HackerNewsStrategy(ParseStrategy):
    def parse(self, data: bs4.BeautifulSoup):
        # get parent of first element with class 'athing'
        first_story = data.select_one('.athing')
        parent = first_story.parent
        parent_children = [child for child in parent.children if isinstance(child, bs4.element.Tag)]
        res = []

        # iterate over all children of parent in group of 3
        for i in range(0, len(parent_children) - 2, 3):
            # get title
            ranks = int(parent_children[i].select_one('.rank').get_text().replace('.', ''))
            title = parent_children[i].select_one('.titleline > a').get_text()

            # get points
            points_element = parent_children[i + 1].select_one('.score')
            points = 0 

            if points_element:
                points = int(points_element.get_text().split()[0])

            # get comments
            comments_siblings = list(parent_children[i + 1].find_all('a', string=lambda text: "comment" in text.lower()))
            comments = 0

            if len(comments_siblings) > 0:
                comments_element = comments_siblings[0]
                comments = int(comments_element.get_text().split()[0])

            res.append(Story(title=title, comments=comments, points=points, rank=ranks)) 
        return res

class WebScraper:
    def __init__(self, url: str):
        self.url: str = url
        self.data: bs4.BeautifulSoup = None

    def get_page(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            self.data = bs4.BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to get page with status code: {response.status_code}")

    def parse_data(self, strategy: ParseStrategy):
        return strategy.parse(self.data)