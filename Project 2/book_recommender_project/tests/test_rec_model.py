import unittest
import pandas as pd
from web.rec_model import BookRecommender
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBookRecommenderSingleton(unittest.TestCase):

    def setUp(self):
        """Підготовка тестового DataFrame: створює користувача з ≥200 оцінками і книгу з ≥50 оцінками"""
        data = {
            'User-ID': [],
            'ISBN': [],
            'Book-Title': [],
            'Book-Author': [],
            'Book-Rating': [],
        }

        for i in range(200):
            data['User-ID'].append(1)
            data['ISBN'].append(f'isbn_{i}')
            if i == 0:
                data['Book-Title'].append('Book A')
                data['Book-Author'].append('Author A')
            else:
                data['Book-Title'].append(f'Book {i}')
                data['Book-Author'].append(f'Author {i}')
            data['Book-Rating'].append(5)

        for uid in range(2, 51):
            data['User-ID'].append(uid)
            data['ISBN'].append('isbn_0')
            data['Book-Title'].append('Book A')
            data['Book-Author'].append('Author A')
            data['Book-Rating'].append(4)

        data['User-ID'].append(1)
        data['ISBN'].append('isbn_common')
        data['Book-Title'].append('Popular Book')
        data['Book-Author'].append('Famous Author')
        data['Book-Rating'].append(5)

        self.df = pd.DataFrame(data)

    def test_singleton_same_instance(self):
        """Перевіряє, що клас BookRecommender реалізовано як Singleton — дві ініціалізації дають той самий об'єкт"""
        rec1 = BookRecommender(self.df)
        rec2 = BookRecommender(self.df)
        self.assertIs(rec1, rec2)

    def test_recommend_known_book(self):
        """Перевіряє, що метод recommend повертає список рекомендацій для відомої книги"""
        recommender = BookRecommender(self.df)
        recs = recommender.recommend('Book A', top_n=2)
        self.assertIsInstance(recs, list)
        self.assertTrue(all('title' in r and 'author' in r for r in recs))

    def test_recommend_unknown_book_returns_empty(self):
        """Перевіряє, що метод recommend повертає порожній список для невідомої книги"""
        recommender = BookRecommender(self.df)
        recs = recommender.recommend('Nonexistent Book')
        self.assertEqual(recs, [])

    def test_pivot_table_creation(self):
        """Перевіряє, що згенерована з даних зведена таблиця (pivot table) містить очікувані значення"""
        recommender = BookRecommender(self.df)
        pt = recommender._create_pivot_table()
        self.assertIn('Book A', pt.index)
        self.assertIn(1, pt.columns)
        self.assertFalse(pt.isnull().values.any())

    def test_filtered_books_contains_only_frequent(self):
        """Перевіряє, що відфільтровані книги містять лише ті, які отримали ≥50 оцінок"""
        recommender = BookRecommender(self.df)
        filtered = recommender.filtered_books
        self.assertIn('Book A', filtered['Book-Title'].values)

    def test_singleton_different_input_same_instance(self):
        """Перевіряє, що Singleton повертає один і той самий екземпляр навіть при різних вхідних даних"""
        df1 = self.df.copy()
        df2 = self.df.copy()
        rec1 = BookRecommender(df1)
        rec2 = BookRecommender(df2)
        self.assertIs(rec1, rec2)
