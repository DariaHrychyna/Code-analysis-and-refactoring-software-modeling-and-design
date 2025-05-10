from order import Order


class Customer:
    def __init__(self, customer_name: str, email: str, phone_number: str):
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number
        self.orders: list[Order] = []

    def place_order(self, order: 'Order'):
        self.orders.append(order)
