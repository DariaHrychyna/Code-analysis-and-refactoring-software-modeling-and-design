import sqlite3
from datetime import datetime


class Order:
    def __init__(self, order_id, customer_info):
        self.order_id = order_id
        self.customer_name = customer_info["Прізвище клієнта"]
        self.product_name = customer_info["Назва товару"]
        self.quantity = customer_info["Кількість"]
        self.price = customer_info["Вартість"]
        self.order_date = datetime.strptime(customer_info["Дата замовлення"], "%Y-%m-%d")

    def __str__(self):
        return (f"Order ID: {self.order_id}, Customer: {self.customer_name}, Product: {self.product_name}, "
                f"Quantity: {self.quantity}, Price: {self.price}, Date: {self.order_date.strftime('%Y-%m-%d')}")


class OrderManager:
    def __init__(self):
        self.orders = {}
        self.conn = sqlite3.connect('orders.db')
        self.create_table()
        self.load_orders()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS orders (
                                order_id INTEGER PRIMARY KEY,
                                customer_name TEXT NOT NULL,
                                product_name TEXT NOT NULL,
                                quantity INTEGER NOT NULL,
                                price REAL NOT NULL,
                                order_date TEXT NOT NULL)''')

    def load_orders(self):
        with self.conn:
            rows = self.conn.execute("SELECT * FROM orders").fetchall()
            for row in rows:
                order_id, customer_name, product_name, quantity, price, order_date = row
                self.orders[order_id] = Order(order_id, {
                    "Прізвище клієнта": customer_name,
                    "Назва товару": product_name,
                    "Кількість": quantity,
                    "Вартість": price,
                    "Дата замовлення": order_date
                })

    def add_order(self, order_id, customer_info):
        with self.conn:
            existing_order = self.conn.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,)).fetchone()
            if existing_order:
                print(f"Order ID {order_id} already exists in the database.")
                return

        order = Order(order_id, customer_info)

        with self.conn:
            self.conn.execute('''INSERT INTO orders (order_id, customer_name, product_name, quantity, price, order_date)
                                 VALUES (?, ?, ?, ?, ?, ?)''',
                              (order_id, order.customer_name, order.product_name, order.quantity, order.price,
                               order.order_date.strftime('%Y-%m-%d')))

        # Тепер додаємо до self.orders
        self.orders[order_id] = order
        print(f"Order {order_id} added successfully.")

    def remove_order(self, order_id):
        with self.conn:
            if order_id in self.orders:
                del self.orders[order_id]
                self.conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
                print(f"Order {order_id} removed successfully.")
            else:
                print(f"Order ID {order_id} not found.")

    def find_order(self, customer_name=None, product_name=None, quantity=None):
        query = "SELECT * FROM orders WHERE 1=1"
        params = []

        if customer_name:
            query += " AND customer_name = ?"
            params.append(customer_name)
        if product_name:
            query += " AND product_name = ?"
            params.append(product_name)
        if quantity is not None:
            query += " AND quantity = ?"
            params.append(quantity)

        with self.conn:
            rows = self.conn.execute(query, params).fetchall()

        if rows:
            for row in rows:
                print(Order(row[0], {
                    "Прізвище клієнта": row[1],
                    "Назва товару": row[2],
                    "Кількість": row[3],
                    "Вартість": row[4],
                    "Дата замовлення": row[5]
                }))
        else:
            print("No matching orders found.")

    def get_order_by_id(self, order_id):
        order = self.orders.get(order_id)
        if order:
            return order
        else:
            return None

    def show_all_orders(self):
        with self.conn:
            rows = self.conn.execute("SELECT * FROM orders").fetchall()
            if rows:
                print(f"{'Order ID':<10} {'Customer Name':<25} {'Product Name':<30} {'Quantity':<10} {'Price':<10} {'Order Date':<15}")
                print("=" * 120)
                for row in rows:
                    print(f"{row[0]:<10} {row[1]:<25} {row[2]:<30} {row[3]:<10} {row[4]:<10} {row[5]:<15}")
            else:
                print("No orders found.")


def user_interface():
    manager = OrderManager()
    while True:
        print("\nВиберіть дію:")
        print("1. Додати нове замовлення")
        print("2. Видалити замовлення")
        print("3. Шукати замовлення")
        print("4. Отримати замовлення за номером")
        print("5. Вивести всі замовлення")
        print("6. Вийти")

        choice = input("Введіть номер дії: ")

        if choice == "1":
            order_id = int(input("Введіть ID замовлення: "))
            customer_info = {
                "Прізвище клієнта": input("Введіть прізвище клієнта: "),
                "Назва товару": input("Введіть назву товару: "),
                "Кількість": int(input("Введіть кількість товару: ")),
                "Вартість": float(input("Введіть вартість товару: ")),
                "Дата замовлення": input("Введіть дату замовлення (YYYY-MM-DD): ")
            }
            manager.add_order(order_id, customer_info)

        elif choice == "2":
            order_id = int(input("Введіть ID замовлення для видалення: "))
            manager.remove_order(order_id)

        elif choice == "3":
            print("\nВиберіть параметр для пошуку замовлення:")
            print("1. Прізвище клієнта")
            print("2. Назва товару")
            print("3. Дата замовлення")
            search_choice = input("Введіть номер параметра: ")
            criteria = {}

            if search_choice == "1":
                customer_name = input("Введіть прізвище клієнта: ")
                criteria["customer_name"] = customer_name
            elif search_choice == "2":
                product_name = input("Введіть назву товару: ")
                criteria["product_name"] = product_name
            elif search_choice == "3":
                date_str = input("Введіть дату замовлення (YYYY-MM-DD): ")
                criteria["order_date"] = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                print("Неправильний вибір. Спробуйте ще раз.")
                continue

            manager.find_order(**criteria)

        elif choice == "4":
            order_id = int(input("Введіть ID замовлення для отримання інформації: "))
            manager.get_order_by_id(order_id)

        elif choice == "5":
            manager.show_all_orders()

        elif choice == "6":
            print("Завершення роботи.")
            break

        else:
            print("Неправильний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    user_interface()

