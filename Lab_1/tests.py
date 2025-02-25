import pytest
from datetime import datetime
from main import Order, OrderManager


@pytest.fixture
def setup_db():
    """Створює тимчасову базу даних для тестів."""
    manager = OrderManager()
    with manager.conn:
        manager.conn.execute("DELETE FROM orders")  # очищення бази перед тестами
    manager.orders.clear()  # очищення кешованих замовленнь
    yield manager
    manager.conn.close()


# ----------------1-----------------------------------------------------------------------
def test_order_creation():
    """Перевіряє, чи правильно створюється об'єкт Order."""
    customer_info = {
        "Прізвище клієнта": "Іваненко",
        "Назва товару": "Ноутбук",
        "Кількість": 2,
        "Вартість": 30000.0,
        "Дата замовлення": "2024-02-24"
    }
    order = Order(1, customer_info)
    assert order.order_id == 1
    assert order.customer_name == "Іваненко"
    assert order.product_name == "Ноутбук"
    assert order.quantity == 2
    assert order.price == 30000.0
    assert order.order_date == datetime.strptime("2024-02-24", "%Y-%m-%d")


# ----------------2-----------------------------------------------------------------------
def test_add_order(setup_db):
    """Перевіряє додавання замовлення в базу даних."""
    manager = setup_db
    customer_info = {
        "Прізвище клієнта": "Петров",
        "Назва товару": "Смартфон",
        "Кількість": 1,
        "Вартість": 15000.0,
        "Дата замовлення": "2024-02-23"
    }
    manager.add_order(1, customer_info)
    assert 1 in manager.orders

    with manager.conn:
        row = manager.conn.execute("SELECT * FROM orders WHERE order_id = ?", (1,)).fetchone()
    assert row is not None
    assert row[1] == "Петров"
    assert row[2] == "Смартфон"


# ----------------3-----------------------------------------------------------------------
def test_add_duplicate_order(setup_db):
    """Перевіряє, що дублювання замовлення не відбувається."""
    manager = setup_db
    customer_info = {
        "Прізвище клієнта": "Сидоренко",
        "Назва товару": "Монітор",
        "Кількість": 1,
        "Вартість": 8000.0,
        "Дата замовлення": "2024-02-20"
    }
    manager.add_order(2, customer_info)
    manager.add_order(2, customer_info)  # дублювання ID

    # в базі має бути лише один запис
    with manager.conn:
        rows = manager.conn.execute("SELECT * FROM orders WHERE order_id = 2").fetchall()
    assert len(rows) == 1


# ----------------4-----------------------------------------------------------------------
def test_remove_order(setup_db):
    """Перевіряє видалення замовлення з бази."""
    manager = setup_db
    customer_info = {
        "Прізвище клієнта": "Ковальчук",
        "Назва товару": "Миша",
        "Кількість": 3,
        "Вартість": 1200.0,
        "Дата замовлення": "2024-02-21"
    }
    manager.add_order(3, customer_info)
    manager.remove_order(3)
    assert 3 not in manager.orders

    with manager.conn:
        row = manager.conn.execute("SELECT * FROM orders WHERE order_id = ?", (3,)).fetchone()
    assert row is None


# ----------------5-----------------------------------------------------------------------
def test_find_order_by_name(setup_db):
    """Перевіряє пошук за прізвищем клієнта."""
    manager = setup_db
    customer_info = {
        "Прізвище клієнта": "Гаврилюк",
        "Назва товару": "Клавіатура",
        "Кількість": 2,
        "Вартість": 2500.0,
        "Дата замовлення": "2024-02-19"
    }
    manager.add_order(4, customer_info)

    found = []
    manager.find_order(customer_name="Гаврилюк")
    for order in manager.orders.values():
        if order.customer_name == "Гаврилюк":
            found.append(order)

    assert len(found) == 1
    assert found[0].product_name == "Клавіатура"


# ----------------6-----------------------------------------------------------------------
def test_find_order_by_product(setup_db):
    """Перевіряє пошук за назвою товару."""
    manager = setup_db
    customer_info = {
        "Прізвище клієнта": "Дмитренко",
        "Назва товару": "Навушники",
        "Кількість": 1,
        "Вартість": 3200.0,
        "Дата замовлення": "2024-02-18"
    }
    manager.add_order(5, customer_info)

    found = []
    manager.find_order(product_name="Навушники")
    for order in manager.orders.values():
        if order.product_name == "Навушники":
            found.append(order)

    assert len(found) == 1
    assert found[0].customer_name == "Дмитренко"


# ----------------7-----------------------------------------------------------------------
def test_get_order_by_id(setup_db):
    """Перевіряє отримання замовлення за ID."""
    manager = setup_db
    customer_info = {
        "Прізвище клієнта": "Левченко",
        "Назва товару": "Планшет",
        "Кількість": 1,
        "Вартість": 11000.0,
        "Дата замовлення": "2024-02-17"
    }
    manager.add_order(6, customer_info)  # додавання замовлення
    order = manager.get_order_by_id(6)  # отримання замовлення
    assert order is not None


# ----------------8-----------------------------------------------------------------------
def test_show_all_orders(setup_db):
    """Перевіряє, що всі замовлення коректно відображаються."""
    manager = setup_db
    # додавання замовлення для тесту
    customer_info = {
        "Прізвище клієнта": "Іваненко",
        "Назва товару": "Ноутбук",
        "Кількість": 1,
        "Вартість": 25000.0,
        "Дата замовлення": "2024-02-24"
    }
    manager.add_order(1, customer_info)

    manager.show_all_orders()
    with manager.conn:
        rows = manager.conn.execute("SELECT COUNT(*) FROM orders").fetchone()
    assert rows[0] > 0  # в базі має бути хоча б одне замовлення


# ----------------9-----------------------------------------------------------------------
def test_invalid_date_format():
    """Перевіряє, що некоректний формат дати викликає помилку."""
    customer_info = {
        "Прізвище клієнта": "Шевченко",
        "Назва товару": "Мишка",
        "Кількість": 1,
        "Вартість": 500.0,
        "Дата замовлення": "24-02-2024"  # некоректний формат дати
    }
    with pytest.raises(ValueError):
        Order(7, customer_info)


# ----------------10-----------------------------------------------------------------------============================
def test_find_order_by_quantity(setup_db):
    """Перевіряє пошук замовлень за кількістю товару."""
    manager = setup_db
    manager.add_order(7, {"Прізвище клієнта": "Олексієнко", "Назва товару": "Камера",
                          "Кількість": 3, "Вартість": 4500.0, "Дата замовлення": "2024-02-14"})

    found = []
    manager.find_order(quantity=3)
    for order in manager.orders.values():
        if order.quantity == 3:
            found.append(order)

    assert len(found) == 1
    assert found[0].product_name == "Камера"


# ----------------11-----------------------------------------------------------------------============================
def test_remove_nonexistent_order(setup_db):
    """Перевіряє, що видалення неіснуючого замовлення не викликає помилок."""
    manager = setup_db
    manager.remove_order(999)  # видалення неіснуючого замовлення
    assert 999 not in manager.orders  # впевнюємося, що воно не з'явилось


# ----------------12-----------------------------------------------------------------------============================
def test_find_order_with_no_matches(setup_db):
    """Перевіряє пошук замовлення, яке не існує."""
    manager = setup_db
    found = []
    manager.find_order(customer_name="Невідомий")
    for order in manager.orders.values():
        if order.customer_name == "Невідомий":
            found.append(order)

    assert len(found) == 0  # не повинно бути результатів
