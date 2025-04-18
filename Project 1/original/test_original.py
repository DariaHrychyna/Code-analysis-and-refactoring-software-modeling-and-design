import original
import sqlite3
import unittest
from original import User, Order, Product, ProductAmount

TEST_DB = "test_original.db"


def get_test_connection():
    """З'єднання з тестовою базою даних."""
    return sqlite3.connect(TEST_DB)


def create_test_db():
    """Створення таблиць для тестової бази даних, якщо вони ще не існують."""
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
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )''')

    conn.commit()
    conn.close()


def seed_test_products():
    """Заповнення тестової бази даних тестовими товарами."""
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


original.get_connection = get_test_connection


class TestShopSystem(unittest.TestCase):
    """Набір тестів для тестування функціоналу системи магазину."""

    def setUp(self):
        """Налаштування середовища перед кожним тестом."""
        create_test_db()
        seed_test_products()
        self.conn = get_test_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute("DELETE FROM orders")
        self.cursor.execute("DELETE FROM order_items")
        self.conn.commit()

    def tearDown(self):
        """Закриває з'єднання з базою після кожного тесту."""
        self.conn.close()

    def test_user_registration_success(self):
        """Тест успішної реєстрації користувача."""
        user = User(0, "Тест", "test@email.com", "123")
        result = user.register()
        self.assertEqual(result, "Реєстрація успішна!")

    def test_user_registration_duplicate_email(self):
        """Тест реєстрації користувача з існуючим email."""
        user1 = User(0, "User1", "duplicate@email.com", "pass")
        user1.register()
        user2 = User(0, "User2", "duplicate@email.com", "pass")
        result = user2.register()
        self.assertEqual(result, "Користувач з таким email вже існує.")

    def test_login_success(self):
        """Тест успішного входу користувача."""
        user = User(0, "User", "logintest@email.com", "pass")
        user.register()
        logged_user, msg = User.login("logintest@email.com", "pass")
        self.assertIsNotNone(logged_user)
        self.assertIn("Вхід успішний", msg)

    def test_login_wrong_password(self):
        """Тест входу з неправильним паролем."""
        user = User(0, "User", "wrongpass@email.com", "pass")
        user.register()
        logged_user, msg = User.login("wrongpass@email.com", "wrong")
        self.assertIsNone(logged_user)
        self.assertEqual(msg, "Неправильний пароль.")

    def test_login_user_not_found(self):
        """Тест входу неіснуючого користувача."""
        user, msg = User.login("noone@email.com", "123")
        self.assertIsNone(user)
        self.assertEqual(msg, "Користувача не знайдено.")

    def test_create_order(self):
        """Тест створення нового замовлення користувачем."""
        user = User(0, "Test", "order@email.com", "123")
        user.register()
        order = user.create_order()
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user_id, user.user_id)

    def test_create_multiple_orders(self):
        """Тест створення кількох замовлень одним користувачем."""
        user = User(0, "Multi", "multi@email.com", "123")
        user.register()
        order1 = user.create_order()
        order2 = user.create_order()
        self.assertEqual(len(user.orders), 2)

    def test_user_get_orders_no_orders(self):
        """Тест отримання замовлень для користувача без замовлень."""
        user = User(0, "NoOrders", "noorders@email.com", "123")
        user.register()
        orders = user.get_orders()
        self.assertEqual(orders, [])

    def test_order_add_product_success(self):
        """Тест додавання продукту до замовлення."""
        user = User(0, "Add", "add@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(1, "Тестовий товар 1", 100.0, 10)
        order.add_product(product, 2)
        self.assertEqual(len(order.order_items_list), 1)

    def test_order_add_product_insufficient_quantity(self):
        """Тест додавання продукту з недостатньою кількістю."""
        user = User(0, "Low", "low@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(1, "Тестовий товар 1", 100.0, 1)
        order.add_product(product, 20)
        self.assertEqual(len(order.order_items_list), 0)

    def test_order_total_after_add_product(self):
        """Тест загальної суми замовлення після додавання товару."""
        user = User(0, "Total", "total@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(1, "Тестовий товар 1", 100.0, 10)
        order.add_product(product, 3)
        self.assertEqual(order.get_total_price(), 300.0)

    def test_order_items_persistence(self):
        """Тест збереження товарів у замовленні в базі даних."""
        user = User(0, "Persist", "persist@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(2, "Тестовий товар 2", 50.0, 5)
        order.add_product(product, 2)
        user_orders = user.get_orders()
        self.assertEqual(len(user_orders[0].order_items_list), 1)
        self.assertEqual(user_orders[0].order_items_list[0].quantity, 2)

    def test_product_info_output(self):
        """Тест виводу інформації про продукт."""
        product = Product(1, "Name", 10.0, 2)
        info = product.get_product_info()
        self.assertIn("Name", info)

    def test_get_product_price(self):
        """Тест отримання ціни продукту з ProductAmount."""
        product = Product(1, "Name", 200.0, 1)
        item = ProductAmount(1, product, 2)
        self.assertEqual(item.get_product_price(), 200.0)

    def test_add_product_zero_quantity(self):
        """Тест додавання товару з нульовою кількістю."""
        user = User(0, "Zero", "zero@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(1, "Тестовий товар 1", 100.0, 10)
        order.add_product(product, 0)
        self.assertEqual(len(order.order_items_list), 0)

    def test_add_product_out_of_stock(self):
        """Тест додавання товару, якого немає в наявності."""
        user = User(0, "Out", "out@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(3, "Немає", 100.0, 0)
        order.add_product(product, 1)
        self.assertEqual(len(order.order_items_list), 0)

    def test_show_order_output(self):
        """Тест виводу замовлення."""
        user = User(0, "Show", "show@email.com", "123")
        user.register()
        order = user.create_order()
        product = Product(1, "Товар", 100.0, 10)
        order.add_product(product, 1)
        order.show_order()

    def test_product_amount_repr(self):
        """Тест створення екземпляра ProductAmount."""
        product = Product(5, "Test", 50, 3)
        amount = ProductAmount(1, product, 3)
        self.assertEqual(amount.quantity, 3)

    def test_empty_order_total_is_zero(self):
        """Тест, що загальна сума порожнього замовлення — 0."""
        user = User(0, "Empty", "empty@email.com", "123")
        user.register()
        order = user.create_order()
        self.assertEqual(order.get_total_price(), 0.0)

    def test_product_availability_decreases_after_add(self):
        """Тест зменшення кількості товару після додавання в замовлення."""
        user = User(0, "Decrease", "decrease@email.com", "123")
        user.register()
        order = user.create_order()

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
