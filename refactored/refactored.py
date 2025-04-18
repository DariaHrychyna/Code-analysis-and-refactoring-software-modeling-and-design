from create_refactored_db import create_tables, seed_products, get_connection
import sqlite3
from enum import Enum
import re


# 1. Extract Class
class AuthService:
    """Клас, що відповідає за реєстрацію та авторизацію користувача."""
    @staticmethod
    def register(user_name, email, password):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute('INSERT INTO users (user_name, email, password) VALUES (?, ?, ?)',
                        (user_name, email, password))
            conn.commit()
            user_id = cur.lastrowid
            return "Реєстрація успішна!", user_id
        except sqlite3.IntegrityError:
            return "Користувач з таким email вже існує.", None
        finally:
            conn.close()

    @staticmethod
    def login(email, password):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT id, user_name, email, password FROM users WHERE email = ?', (email,))
        row = cur.fetchone()
        conn.close()

        if not row or row[3] != password:   # 9. Consolidate Duplicate Conditional Fragments
            return None, "Неправильний email чи пароль."

        return User(row[0], row[1], row[2], row[3]), f"Вхід успішний! Вітаємо, {row[1]}."


class OrderStatus(Enum):  # 6. Replace Type Code with Class
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class User:
    """Клас, що представляє користувача магазину"""

    def __init__(self, user_id: int, user_name: str, email: str, password: str):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self._password = password  # 5. Encapsulate Field
        self.orders = []

    def get_password(self):  # 5. Encapsulate Field - використано
        """Геттер для пароля"""
        return self._password

    def set_password(self, password):  # 5. Encapsulate Field - використано
        """Сеттер для пароля"""
        self._password = password

    def place_new_order(self):  # 3. Rename Method
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO orders (user_id) VALUES (?)', (self.user_id,))
        conn.commit()
        order_id = cur.lastrowid
        conn.close()

        order = Order.create_new_order(order_id, self.user_id)  # 8. Replace Constructor with Factory Method
        self.orders.append(order)
        return order

    def get_orders(self):
        """Завантажує замовлення користувача з бази даних, з нумерацією для кожного користувача"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM orders WHERE user_id = ?", (self.user_id,))
        order_rows = cur.fetchall()

        orders = []
        for row in order_rows:
            order_id = row[0]
            order = Order.create_new_order(order_id, self.user_id)  # 8. Replace Constructor with Factory Method

            cur.execute("""SELECT products.id, products.name, products.price, products.availability, order_items.quantity
                           FROM order_items
                           JOIN products ON order_items.product_id = products.id
                           WHERE order_items.order_id = ?""", (order_id,))
            product_rows = cur.fetchall()

            for prod_id, name, price, availability, quantity in product_rows:
                product = Product(prod_id, name, price, availability)
                order.order_items.append(ProductAmount(order_id, product, quantity))

            orders.append(order)

        conn.close()
        return orders


class Order:
    """Клас, що представляє замовлення"""
    def __init__(self, order_id: int, user_id: int):
        self.order_id = order_id
        self.user_id = user_id
        self.order_items = []  # 4. Rename Variable
        self.status = OrderStatus.PENDING  # 6. Replace Type Code with Class

    @classmethod
    def create_new_order(cls, order_id: int, user_id: int):  # 8. Replace Constructor with Factory Method
        return cls(order_id, user_id)

    def add_product(self, product, quantity):
        if not product.availability or quantity <= 0:
            print("Товар недоступний або неправильна кількість.")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT availability FROM products WHERE id = ?", (product.product_id,))
        available = cur.fetchone()[0]
        if available < quantity:
            print(f"Недостатньо товару на складі. В наявності: {available}")
            conn.close()
            return

        cur.execute('INSERT INTO order_items (order_id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)',
                    (self.order_id, self.user_id, product.product_id, quantity))

        cur.execute('UPDATE products SET availability = availability - ? WHERE id = ?',
                    (quantity, product.product_id))

        conn.commit()
        conn.close()

        self.order_items.append(ProductAmount(self.order_id, product, quantity))

# 10. Remove Dead Code - видалено метод remove_product

    def get_total_price(self):
        """Обчислює загальну суму замовлення"""
        return sum(item.quantity * item.product.price for item in self.order_items)

    def show_order(self):
        for item in self.order_items:
            print(f"{item.product.product_name} x {item.quantity} = {item.product.price * item.quantity} грн")
        print(f"Загальна сума: {self.get_total_price()} грн")

    def get_product_names(self):  # 7. Hide Delegate
        """Отримує імена всіх товарів у замовленні"""
        return [item.product.product_name for item in self.order_items]


class ProductAmount:
    """Зв'язує товар із його кількістю в замовленні"""
    def __init__(self, order_id: int, product, quantity: int):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity

