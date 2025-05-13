import sqlite3

from Business.book import Book


class Database:
    def __init__(self, db_name="bookstore.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                total REAL,
                payment_method TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                book_id INTEGER,
                quantity INTEGER
            )
        """)

        self.connection.commit()

    def insert_book(self, book):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, price) VALUES ( ?, ?, ?)",
            (book.title, book.author, book.price)
        )
        self.connection.commit()

    def insert_customer(self, customer):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email) VALUES (?, ?)",
            (customer.name, customer.email)
        )
        self.connection.commit()

    def insert_order(self, order, payment_method):
        cursor = self.connection.cursor()
        total = order.calculate_total()
        cursor.execute(
            "INSERT INTO orders (customer_id, total, payment_method) VALUES (?, ?, ?)",
            (order.customer.id, total, payment_method)
        )
        for item in order.items:
            cursor.execute(
                "INSERT INTO order_items (order_id, book_id, quantity) VALUES (?, ?, ?)",
                (order.id, item.book.id, item.quantity)
            )
        self.connection.commit()

    def get_all_books(self) -> list[Book]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, author, price FROM books")
        rows = cursor.fetchall()
        return [Book(row[0], row[1], row[2], row[3]) for row in rows]

    def close(self):
        self.connection.close()
