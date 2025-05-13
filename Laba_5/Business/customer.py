from Business.order import Order


class Customer:
    def __init__(self, customer_id: int, name: str, email: str):
        self.id = customer_id
        self.name = name
        self.email = email
        self._order_history: list[Order] = []

    def create_order(self) -> Order:
        order = Order(self)
        self._order_history.append(order)
        return order

    def get_order_history(self) -> list[Order]:
        return self._order_history
