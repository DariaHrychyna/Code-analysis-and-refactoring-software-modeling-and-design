import unittest
from main import User, Order, Product, ProductAmount


class TestStore(unittest.TestCase):

    def setUp(self):
        """Створення початкових об'єктів для тестів"""
        self.user = User(user_id=1, user_name="TestUser", email="test@example.com", password="password123")
        self.product = Product(product_id=101, product_name="Laptop", price=1000.0, availability=True)
        self.product1 = Product(product_id=102, product_name="Mouse", price=50.0, availability=True)
        self.product2 = Product(product_id=103, product_name="Keyboard", price=150.0, availability=True)
        self.order = Order(order_id=1, user_id=self.user.user_id)

    def test_register_user(self):
        """Перевірка реєстрації користувача"""
        new_user = User(user_id=2, user_name="NewUser", email="new@example.com", password="password123")
        self.assertEqual(new_user.user_name, "NewUser")
        self.assertEqual(new_user.email, "new@example.com")

    def test_create_order(self):
        """Перевірка створення замовлення користувачем"""
        order = self.user.create_order()
        self.assertEqual(len(self.user.get_orders()), 1)
        self.assertEqual(order.status, "Pending")

    def test_add_product_to_order(self):
        """Перевірка додавання товару до замовлення"""
        self.order.add_product(self.product, quantity=2)
        self.assertEqual(len(self.order.order_items_list), 1)
        self.assertIsInstance(self.order.order_items_list[0], ProductAmount)
        self.assertEqual(self.order.order_items_list[0].quantity, 2)
        self.assertEqual(self.order.order_items_list[0].product, self.product)

    def test_add_multiple_products_to_order(self):
        """Перевірка додавання кількох продуктів у замовлення"""
        self.order.add_product(self.product1, quantity=1)
        self.order.add_product(self.product2, quantity=3)
        self.assertEqual(len(self.order.order_items_list), 2)
        self.assertEqual(self.order.get_total_price(), 500.0)

    def test_add_product_when_unavailable(self):
        """Перевірка додавання товару, якщо товар недоступний"""
        unavailable_product = Product(product_id=104, product_name="Tablet", price=300.0, availability=False)
        self.order.add_product(unavailable_product, quantity=1)
        self.assertEqual(len(self.order.order_items_list), 0)

    def test_add_product_with_excess_quantity(self):
        """Перевірка додавання товару з кількістю, яка перевищує наявну"""
        self.product.availability = False
        self.order.add_product(self.product, quantity=10)
        self.assertEqual(len(self.order.order_items_list), 0)

    def test_add_large_quantity_of_product(self):
        """Перевірка додавання великої кількості товару"""
        self.order.add_product(self.product, quantity=1000000)
        self.assertEqual(self.order.get_total_price(),
                         1000000 * self.product.price)

    def test_get_total_price(self):
        """Перевірка обчислення загальної вартості замовлення"""
        self.order.add_product(self.product, quantity=2)
        self.assertEqual(self.order.get_total_price(), 2000.0)

    def test_remove_product(self):
        """Перевірка видалення товару із замовлення"""
        self.order.add_product(self.product, quantity=2)
        self.order.remove_product(self.product.product_id)
        self.assertEqual(len(self.order.order_items_list), 0)

    def test_remove_nonexistent_product(self):
        """Перевірка видалення продукту, якого немає в замовленні"""
        initial_count = len(self.order.order_items_list)
        self.order.remove_product(self.product1)
        self.assertEqual(len(self.order.order_items_list), initial_count)

    def test_create_multiple_orders(self):
        """Перевірка створення кількох замовлень одним користувачем"""
        order1 = self.user.create_order()
        order2 = self.user.create_order()
        self.assertEqual(len(self.user.get_orders()), 2)
        self.assertNotEqual(order1.order_id, order2.order_id)

    def test_product_availability(self):
        """Перевірка доступності товару"""
        self.assertTrue(self.product.availability)

    def test_order_status_change(self):
        """Перевірка зміни статусу замовлення"""
        self.order.status = "Shipped"
        self.assertEqual(self.order.status, "Shipped")


if __name__ == "__main__":
    unittest.main()
