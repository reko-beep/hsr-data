import json


class Books:
    def __init__(self, book_id: int):
        with open(f"raw_data/en/books/{book_id}.json") as file:
            self.content: dict = json.loads(file.read())


print(Books(12643).content)
