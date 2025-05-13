from Business.book_factory import BookFactory
from Business.customer import Customer
from Business.order_item import OrderItem
from Business.payment_strategy import OnlinePayment, CashOnDelivery
from Business.delivery_strategy import CourierDelivery, SelfPickupDelivery
from Business.book import Book
from Data.database import Database


def show_books(books: list[Book]):
    print("\nСписок книг:")
    for book in books:
        print(f"{book.id}.{book.get_info()}")
    print()


def admin_menu(db: Database, books: list[Book]):
    while True:
        print("\n--- Адмін меню ---")
        print("1. Додати книгу")
        print("2. Переглянути книги")
        print("3. Видалити книгу")
        print("4. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            title = input("Назва книги: ")
            author = input("Автор: ")
            price = float(input("Ціна: "))
            new_book = BookFactory.create_book(title, author, price)
            db.insert_book(new_book)
            books = db.get_all_books()
            print("Книгу додано.")
        elif choice == "2":
            show_books(books)
        elif choice == "3":
            show_books(books)
            book_id = int(input("Введіть ID книги для видалення: "))
            book_to_remove = next((b for b in books if b.id == book_id), None)
            if book_to_remove:
                books.remove(book_to_remove)
                print("Книгу видалено.")
            else:
                print("Книгу не знайдено.")
        elif choice == "4":
            break
        else:
            print("Невірний вибір.")


def user_menu(db: Database, customer: Customer, books: list[Book]):
    current_order = None
    while True:
        print("\n--- Меню користувача ---")
        print("1. Переглянути книги")
        print("2. Додати книгу до замовлення")
        print("3. Переглянути замовлення")
        print("4. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            show_books(books)
        elif choice == "2":
            if current_order is None:
                current_order = customer.create_order()

            show_books(books)
            book_id = int(input("Введіть ID книги: "))
            quantity = int(input("Кількість: "))

            book = next((b for b in books if b.id == book_id), None)
            if book:
                current_order.add_item(OrderItem(book, quantity))
                print("Книгу додано до замовлення.")
            else:
                print("Книгу не знайдено.")
        elif choice == "3":
            if not current_order or not current_order.items:
                print("Немає активного замовлення.")
                continue

            total = current_order.calculate_total()
            print(f"\nЗагальна сума: {total:.2f}")

            print("\nОберіть метод оплати:")
            print("1. Онлайн")
            print("2. При отриманні")
            p_choice = input("Вибір: ")

            if p_choice == "1":
                payment = OnlinePayment(total)
            else:
                payment = CashOnDelivery(total)

            current_order.set_payment(payment)
            print(payment.process_payment())

            print("\nОберіть спосіб доставки:")
            print("1. Кур'єр")
            print("2. Самовивіз")
            d_choice = input("Вибір: ")

            if d_choice == "1":
                delivery = CourierDelivery()
            else:
                delivery = SelfPickupDelivery()

            print(delivery.deliver(current_order))
            db.insert_order(current_order, payment.__class__.__name__)
            print("Замовлення збережено.")
            current_order = None
        elif choice == "4":
            break
        else:
            print("Невірний вибір.")


def main():
    db = Database()
    books = db.get_all_books()
    customers = []
    current_customer_id = 1

    while True:
        print("\n=== Головне меню ===")
        print("1. Увійти")
        print("2. Зареєструватися")
        print("3. Вихід")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            name = input("Ім'я: ")
            email = input("Email: ")
            if name == "admin" and email == "admin@gmail.com":
                admin_menu(db, books)
            else:
                customer = Customer(current_customer_id, name, email)
                customers.append(customer)
                db.insert_customer(customer)
                current_customer_id += 1
                user_menu(db, customer, books)
        elif choice == "2":
            name = input("Ім'я: ")
            email = input("Email: ")
            if name == "admin" and email == "admin@gmail.com":
                admin_menu(db, books)
            customer = Customer(current_customer_id, name, email)
            customers.append(customer)
            db.insert_customer(customer)
            current_customer_id += 1
            print("Реєстрація успішна.")
            user_menu(db, customer, books)
        elif choice == "3":
            db.close()
            print("До побачення!")
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
