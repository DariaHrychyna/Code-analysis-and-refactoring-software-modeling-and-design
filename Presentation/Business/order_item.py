from Business.book import Book


class OrderItem:
    def __init__(self, book: Book, quantity: int):
        self.book = book
        self.quantity = quantity

    def get_total_price(self) -> float:
        return self.book.price * self.quantity
