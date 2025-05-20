import unittest
from abc import ABCMeta

import pandas as pd
from web.strategy_sorting import (
    NameAscStrategy, NameDescStrategy, CountAscStrategy, CountDescStrategy,
    TitleAscStrategy, TitleDescStrategy, YearAscStrategy, YearDescStrategy, SortingStrategy
)
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestSortingStrategies(unittest.TestCase):

    def setUp(self):
        self.authors_df = pd.DataFrame({
            'Book-Author': ['Author C', 'Author A', 'Author B'],
            'Book-Count': [10, 5, 15]
        })
        self.books_df = pd.DataFrame({
            'Book-Title': ['Book C', 'Book A', 'Book B'],
            'Year-Of-Publication': [2000, 2010, 1990]
        })

    def test_name_asc_sort(self):
        """Перевіряє, що NameAscStrategy сортує авторів за іменем у зростаючому порядку"""
        sorted_df = NameAscStrategy().sort(self.authors_df)
        self.assertEqual(list(sorted_df['Book-Author']), ['Author A', 'Author B', 'Author C'])

    def test_name_desc_sort(self):
        """Перевіряє, що NameDescStrategy сортує авторів за іменем у спадаючому порядку"""
        sorted_df = NameDescStrategy().sort(self.authors_df)
        self.assertEqual(list(sorted_df['Book-Author']), ['Author C', 'Author B', 'Author A'])

    def test_count_asc_sort(self):
        """Перевіряє, що CountAscStrategy сортує авторів за кількістю книг у зростаючому порядку"""
        sorted_df = CountAscStrategy().sort(self.authors_df)
        self.assertEqual(list(sorted_df['Book-Count']), [5, 10, 15])

    def test_count_desc_sort(self):
        """Перевіряє, що CountDescStrategy сортує авторів за кількістю книг у спадаючому порядку"""
        sorted_df = CountDescStrategy().sort(self.authors_df)
        self.assertEqual(list(sorted_df['Book-Count']), [15, 10, 5])

    def test_title_asc_sort(self):
        """Перевіряє, що TitleAscStrategy сортує книги за назвою у зростаючому порядку"""
        sorted_df = TitleAscStrategy().sort(self.books_df)
        self.assertEqual(list(sorted_df['Book-Title']), ['Book A', 'Book B', 'Book C'])

    def test_title_desc_sort(self):
        """Перевіряє, що TitleDescStrategy сортує книги за назвою у спадаючому порядку"""
        sorted_df = TitleDescStrategy().sort(self.books_df)
        self.assertEqual(list(sorted_df['Book-Title']), ['Book C', 'Book B', 'Book A'])

    def test_year_asc_sort(self):
        """Перевіряє, що YearAscStrategy сортує книги за роком публікації у зростаючому порядку"""
        sorted_df = YearAscStrategy().sort(self.books_df)
        self.assertEqual(list(sorted_df['Year-Of-Publication']), [1990, 2000, 2010])

    def test_year_desc_sort(self):
        """Перевіряє, що YearDescStrategy сортує книги за роком публікації у спадаючому порядку"""
        sorted_df = YearDescStrategy().sort(self.books_df)
        self.assertEqual(list(sorted_df['Year-Of-Publication']), [2010, 2000, 1990])

    def test_sorting_empty_dataframe_returns_empty(self):
        """Перевіряє, що сортування порожнього DataFrame повертає також порожній DataFrame"""
        empty_df = pd.DataFrame(columns=['Book-Author', 'Book-Count'])
        sorted_df = NameAscStrategy().sort(empty_df)
        self.assertTrue(sorted_df.empty)

    def test_sortingstrategy_is_abstract(self):
        """Перевіряє, що SortingStrategy є абстрактним класом з абстрактним методом sort"""
        self.assertTrue(isinstance(SortingStrategy, ABCMeta))
        with self.assertRaises(TypeError):
            # Спроба створити інстанс абстрактного класу має викликати помилку
            SortingStrategy()

    def test_all_strategies_are_subclasses(self):
        """Перевіряє, що всі конкретні стратегії є підкласами SortingStrategy"""
        strategies = [
            NameAscStrategy, NameDescStrategy,
            CountAscStrategy, CountDescStrategy,
            TitleAscStrategy, TitleDescStrategy,
            YearAscStrategy, YearDescStrategy
        ]
        for strategy_cls in strategies:
            self.assertTrue(issubclass(strategy_cls, SortingStrategy))

    def test_sort_returns_sorted_copy_not_modify_original(self):
        """Перевіряє, що метод sort повертає новий DataFrame і не змінює вхідний"""
        strategy = NameAscStrategy()
        df_copy = self.authors_df.copy()
        sorted_df = strategy.sort(self.authors_df)
        # Оригінальний DataFrame не змінено
        pd.testing.assert_frame_equal(self.authors_df, df_copy)
        # Відсортований DataFrame відрізняється, якщо порядок початковий не відсортований
        self.assertNotEqual(list(sorted_df['Book-Author']), list(self.authors_df['Book-Author']))

    def test_strategies_handle_empty_dataframe(self):
        """Перевіряє, що всі стратегії коректно сортують порожній DataFrame, повертаючи порожній"""
        empty_authors_df = pd.DataFrame(columns=['Book-Author', 'Book-Count'])
        empty_books_df = pd.DataFrame(columns=['Book-Title', 'Year-Of-Publication'])

        strategies_authors = [
            NameAscStrategy(), NameDescStrategy(),
            CountAscStrategy(), CountDescStrategy()
        ]
        for strat in strategies_authors:
            sorted_df = strat.sort(empty_authors_df)
            self.assertTrue(sorted_df.empty)

        strategies_books = [
            TitleAscStrategy(), TitleDescStrategy(),
            YearAscStrategy(), YearDescStrategy()
        ]
        for strat in strategies_books:
            sorted_df = strat.sort(empty_books_df)
            self.assertTrue(sorted_df.empty)
