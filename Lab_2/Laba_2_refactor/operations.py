# Дублювання коду і Магічні числа
# Метод вилучення і Заміна магічних чисел на константи

"""Константа"""
NUM_ELEMENTS = 5


def sort(my_list):
    """Сортує список за зростанням."""
    return sorted(my_list)


def find(my_list, value):
    """Знаходить індекс першого входження значення в список.

    Параметри:
    my_list (list): Список, в якому шукається значення.
    value: Значення, яке потрібно знайти.

    Повертає:
    int: Індекс першого входження значення в список, або -1, якщо значення не знайдено.
    """
    try:
        return my_list.index(value)
    except ValueError:
        return -1


def find_sequence(my_list, sequence):
    """Знаходить індекс першого входження послідовності елементів у список.

    Параметри:
    my_list (list): Список, в якому шукається послідовність.
    sequence (list): Послідовність елементів, яку потрібно знайти.

    Повертає:
    int: Індекс першого входження послідовності, або -1, якщо послідовність не знайдена.
    """
    for i in range(len(my_list) - len(sequence) + 1):
        if my_list[i:i + len(sequence)] == sequence:
            return i
    return -1


def find_first_num_elements(my_list, reverse=False):
    """Знаходить перші `NUM_ELEMENTS` елементів з відсортованого списку.

    Параметри:
    my_list (list): Список, з якого вибираються елементи.
    reverse (bool, optional): Якщо True, сортує список у зворотньому порядку.
    За замовчуванням False.

    Повертає:
    list: Список з перших `NUM_ELEMENTS` елементів після сортування.
    """
    return sorted(my_list, reverse=reverse)[:NUM_ELEMENTS]


def average(my_list):
    """Обчислює середнє арифметичне елементів списку.

    Параметри:
    my_list (list): Список чисел.

    Повертає:
    float: Середнє арифметичне елементів списку, або 0, якщо список порожній.
    """
    if len(my_list) == 0:
        return 0
    return sum(my_list) / len(my_list)


def remove_duplicates(my_list):
    """Видаляє дублікати елементів з списку.

    Параметри:
    my_list (list): Список, з якого потрібно видалити дублікати.

    Повертає:
    list: Список без дублікованих елементів.
    """
    seen = set()
    no_duplicates = []
    for item in my_list:
        if item not in seen:
            no_duplicates.append(item)
            seen.add(item)
    return no_duplicates
