class User:
    """Клас, що представляє користувача магазину"""
    def __init__(self, user_id: int, user_name: str, email: str, password: str):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.orders = []

    def register(self, users_db):
        """Реєстрація користувача."""
        if self.email in users_db:
            return "Користувач з таким email вже існує."

        users_db[self.email] = self
        return "Реєстрація успішна!"

    def login(self, email, password, users_db):
        """Авторизація користувача."""
        user = users_db.get(email)
        if user is None:
            return "Користувача не знайдено."
        if user.password != password:
            return "Неправильний пароль."

        return f"Вхід успішний! Вітаємо, {user.user_name}."

    def create_order(self):
        """Створення нового замовлення"""
        order = Order(len(self.orders) + 1, self.user_id)
        self.orders.append(order)
        return order

    def get_orders(self):
        """Повертає список замовлень користувача"""
        return self.orders


class Order:
    """Клас, що представляє замовлення"""
    def __init__(self, order_id: int, user_id: int):
        self.order_id = order_id
        self.user_id = user_id
        self.order_items_list = []  # список ProductAmount
        self.status = "Pending"

    def add_product(self, product, quantity):
        """Додає товар до замовлення, якщо він доступний"""
        if not product.availability:
            return

        self.order_items_list.append(ProductAmount(self.order_id, product, quantity))

    def remove_product(self, product_id):
        """Видаляє товар із замовлення"""
        self.order_items_list = [item for item in self.order_items_list
                                 if item.product.product_id != product_id]

    def get_total_price(self):
        """Обчислює загальну суму замовлення"""
        return sum(item.quantity * item.get_product_price() for item in self.order_items_list)


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
    def __init__(self, product_id: int, product_name: str, price: float, availability: bool):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.availability = availability

    def get_product_info(self):
        """Повертає інформацію про товар"""
        return (f"{self.product_name}: {self.price} грн, "
                f"{'Є в наявності' if self.availability else 'Немає'}")
