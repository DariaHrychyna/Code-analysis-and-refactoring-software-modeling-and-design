import unittest
from main import Dish, Menu, Customer
from order import Order, OfflineOrder, OnlineOrder
from patterns.observer import  Notifier, KitchenNotifier


class TestRestaurant(unittest.TestCase):
    def test_create_dish(self):
        """Тест створення об'єкта Dish та перевірки його полів"""
        dish = Dish("Піца", 150.0, "Основна страва")
        self.assertEqual(dish.dish_name, "Піца")
        self.assertEqual(dish.price, 150.0)
        self.assertEqual(dish.category, "Основна страва")

    def test_create_customer(self):
        """Тест створення об'єкта Customer та перевірки полів"""
        customer = Customer("Адам", "adam@example.com", "0987654321")
        self.assertEqual(customer.customer_name, "Адам")
        self.assertEqual(customer.email, "adam@example.com")
        self.assertEqual(customer.phone_number, "0987654321")

    def test_add_dish_to_menu(self):
        """Тест додавання страви до меню"""
        menu = Menu()
        dish = Dish("Борщ", 80.0, "Суп")
        menu.add_dish_to_menu(dish)
        self.assertIn(dish, menu.get_dishes())

    def test_add_dish_to_order(self):
        """Тест додавання страви до замовлення"""
        customer = Customer("Ірина", "irina@example.com", "0977777777")
        order = OfflineOrder(customer)
        dish = Dish("Салат", 50.0, "Закуска")
        order.add_dish_to_order(dish)
        self.assertIn(dish, order.dishes)

    def test_order_total_price_single_dish(self):
        """Тест обчислення вартості замовлення з однієї страви"""
        customer = Customer("Анна", "anna@example.com", "0966666666")
        order = OfflineOrder(customer)
        order.add_dish_to_order(Dish("Пельмені", 90.0, "Основна страва"))
        self.assertEqual(order.calculate_total_price(), 90.0)

    def test_order_total_price_multiple_dishes(self):
        """Тест обчислення вартості замовлення з кількох страв"""
        customer = Customer("Богдан", "bogdan@example.com", "0933333333")
        order = OfflineOrder(customer)
        order.add_dish_to_order(Dish("Суп", 40.0, "Суп"))
        order.add_dish_to_order(Dish("Картопля з котлетою", 60.0, "Основна страва"))
        self.assertEqual(order.calculate_total_price(), 100.0)

    def test_create_order_for_customer(self):
        """Тест створення замовлення для конкретного клієнта"""
        customer = Customer("Олег", "oleg@example.com", "0999999999")
        order = OnlineOrder(customer)
        self.assertEqual(order.customer, customer)

    def test_place_order(self):
        """Тест розміщення замовлення клієнтом"""
        customer = Customer("Оля", "olya@example.com", "0951111111")
        order = OfflineOrder(customer)
        customer.place_order(order)
        self.assertIn(order, customer.orders)

    def test_multiple_orders_for_customer(self):
        """Тест обчислення вартості замовлення з кількох страв"""
        customer = Customer("Петро", "petro@example.com", "0911111111")
        order1 = OnlineOrder(customer)
        order2 = OfflineOrder(customer)
        customer.place_order(order1)
        customer.place_order(order2)
        self.assertEqual(len(customer.orders), 2)

    def test_menu_multiple_dishes(self):
        """Тест додавання кількох страв у меню"""
        menu = Menu()
        d1 = Dish("Омлет", 45.0, "Сніданок")
        d2 = Dish("Каша", 35.0, "Сніданок")
        menu.add_dish_to_menu(d1)
        menu.add_dish_to_menu(d2)
        self.assertEqual(len(menu.get_dishes()), 2)

    def test_online_order_uses_discount_strategy(self):
        customer = Customer("Юрій", "yurii@example.com", "0935555555")
        order = OnlineOrder(customer)
        order.add_dish_to_order(Dish("Кава", 40.0, "Напій"))
        self.assertLess(order.calculate_total_price(), 40.0)

    def test_total_price_empty_order(self):
        customer = Customer("Ілля", "illya@example.com", "0959999999")
        order = OfflineOrder(customer)
        self.assertEqual(order.calculate_total_price(), 0.0)


if __name__ == '__main__':
    unittest.main()
