import unittest
from Business.book import Book
from Business.book_factory import BookFactory
from Business.customer import Customer
from Business.order import Order
from Business.order_item import OrderItem
from Business.delivery_strategy import CourierDelivery, SelfPickupDelivery
from Business.payment_strategy import OnlinePayment, CashOnDelivery


class TestBookstore(unittest.TestCase):
    def test_book_creation(self):
        """Перевіряє правильність створення книги."""
        book = Book(1, "1984", "George Orwell", 100.0)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.price, 100.0)

    def test_book_factory(self):
        """Перевіряє роботу фабрики створення книг."""
        book = BookFactory.create_book("Brave New World", "Aldous Huxley", 150.0)
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "Brave New World")

    def test_customer_and_order_creation(self):
        """Перевіряє створення користувача та замовлення, і додавання замовлення в історію."""
        customer = Customer(1, "Alice", "alice@gmail.com")
        order = customer.create_order()
        self.assertEqual(len(customer.get_order_history()), 1)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.customer.name, "Alice")

    def test_add_order_item_and_total(self):
        """Перевіряє додавання товару в замовлення та обчислення загальної суми."""
        book = Book(1, "Dune", "Frank Herbert", 200.0)
        item = OrderItem(book, 2)
        order = Order(Customer(1, "Bob", "bob@gmail.com"))
        order.add_item(item)
        self.assertAlmostEqual(order.calculate_total(), 400.0)

    def test_online_payment_strategy(self):
        """Перевіряє роботу стратегії онлайн-оплати."""
        payment = OnlinePayment(250.0)
        self.assertEqual(payment.process_payment(), "Виконується онлайн оплата  250.00")

    def test_cash_on_delivery_strategy(self):
        """Перевіряє роботу стратегії оплати при отриманні."""
        payment = CashOnDelivery(180.0)
        self.assertEqual(payment.process_payment(), "Оплата  180.00 буде виконана після отримання товару")

    def test_set_payment_strategy(self):
        """Перевіряє встановлення стратегії оплати для замовлення."""
        order = Order(Customer(1, "John", "john@example.com"))
        payment = OnlinePayment(100.0)
        order.set_payment(payment)
        self.assertIs(order.payment, payment)

    def test_delivery_strategy_courier(self):
        """Перевіряє доставку кур'єром."""
        order = Order(Customer(1, "Test", "t@t.com"))
        delivery = CourierDelivery()
        result = delivery.deliver(order)
        self.assertIn("кур'єром", result)

    def test_delivery_strategy_selfpickup(self):
        """Перевіряє самовивіз користувачем."""
        order = Order(Customer(2, "Anna", "anna@gmail.com"))
        delivery = SelfPickupDelivery()
        result = delivery.deliver(order)
        self.assertIn("особисто користувачем", result)

    def test_multiple_order_items_total(self):
        """Перевіряє обчислення загальної суми для кількох товарів у замовленні."""
        book1 = Book(1, "Book A", "Author A", 50.0)
        book2 = Book(2, "Book B", "Author B", 75.0)
        item1 = OrderItem(book1, 1)
        item2 = OrderItem(book2, 2)
        order = Order(Customer(3, "Liam", "liam@example.com"))
        order.add_item(item1)
        order.add_item(item2)
        self.assertAlmostEqual(order.calculate_total(), 200.0)


if __name__ == '__main__':
    unittest.main()
