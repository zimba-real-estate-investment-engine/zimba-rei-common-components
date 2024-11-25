from abc import ABC, abstractmethod


class DataPreprocessor(ABC):
    def __init__(self, url=None, text=None, html=None):
        self.url = url
        self.text = text
        self.html = html

    @abstractmethod
    def get_raw_text(self):
        pass

    def get_html(self):
        pass

    def get_json(self):
        pass
