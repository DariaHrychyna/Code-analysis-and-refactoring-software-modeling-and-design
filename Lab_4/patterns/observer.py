from abc import ABC, abstractmethod
from order import Order


class Observer(ABC):
    @abstractmethod
    def update(self, order: Order) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self, order: Order) -> None:
        pass


class Notifier(ABC):
    @abstractmethod
    def notify(self, order: Order) -> None:
        pass


class KitchenNotifier(Notifier, Observer):
    def update(self, order: Order) -> None:
        kitchen_categories = ["Сніданок", "Гаряча страва", "Закуска"]
        if any(dish.category in kitchen_categories for dish in order.dishes):
            print(f"[Кухар] Отримано нове замовлення від {order.customer.customer_name}.")

    def notify(self, order: Order) -> None:
        self.update(order)


class BaristaNotifier(Notifier, Observer):
    def update(self, order: Order) -> None:
        drink_categories = ["Напої"]
        if any(dish.category in drink_categories for dish in order.dishes):
            print(f"[Бариста] Отримано нове замовлення від {order.customer.customer_name}.")

    def notify(self, order: Order) -> None:
        self.update(order)


class OrderManager(Subject):
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self, order: Order) -> None:
        for observer in self._observers:
            observer.update(order)

    def create_order(self, order: Order) -> None:
        print("Замовлення створено.")
        self.notify_observers(order)
