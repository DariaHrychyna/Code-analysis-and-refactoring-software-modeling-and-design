import unittest
from operations import (
    sort, find, find_sequence,
    find_first_num_elements,
    average, remove_duplicates
)


class TestOperations(unittest.TestCase):

    def test_sort(self):
        """сортування списку"""
        self.assertEqual(sort([3, 1, 2]), [1, 2, 3])  # перевірка, чи правильно сортуються числа
        self.assertEqual(sort([]), [])  # перевірка, чи коректно працює з порожнім списком
        self.assertEqual(sort([5]), [5])  # перевірка, чи повертає той самий елемент для списку з одним числом

    def test_find(self):
        """пошук елемента у списку"""
        self.assertEqual(find([10, 20, 30], 20), 1)  # перевірка, чи знаходить індекс існуючого елемента
        self.assertEqual(find([10, 20, 30], 40), -1)  # перевірка, чи повертає -1 для відсутнього елемента
        self.assertEqual(find([], 5), -1)  # перевірка пошук у порожньому списку

    def test_find_sequence(self):
        """пошук підпослідовності у списку"""
        self.assertEqual(find_sequence([1, 2, 3, 4, 5], [2, 3]), 1)  # послідовність всередині
        self.assertEqual(find_sequence([1, 2, 3, 4, 5], [4, 5]), 3)  # послідовність вкінці
        self.assertEqual(find_sequence([1, 2, 3, 4, 5], [6, 7]), -1)  # послідовність відсутня

    def test_find_first_5_minimums(self):
        """знаходження 5 найменших елементів"""
        self.assertEqual(find_first_num_elements([10, 5, 3, 8, 2, 7, 1]), [1, 2, 3, 5, 7])  # стандартний випадок
        self.assertEqual(find_first_num_elements([4, 2]), [2, 4])  # якщо елементів менше 5
        self.assertEqual(find_first_num_elements([]), [])  # якщо список порожній

    def test_find_first_5_maximums(self):
        """знаходження 5 найбільших елементів"""
        self.assertEqual(find_first_num_elements([10, 5, 3, 8, 2, 7, 1], reverse=True), [10, 8, 7, 5, 3])  # стандартний випадок
        self.assertEqual(find_first_num_elements([4, 2], reverse=True), [4, 2])  # якщо менше 5 елементів
        self.assertEqual(find_first_num_elements([], reverse=True), [])  # якщо порожній список

    def test_average(self):
        """обчислення середнього значення"""
        self.assertEqual(average([10, 20, 30]), 20)  # стандартний випадок
        self.assertEqual(average([5]), 5)  # якщо один елемент у списку
        self.assertEqual(average([]), 0)  # якщо порожній список, очікуємо 0

    def test_remove_duplicates(self):
        """видалення дублікатів зі списку"""
        self.assertEqual(remove_duplicates([1, 2, 2, 3, 3, 3, 4]), [1, 2, 3, 4])  # дублікати видаляються
        self.assertEqual(remove_duplicates([]), [])  # порожній список
        self.assertEqual(remove_duplicates([1, 1, 1, 1]), [1])  # усі елементи однакові

    def test_find_sequence_not_found(self):
        """коли підпослідовність у списку відсутня"""
        self.assertEqual(find_sequence([1, 2, 3, 4, 5], [7, 8]), -1)  # очікуємо -1

    def test_find_index_first_element(self):
        """пошук індексу першого елемента"""
        self.assertEqual(find([1, 2, 3], 1), 0)  # очікуємо 0, бо елемент на першій позиції

    def test_find_index_last_element(self):
        """пошук індексу останнього елемента"""
        self.assertEqual(find([1, 2, 3], 3), 2)  # очікуємо 2, бо це останній елемент

    def test_sort_with_duplicates(self):
        """сортування списку, що містить дублікатні значення"""
        self.assertEqual(sort([3, 1, 2, 1, 3]), [1, 1, 2, 3, 3])  # дублікатні значення мають залишатися

    def test_average_negative_numbers(self):
        """обчислення середнього значення для від'ємних чисел"""
        self.assertEqual(average([-10, -20, -30]), -20)  # очікуємо -20 як середнє значення

    def test_find_sequence_at_end(self):
        """пошук підпослідовності, що знаходиться в кінці списку"""
        self.assertEqual(find_sequence([1, 2, 3, 4, 5, 6], [5, 6]), 4)  # підпослідовність починається з індексу 4


if __name__ == "__main__":
    unittest.main()
