from abc import ABC, abstractmethod
from Business.order import Order


class DeliveryStrategy(ABC):
    @abstractmethod
    def deliver(self, order: Order) -> str:
        pass


class CourierDelivery(DeliveryStrategy):
    def deliver(self, order: Order) -> str:
        return f"Замовлення {order.id} буде надіслано кур'єром."


class SelfPickupDelivery(DeliveryStrategy):
    def deliver(self, order: Order) -> str:
        return f"Замовлення {order.id} буде отримано особисто користувачем."
