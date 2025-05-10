from customer import Customer
from dish import Dish
from database import init_db, add_dish, add_customer, add_order, login_customer
from patterns.observer import OrderManager, KitchenNotifier, BaristaNotifier
from patterns.singleton import OrderDatabase
from patterns.factory import OrderFactory


class Menu:
    def __init__(self):
        self.dishes: list[Dish] = []

    def add_dish_to_menu(self, dish: Dish):
        self.dishes.append(dish)

    def get_dishes(self) -> list[Dish]:
        return self.dishes


if __name__ == "__main__":
    init_db()

    menu = Menu()
    dishes_to_add = [
        Dish("Сирники", 50, "Сніданок"),
        Dish("Борщ", 80, "Гаряча страва"),
        Dish("Чай", 10, "Напої"),
        Dish("Салат", 30, "Закуска")
    ]

    for dish in dishes_to_add:
        menu.add_dish_to_menu(dish)
        add_dish(dish)

    # створення менеджера і підключення спостерігачів
    manager = OrderManager()
    kitchen = KitchenNotifier()
    barista = BaristaNotifier()
    manager.attach(kitchen)
    manager.attach(barista)

    current_customer = None

    while True:
        if current_customer is None:
            print("=== Вхід або реєстрація ===")
            email = input("Email: ")
            existing = login_customer(email)
            if existing:
                print(f"Ласкаво просимо, {existing[1]}!")
                current_customer = Customer(existing[1], existing[2], existing[3])
                customer_id = existing[0]
            else:
                print("Користувача не знайдено. Зареєструємо нового.")
                name = input("Ім'я: ")
                phone = input("Телефон: ")
                current_customer = Customer(name, email, phone)
                customer_id = add_customer(current_customer)
        else:
            continue_as_current = input("Продовжити як поточний користувач? (y/n): ")
            if continue_as_current.lower() != 'y':
                current_customer = None
                continue

        print("\n=== Виберіть тип замовлення ===")
        print("1 - Офлайн")
        print("2 - Онлайн")
        choice = input("Ваш вибір: ")
        order_type = "offline" if choice == "1" else "online" if choice == "2" else None
        if order_type:
            order = OrderFactory.create_order(current_customer, order_type)
        else:
            print("Невірний вибір. Завершення програми.")
            continue

        print("\n=== Меню ===")
        dishes = menu.get_dishes()
        for idx, dish in enumerate(dishes):
            print(f"{idx + 1}. {dish.dish_name} - {dish.price} грн ({dish.category})")

        while True:
            selection = input("Введіть номер страви для додавання або 'q' для завершення: ")
            if selection.lower() == 'q':
                break
            try:
                index = int(selection) - 1
                if 0 <= index < len(dishes):
                    order.add_dish_to_order(dishes[index])
                    print(f"Додано: {dishes[index].dish_name}")
                else:
                    print("Невірний номер страви.")
            except ValueError:
                print("Введіть коректний номер або 'q'.")

        total = order.calculate_total_price()
        print(f"\n=== Замовлення завершено ===")
        print(f"Загальна сума: {total:.2f} грн")

        current_customer.place_order(order)

        # збереження замовлення в Singleton
        db = OrderDatabase()
        db.add_order(order)

        add_order(order, customer_id)

        # повідомлення від спостерігачів
        manager.create_order(order)

        again = input("\nБажаєте створити нове замовлення? (y/n): ")
        if again.lower() != 'y':
            print("Дякуємо за використання програми!")
            break
