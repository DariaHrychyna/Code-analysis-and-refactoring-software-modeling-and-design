from Business.book import Book


class BookFactory:
    _id_counter = 1

    @classmethod
    def create_book(cls, title: str, author: str, price: float) -> Book:
        book = Book(cls._id_counter, title, author, price)
        cls._id_counter += 1
        return book
