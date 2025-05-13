from Business.order_item import OrderItem
from Business.payment_strategy import PaymentStrategy


class Order:
    _id_counter = 1

    def __init__(self, customer):
        self.id = Order._id_counter
        Order._id_counter += 1

        self.customer = customer
        self.items: list[OrderItem] = []
        self.payment: PaymentStrategy = None

    def add_item(self, item: OrderItem):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.get_total_price() for item in self.items)

    def set_payment(self, payment: PaymentStrategy):
        self.payment = payment

