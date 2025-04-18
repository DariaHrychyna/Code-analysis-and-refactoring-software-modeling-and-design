import sqlite3


def create_tables():
    conn = sqlite3.connect("store_original.db")
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        availability INTEGER NOT NULL
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )''')

    conn.commit()
    conn.close()


def seed_products():
    conn = sqlite3.connect("store_original.db")
    cur = conn.cursor()

    # Перевіримо, чи вже є дані
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        products = [
            (1, "Гірський велосипед", 12000.0, 100),
            (2, "Міський велосипед", 8500.0, 50),
            (3, "Дитячий велосипед", 5600.0, 30),
            (4, "Електровелосипед", 22000.0, 0)  # Немає в наявності
        ]
        cur.executemany("INSERT INTO products (id, name, price, availability) VALUES (?, ?, ?, ?)", products)
        conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect("store_original.db")


if __name__ == "__main__":
    create_tables()
