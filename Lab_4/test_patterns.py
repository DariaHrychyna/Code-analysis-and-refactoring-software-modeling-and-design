import unittest
from customer import Customer
from dish import Dish
from patterns.singleton import OrderDatabase
from patterns.factory import OrderFactory
from patterns.observer import OrderManager, KitchenNotifier, BaristaNotifier
from patterns.strategy import RegularPricing, DiscountPricing
from order import OfflineOrder, OnlineOrder


class TestSingletonPattern(unittest.TestCase):

    def test_single_instance_created(self):
        """Перевіряє, що Singleton створює лише один екземпляр."""
        db1 = OrderDatabase()
        db2 = OrderDatabase()
        self.assertIs(db1, db2)

    def test_order_added_once(self):
        """Перевіряє, що доданий запис зберігається в Singleton-об'єкті."""
        db = OrderDatabase()
        db.orders.clear()
        db.add_order("Test Order 1")
        self.assertEqual(len(db.get_all_orders()), 1)

    def test_orders_persist_across_instances(self):
        """Перевіряє, що дані зберігаються між різними екземплярами Singleton."""
        db1 = OrderDatabase()
        db2 = OrderDatabase()
        db1.add_order("Test Order 2")
        self.assertIn("Test Order 2", db2.get_all_orders())


class TestFactoryPattern(unittest.TestCase):

    def test_create_offline_order(self):
        """Перевіряє, що фабрика створює OfflineOrder."""
        customer = Customer("Іван", "ivan@email.com", "123456")
        order = OrderFactory.create_order(customer, "offline")
        self.assertIsInstance(order, OfflineOrder)

    def test_create_online_order(self):
        """Перевіряє, що фабрика створює OnlineOrder."""
        customer = Customer("Олена", "olena@email.com", "654321")
        order = OrderFactory.create_order(customer, "online")
        self.assertIsInstance(order, OnlineOrder)

    def test_invalid_order_type_raises_error(self):
        """Перевіряє, що при неправильному типі замовлення викидається помилка."""
        customer = Customer("Ігор", "ihor@email.com", "987654")
        with self.assertRaises(ValueError):
            OrderFactory.create_order(customer, "unknown")


class TestObserverPattern(unittest.TestCase):

    def setUp(self):
        self.manager = OrderManager()
        self.kitchen = KitchenNotifier()
        self.barista = BaristaNotifier()
        self.customer = Customer("Тест", "test@email.com", "000000")

    def test_attach_observer(self):
        """Перевіряє, що спостерігач додається до списку."""
        self.manager.attach(self.kitchen)
        self.assertIn(self.kitchen, self.manager._observers)

    def test_detach_observer(self):
        """Перевіряє, що спостерігач успішно видаляється."""
        self.manager.attach(self.kitchen)
        self.manager.detach(self.kitchen)
        self.assertNotIn(self.kitchen, self.manager._observers)

    def test_notify_observers_prints(self):
        """Перевіряє, що при створенні замовлення всі спостерігачі отримують повідомлення."""
        self.manager.attach(self.kitchen)
        self.manager.attach(self.barista)
        order = OfflineOrder(self.customer)
        order.add_dish_to_order(Dish("Борщ", 80, "Гаряча страва"))
        self.manager.create_order(order)


class TestStrategyPattern(unittest.TestCase):

    def setUp(self):
        self.dishes = [
            Dish("Салат", 30, "Закуска"),
            Dish("Чай", 10, "Напої")
        ]

    def test_regular_pricing(self):
        """Перевіряє правильність розрахунку загальної вартості без знижки."""
        pricing = RegularPricing()
        total = pricing.calculate_total(self.dishes)
        self.assertEqual(total, 40)

    def test_discount_pricing(self):
        """Перевіряє правильність розрахунку загальної вартості зі знижкою."""
        pricing = DiscountPricing()
        total = pricing.calculate_total(self.dishes)
        self.assertEqual(total, 36)

    def test_strategy_change_runtime(self):
        """Перевіряє зміну стратегії ціноутворення під час виконання."""
        customer = Customer("Марія", "maria@email.com", "112233")
        order = OfflineOrder(customer)
        for dish in self.dishes:
            order.add_dish_to_order(dish)
        order.pricing_strategy = DiscountPricing()
        self.assertEqual(order.calculate_total_price(), 36)


if __name__ == "__main__":
    unittest.main()
