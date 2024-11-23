import requests
from bs4 import BeautifulSoup

from app.domain.llm.DataPreprocessor import DataPreprocessor


class WebsitePreprocessor(DataPreprocessor):
    def get_raw_text(self) -> str:
        if self.url is None and self.html is None:
            raise ValueError("Either URL or HTML must be define")

        html_content = ""
        if self.url is not None:
            response = requests.get(self.url)
            html_content = response.text
        else:
            html_content = self.html

        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        text = ' '.join(text.split())

        return text

