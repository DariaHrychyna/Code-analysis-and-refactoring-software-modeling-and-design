class Book:
    def __init__(self, book_id: int, title: str, author: str, price: float):
        self.id = book_id
        self.title = title
        self.author = author
        self.price = price

    def get_info(self) -> str:
        return f"{self.title}, автор {self.author} - {self.price: .2f}"
