from create_original_db import create_tables, seed_products, get_connection
import sqlite3


class User:
    """Клас, що представляє користувача магазину"""
    def __init__(self, user_id: int, user_name: str, email: str, password: str):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.orders = []

    def register(self):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute('INSERT INTO users (user_name, email, password) VALUES (?, ?, ?)',
                        (self.user_name, self.email, self.password))
            conn.commit()
            self.user_id = cur.lastrowid
            return "Реєстрація успішна!"
        except sqlite3.IntegrityError:
            return "Користувач з таким email вже існує."
        finally:
            conn.close()

    @staticmethod
    def login(email, password):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT id, user_name, email, password FROM users WHERE email = ?', (email,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None, "Користувача не знайдено."
        if row[3] != password:
            return None, "Неправильний пароль."

        user = User(row[0], row[1], row[2], row[3])
        return user, f"Вхід успішний! Вітаємо, {user.user_name}."

    def create_order(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO orders (user_id) VALUES (?)', (self.user_id,))
        conn.commit()
        order_id = cur.lastrowid
        conn.close()

        order = Order(order_id, self.user_id)
        self.orders.append(order)
        return order

    def get_orders(self):
        """Завантажує замовлення користувача з бази даних"""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM orders WHERE user_id = ?", (self.user_id,))
        order_rows = cur.fetchall()

        orders = []
        for row in order_rows:
            order_id = row[0]
            order = Order(order_id, self.user_id)

            # Завантажити товари для кожного замовлення
            cur.execute("""
                SELECT products.id, products.name, products.price, products.availability, order_items.quantity
                FROM order_items
                JOIN products ON order_items.product_id = products.id
                WHERE order_items.order_id = ?
            """, (order_id,))
            product_rows = cur.fetchall()

            for prod_id, name, price, availability, quantity in product_rows:
                product = Product(prod_id, name, price, availability)
                order.order_items_list.append(ProductAmount(order_id, product, quantity))

            orders.append(order)

        conn.close()
        return orders


class Order:
    """Клас, що представляє замовлення"""
    def __init__(self, order_id: int, user_id: int):
        self.order_id = order_id
        self.user_id = user_id
        self.order_items_list = []  # список ProductAmount
        self.status = "Pending"

    def add_product(self, product, quantity):
        if not product.availability or quantity <= 0:
            print("Товар недоступний або неправильна кількість.")
            return

        conn = get_connection()
        cur = conn.cursor()

        # Отримати кількість товару
        cur.execute("SELECT availability FROM products WHERE id = ?", (product.product_id,))
        available = cur.fetchone()[0]
        if available < quantity:
            print(f"Недостатньо товару на складі. В наявності: {available}")
            conn.close()
            return

        # Додати в order_items
        cur.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (self.order_id, product.product_id, quantity))

        # Оновити кількість на складі
        cur.execute('UPDATE products SET availability = availability - ? WHERE id = ?',
                    (quantity, product.product_id))

        conn.commit()
        conn.close()

        self.order_items_list.append(ProductAmount(self.order_id, product, quantity))

    def remove_product(self, product_id):
        """Видаляє товар із замовлення"""
        self.order_items_list = [item for item in self.order_items_list
                                 if item.product.product_id != product_id]

    def get_total_price(self):
        """Обчислює загальну суму замовлення"""
        return sum(item.quantity * item.get_product_price() for item in self.order_items_list)

    def show_order(self):
        for item in self.order_items_list:
            print(f"{item.product.product_name} x {item.quantity} = {item.get_product_price() * item.quantity} грн")
        print(f"Загальна сума: {self.get_total_price()} грн")


class ProductAmount:
    """Зв'язує товар із його кількістю в замовленні"""
    def __init__(self, order_id: int, product, quantity: int):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity

    def get_product_price(self):
        """Отримує реальну ціну товару"""
        return self.product.price


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


# ==== додатковий код для роботи ====

def main():
    create_tables()
    seed_products()
    current_user = None

    def get_all_products():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, price, availability FROM products")
        rows = cur.fetchall()
        conn.close()
        return [Product(id_, name, price, availability) for id_, name, price, availability in rows]

    while True:
        if current_user is None:
            print("\n--- ГОЛОВНЕ МЕНЮ ---")
            print("1. Зареєструватися")
            print("2. Увійти")
            print("3. Вийти з програми")

            choice = input("Оберіть дію: ")

            if choice == '1':
                name = input("Ім'я: ")
                email = input("Email: ")
                if "@" not in email:
                    print("Некоректний email. Повинен містити символ '@'.")
                    continue
                password = input("Пароль: ")
                user = User(0, name, email, password)
                print(user.register())

            elif choice == '2':
                email = input("Email: ")
                password = input("Пароль: ")
                user, message = User.login(email, password)
                if user:
                    current_user = user
                    print(message)
                else:
                    print(message)

            elif choice == '3':
                print("До побачення!")
                break

            else:
                print("Невірна опція!")

        else:
            print(f"\n--- МЕНЮ КОРИСТУВАЧА ({current_user.user_name}) ---")
            print("1. Створити нове замовлення")
            print("2. Переглянути мої замовлення")
            print("3. Вийти з акаунта")

            choice = input("Оберіть дію: ")

            if choice == '1':
                order = current_user.create_order()
                while True:
                    products = get_all_products()
                    print("\n--- ДОДАВАННЯ ТОВАРІВ ДО ЗАМОВЛЕННЯ ---")
                    for p in products:
                        print(p.get_product_info())

                    product_id = input("Введіть ID товару (або 'done' для завершення): ")
                    if product_id == 'done':
                        break

                    product = next((p for p in products if str(p.product_id) == product_id), None)
                    if not product:
                        print("Товар не знайдено.")
                        continue

                    quantity = int(input("Кількість: "))
                    order.add_product(product, quantity)

                print("\n--- ПІДСУМОК ЗАМОВЛЕННЯ ---")
                order.show_order()

            elif choice == '2':
                orders = current_user.get_orders()
                if not orders:
                    print("У вас ще немає замовлень.")
                else:
                    for order in orders:
                        print(f"\n")
                        order.show_order()

            elif choice == '3':
                print(f"До побачення, {current_user.user_name}!")
                current_user = None
            else:
                print("Невірна опція!")


if __name__ == "__main__":
    main()
