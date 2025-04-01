"""Імпорт"""
import random
from operations import (
    sort, find, find_sequence,
    find_first_num_elements,
    average, remove_duplicates
)

# КОНСТАНТИ
NUM_ELEMENTS = 5
MIN_RANDOM_VALUE = 1
MAX_RANDOM_VALUE = 100

if __name__ == "__main__":
    my_list = [random.randint(MIN_RANDOM_VALUE, MAX_RANDOM_VALUE) for _ in range(15)]

    print("Оригінальний список:", my_list)

    print("Відсортований список:", sort(my_list))

    random_value = random.choice(my_list)
    print(f"Індекс елементу  {random_value} з оригінального списку:", find(my_list, random_value))

    sequence = [my_list[1], my_list[2]]
    print(f"Індекс послідовності {sequence} з оригінального списку:", find_sequence(my_list,
                                                                                    sequence))

    print(f"Перші {NUM_ELEMENTS} мінімальних елементів:", find_first_num_elements(my_list))

    print(f"Перші {NUM_ELEMENTS} максимальних елементів:", find_first_num_elements(my_list,
                                                                                   reverse=True))

    print("Середнє арифметичне:", average(my_list))

    print("Список без дублікатів:", remove_duplicates(my_list))
