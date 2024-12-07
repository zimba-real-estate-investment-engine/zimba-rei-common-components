import json
import os
import random

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from app.domain.llm.DataPreprocessor import DataPreprocessor


class WebsitePreprocessor(DataPreprocessor):
    """
        Processes websites and extracts data

     self.url = url
        self.text = text
        self.html = html

        Attributes:
        url (str): The site to be processed.
        text str): When it's raw text is to be processed.
        html (str): When it's html is to be processed.
    """

    def get_raw_text(self) -> str:
        if self.url is None and self.html is None:
            raise ValueError("Either URL or HTML must be define")

        html_content = ""
        if self.url is not None:
            html_content = self.get_html()
        else:
            html_content = self.html

        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        text = ' '.join(text.split())

        return text

    def get_html(self) -> str:
        if self.url is None:
            raise ValueError("Set the URL where the HMTL is located")

        try:
            response = requests.get(url=self.url, headers=self._get_random_headers(), timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(f"Error fetching {self.url}: {str(e)}")

    def _load_user_agents(self) -> str:
        load_dotenv()
        self.user_agents = json.loads(os.getenv("USER_AGENTS"))

        if self.user_agents is None:
            raise ValueError("You need .env to have USER_AGENTS list of web user agents")
        return self.user_agents

    def _get_random_headers(self) -> dict:
        headers = {
            "User-Agent": random.choice(self._load_user_agents()),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Upgrade-Insecure-Requests": "1"
        }
        self.headers = headers
        return headers

    @staticmethod
    def get_text_from_url(url: str) -> str:
        try:
            response = requests.get(url=url, headers=WebsitePreprocessor.get_random_headers(), timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(f"Error fetching {url}: {str(e)}")

    @staticmethod
    def get_random_headers() -> dict:
        headers = {
            "User-Agent": random.choice(WebsitePreprocessor.load_user_agents()),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Upgrade-Insecure-Requests": "1"
        }
        return headers

    @staticmethod
    def load_user_agents() -> str:
        load_dotenv()
        user_agents = json.loads(os.getenv("USER_AGENTS"))

        if user_agents is None:
            raise ValueError("You need .env to have USER_AGENTS list of web user agents")
        return user_agents

    @staticmethod
    def get_raw_text_from_html(html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        text = ' '.join(text.split())

        return text
