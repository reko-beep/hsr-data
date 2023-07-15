import json
import os
from pathlib import Path


class Books:
    def __init__(self, book_id: int):
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/books/{book_id}.json") as file:
            self.content: dict = json.loads(file.read())
