from order import OfflineOrder, OnlineOrder
from customer import Customer


class OrderFactory:
    @staticmethod
    def create_order(customer: Customer, order_type: str):
        if order_type == "offline":
            return OfflineOrder(customer)
        elif order_type == "online":
            return OnlineOrder(customer)
        else:
            raise ValueError("Невідомий тип замовлення")

