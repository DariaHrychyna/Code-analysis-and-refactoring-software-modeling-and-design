from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    def __init__(self, amount: float):
        self.amount = amount

    @abstractmethod
    def process_payment(self) -> str:
        pass


class OnlinePayment(PaymentStrategy):
    def process_payment(self) -> str:
        return f"Виконується онлайн оплата {self.amount: .2f}"


class CashOnDelivery(PaymentStrategy):
    def process_payment(self) -> str:
        return f"Оплата {self.amount: .2f} буде виконана після отримання товару"
