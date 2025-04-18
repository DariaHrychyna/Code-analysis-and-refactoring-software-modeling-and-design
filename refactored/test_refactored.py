import refactored
import sqlite3
import unittest
from refactored import User, Order, Product, ProductAmount

TEST_DB = "test_refactored.db"


def get_test_connection():
    return sqlite3.connect(TEST_DB)


def create_test_db():
    conn = get_test_connection()
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
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )''')
    conn.commit()
    conn.close()

def seed_test_products():
    conn = get_test_connection()
    c = conn.cursor()
    c.execute("DELETE FROM products")
    c.executemany('''
        INSERT INTO products (id, name, price, availability)
        VALUES (?, ?, ?, ?)
    ''', [
        (1, "Тестовий товар 1", 100.0, 10),
        (2, "Тестовий товар 2", 50.0, 5),
    ])
    conn.commit()
    conn.close()

refactored.get_connection = get_test_connection

class TestShopSystem(unittest.TestCase):
    def setUp(self):
        create_test_db()
        seed_test_products()
        self.conn = get_test_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute("DELETE FROM orders")
        self.cursor.execute("DELETE FROM order_items")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def register_user(self, name, email, password):
        msg, user_id = refactored.AuthService.register(name, email, password)
        return refactored.User(user_id, name, email, password)

    def test_user_registration_success(self):
        msg, user_id = refactored.AuthService.register("Тест", "test@email.com", "123")
        self.assertEqual(msg, "Реєстрація успішна!")
        self.assertIsNotNone(user_id)

    def test_user_registration_duplicate_email(self):
        refactored.AuthService.register("User1", "duplicate@email.com", "pass")
        msg, _ = refactored.AuthService.register("User2", "duplicate@email.com", "pass")
        self.assertEqual(msg, "Користувач з таким email вже існує.")

    def test_login_success(self):
        self.register_user("User", "logintest@email.com", "pass")
        logged_user, msg = refactored.AuthService.login("logintest@email.com", "pass")
        self.assertIsNotNone(logged_user)
        self.assertIn("Вхід успішний", msg)

    def test_login_wrong_password(self):
        self.register_user("User", "wrongpass@email.com", "pass")
        logged_user, msg = refactored.AuthService.login("wrongpass@email.com", "wrong")
        self.assertIsNone(logged_user)
        self.assertEqual(msg, "Неправильний email чи пароль.")

    def test_login_user_not_found(self):
        user, msg = refactored.AuthService.login("noone@email.com", "123")
        self.assertIsNone(user)
        self.assertEqual(msg, "Неправильний email чи пароль.")

    def test_create_order(self):
        user = self.register_user("Test", "order@email.com", "123")
        order = user.place_new_order()
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user_id, user.user_id)

    def test_create_multiple_orders(self):
        user = self.register_user("Multi", "multi@email.com", "123")
        user.place_new_order()
        user.place_new_order()
        self.assertEqual(len(user.orders), 2)

    def test_user_get_orders_no_orders(self):
        user = self.register_user("NoOrders", "noorders@email.com", "123")
        orders = user.get_orders()
        self.assertEqual(orders, [])

    def test_order_add_product_success(self):
        user = self.register_user("Add", "add@email.com", "123")
        order = user.place_new_order()
        product = Product(1, "Тестовий товар 1", 100.0, 10)
        order.add_product(product, 2)
        self.assertEqual(len(order.order_items), 1)

    def test_order_add_product_insufficient_quantity(self):
        user = self.register_user("Low", "low@email.com", "123")
        order = user.place_new_order()
        product = Product(1, "Тестовий товар 1", 100.0, 1)
        order.add_product(product, 20)
        self.assertEqual(len(order.order_items), 0)

    def test_order_total_after_add_product(self):
        user = self.register_user("Total", "total@email.com", "123")
        order = user.place_new_order()
        product = Product(1, "Тестовий товар 1", 100.0, 10)
        order.add_product(product, 3)
        self.assertEqual(order.get_total_price(), 300.0)

    def test_order_items_persistence(self):
        user = self.register_user("Persist", "persist@email.com", "123")
        order = user.place_new_order()
        product = Product(2, "Тестовий товар 2", 50.0, 5)
        order.add_product(product, 2)
        user_orders = user.get_orders()
        self.assertEqual(len(user_orders[0].order_items), 1)
        self.assertEqual(user_orders[0].order_items[0].quantity, 2)

    def test_product_info_output(self):
        product = Product(1, "Name", 10.0, 2)
        info = product.get_product_info()
        self.assertIn("Name", info)

    def test_get_product_price(self):
        product = Product(1, "Name", 200.0, 1)
        item = ProductAmount(1, product, 2)
        self.assertEqual(item.product.price, 200.0)

    def test_add_product_zero_quantity(self):
        user = self.register_user("Zero", "zero@email.com", "123")
        order = user.place_new_order()
        product = Product(1, "Тестовий товар 1", 100.0, 10)
        order.add_product(product, 0)
        self.assertEqual(len(order.order_items), 0)

    def test_add_product_out_of_stock(self):
        user = self.register_user("Out", "out@email.com", "123")
        order = user.place_new_order()
        product = Product(3, "Немає", 100.0, 0)
        order.add_product(product, 1)
        self.assertEqual(len(order.order_items), 0)

    def test_show_order_output(self):
        user = self.register_user("Show", "show@email.com", "123")
        order = user.place_new_order()
        product = Product(1, "Товар", 100.0, 10)
        order.add_product(product, 1)
        order.show_order()

    def test_product_amount_repr(self):
        product = Product(5, "Test", 50, 3)
        amount = ProductAmount(1, product, 3)
        self.assertEqual(amount.quantity, 3)

    def test_empty_order_total_is_zero(self):
        user = self.register_user("Empty", "empty@email.com", "123")
        order = user.place_new_order()
        self.assertEqual(order.get_total_price(), 0.0)

    def test_product_availability_decreases_after_add(self):
        user = self.register_user("Decrease", "decrease@email.com", "123")
        order = user.place_new_order()

        conn = get_test_connection()
        cur = conn.cursor()
        cur.execute("SELECT availability FROM products WHERE id = 1")
        initial = cur.fetchone()[0]
        conn.close()

        product = Product(1, "Тестовий товар 1", 100.0, initial)
        order.add_product(product, 2)

        conn = get_test_connection()
        cur = conn.cursor()
        cur.execute("SELECT availability FROM products WHERE id = 1")
        after = cur.fetchone()[0]
        conn.close()

        self.assertEqual(after, initial - 2)

if __name__ == '__main__':
    unittest.main()
