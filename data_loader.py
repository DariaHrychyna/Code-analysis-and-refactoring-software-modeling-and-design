import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class DataLoaderFactory:

    @staticmethod
    def load_data(data_type):
        file_map = {
            'books': 'Books.csv',
            'books_fixed': 'Books_fixed.csv',
            'ratings': 'Ratings.csv',
            'users': 'Users.csv',
            'top_books': 'Top_Books.csv'
        }

        if data_type not in file_map:
            raise ValueError(f"Невідомий тип даних: {data_type}")

        file_name = file_map[data_type]
        print(f"Завантаження {data_type} з файлу {file_name}...")
        return pd.read_csv(os.path.join(DATA_DIR, file_name), encoding='latin-1')


if __name__ == '__main__':
    print("Завантажую дані...")
    print(f"Кількість книг: {len(DataLoaderFactory.load_data('books'))}")
    print(f"Кількість рейтингів: {len(DataLoaderFactory.load_data('ratings'))}")
    print(f"Кількість користувачів: {len(DataLoaderFactory.load_data('users'))}")
