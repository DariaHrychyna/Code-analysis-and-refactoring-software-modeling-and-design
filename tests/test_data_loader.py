import unittest
from unittest.mock import patch
import pandas as pd
from data_loader import DataLoaderFactory
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@patch('data_loader.pd.read_csv')
class TestDataLoaderFactory(unittest.TestCase):

    def test_load_all_known_types(self, mock_read_csv):
        """Перевіряє, що всі відомі типи даних коректно завантажуються як DataFrame"""
        mock_read_csv.return_value = pd.DataFrame()
        for data_type in ['books', 'books_fixed', 'ratings', 'users', 'top_books']:
            df = DataLoaderFactory.load_data(data_type)
            self.assertIsInstance(df, pd.DataFrame)

    def test_load_empty_csv_returns_empty_dataframe(self, mock_read_csv):
        """Перевіряє, що при завантаженні порожнього CSV повертається порожній DataFrame"""
        mock_read_csv.return_value = pd.DataFrame()
        df = DataLoaderFactory.load_data('books')
        self.assertTrue(df.empty)

    def test_load_books_calls_read_csv_with_correct_path(self, mock_read_csv):
        """Перевіряє, що метод load_data викликає pd.read_csv з правильним шляхом до файлу Books.csv"""
        mock_read_csv.return_value = pd.DataFrame()
        result = DataLoaderFactory.load_data('books')
        args, kwargs = mock_read_csv.call_args
        self.assertTrue(args[0].endswith('Books.csv'))
        self.assertEqual(kwargs.get('encoding'), 'latin-1')
        self.assertIsInstance(result, pd.DataFrame)

    def test_load_unknown_data_type_raises_value_error(self, mock_read_csv):
        """Перевіряє, що метод load_data виводить ValueError при спробі завантажити невідомий тип даних"""
        with self.assertRaises(ValueError) as context:
            DataLoaderFactory.load_data('unknown_type')
        self.assertIn('Невідомий тип даних', str(context.exception))
        mock_read_csv.assert_not_called()

    def test_load_data_is_static_method(self, mock_read_csv):
        """Перевіряє, що метод load_data є статичним методом (static factory method)"""
        self.assertTrue(callable(DataLoaderFactory.load_data))
        self.assertIsInstance(DataLoaderFactory.__dict__['load_data'], staticmethod)

    def test_factory_returns_different_dataframes_for_each_type(self, mock_read_csv):
        """Перевіряє, що фабрика повертає різні DataFrame об'єкти залежно від типу даних"""
        mock_read_csv.side_effect = [
            pd.DataFrame({'A': [1]}),
            pd.DataFrame({'B': [2]}),
            pd.DataFrame({'C': [3]})
        ]

        books_df = DataLoaderFactory.load_data('books')
        ratings_df = DataLoaderFactory.load_data('ratings')
        users_df = DataLoaderFactory.load_data('users')

        self.assertIn('A', books_df.columns)
        self.assertIn('B', ratings_df.columns)
        self.assertIn('C', users_df.columns)
