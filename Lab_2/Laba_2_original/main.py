import random
from operations import (
    sort, find, find_sequence,
    find_first_5_minimums, find_first_5_maximums,
    average, remove_duplicates
)

if __name__ == "__main__":
    my_list = [random.randint(1, 100) for _ in range(15)]

    print("Оригінальний список:", my_list)

    print("Відсортований список:", sort(my_list))

    random_value = random.choice(my_list)
    print(f"Індекс елементу  {random_value} з оригінального списку:", find(my_list, random_value))

    sequence = [my_list[1], my_list[2]]
    print(f"Індекс послідовності {sequence} з оригінального списку:", find_sequence(my_list, sequence))

    print("Перші п'ять мінімальних елементів:", find_first_5_minimums(my_list))

    print("Перші п'ять максимальних елементів:", find_first_5_maximums(my_list))

    print("Середнє арифметичне:", average(my_list))

    print("Список без дублікатів:", remove_duplicates(my_list))
