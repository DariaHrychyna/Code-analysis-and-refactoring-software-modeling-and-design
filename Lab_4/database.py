import sqlite3
from dish import Dish
from customer import Customer
from order import Order, OnlineOrder

DB_NAME = "restaurant.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_type TEXT,
            total_price REAL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_dishes (
            order_id INTEGER,
            dish_id INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(dish_id) REFERENCES dishes(id)
        )
    ''')

    conn.commit()
    conn.close()


def add_dish(dish: Dish):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO dishes (name, price, category) VALUES (?, ?, ?)",
                       (dish.dish_name, dish.price, dish.category))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()


def add_customer(customer: Customer) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
                   (customer.customer_name, customer.email, customer.phone_number))
    customer_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return customer_id


def add_order(order: Order, customer_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    order_type = "online" if isinstance(order, OnlineOrder) else "offline"
    total_price = order.calculate_total_price()

    cursor.execute("INSERT INTO orders (customer_id, order_type, total_price) VALUES (?, ?, ?)",
                   (customer_id, order_type, total_price))
    order_id = cursor.lastrowid

    for dish in order.dishes:
        cursor.execute("SELECT id FROM dishes WHERE name=? AND category=?", (dish.dish_name, dish.category))
        dish_row = cursor.fetchone()
        if dish_row:
            dish_id = dish_row[0]
            cursor.execute("INSERT INTO order_dishes (order_id, dish_id) VALUES (?, ?)", (order_id, dish_id))

    conn.commit()
    conn.close()


def login_customer(email: str):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result