# 2. Inline Method - get_product_price() замінено прямим доступом до product.price


class Product:
    """Клас, що представляє товар у магазині"""
    def __init__(self, product_id, product_name, price, availability):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.availability = availability

    def get_product_info(self):
        return (f"{self.product_id}. {self.product_name}: {self.price} грн, "
                f"{'Є в наявності' if self.availability > 0 else 'Немає'}"
                f"{f' ({self.availability})' if self.availability > 0 else ''}")

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, price, availability FROM products")
        rows = cur.fetchall()
        conn.close()
        return [Product(id_, name, price, availability) for id_, name, price, availability in rows]


def is_valid_gmail(email):
    pattern = r'^[\w\.-]+@gmail\.com$'
    return re.match(pattern, email) is not None


# ==== додатковий код для роботи ==== 11. Extract Function
def show_main_menu():
    print("\n--- ГОЛОВНЕ МЕНЮ ---")
    print("1. Зареєструватися")
    print("2. Увійти")
    print("3. Вийти з програми")


def show_user_menu(user_name):
    print(f"\n--- МЕНЮ КОРИСТУВАЧА ({user_name}) ---")
    print("1. Створити нове замовлення")
    print("2. Переглянути мої замовлення")
    print("3. Вийти з акаунта")


def handle_registration():
    name = input("Ім'я: ")
    email = input("Email: ")
    if not is_valid_gmail(email):
        print("Некоректний email. Потрібно ввести дійсну адресу @gmail.com.")
        return None
    password = input("Пароль: ")
    message, user_id = AuthService.register(name, email, password)
    print(message)
    if user_id:
        return User(user_id, name, email, password)
    return None


def handle_login():
    email = input("Email: ")
    password = input("Пароль: ")
    user, message = AuthService.login(email, password)
    print(message)
    return user


def handle_order_creation(user):
    order = user.place_new_order()
    while True:
        products = Product.get_all()  # 12. Move Function
        print("\n--- ДОДАВАННЯ ТОВАРІВ ДО ЗАМОВЛЕННЯ ---")
        for p in products:
            print(p.get_product_info())

        product_id_input = input("Введіть ID товару (або 'done' для завершення): ")
        if product_id_input.lower() == 'done':
            break
        try:
            product_id = int(product_id_input)
            quantity = int(input("Кількість: "))
            if quantity <= 0:
                print("Кількість має бути більшою за нуль.")
                continue
            selected_product = next((p for p in products if p.product_id == product_id), None)
            if selected_product:
                order.add_product(selected_product, quantity)
            else:
                print("Товар не знайдений.")
        except ValueError:
            print("Некоректний ввід.")

    order.show_order()


def handle_view_orders(user):
    print("\nМої замовлення:")
    orders = user.get_orders()
    if not orders:
        print("У вас ще немає замовлень.")
    else:
        for idx, order in enumerate(orders, 1):
            print(f"Замовлення #{idx}, Статус: {order.status.value}")
            order.show_order()


def main():
    create_tables()
    seed_products()
    current_user = None

    while True:
        if current_user is None:
            show_main_menu()
            choice = input("Оберіть дію: ")
            if choice == '1':
                current_user = handle_registration()
            elif choice == '2':
                current_user = handle_login()
            elif choice == '3':
                print("До побачення!")
                break
            else:
                print("Невірна опція!")
        else:
            show_user_menu(current_user.user_name)
            choice = input("Оберіть дію: ")
            if choice == '1':
                handle_order_creation(current_user)
            elif choice == '2':
                handle_view_orders(current_user)
            elif choice == '3':
                current_user = None
            else:
                print("Невірна опція!")


if __name__ == '__main__':
    main()

