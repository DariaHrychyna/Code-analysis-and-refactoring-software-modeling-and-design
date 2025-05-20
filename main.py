from data_loader import DataLoaderFactory
from data_preprocessing import analyze_dataset
from tabulate import tabulate


def show_data():
    books = DataLoaderFactory.load_data('books')
    ratings = DataLoaderFactory.load_data('ratings')
    users = DataLoaderFactory.load_data('users')

    print(f"\nДані про книги (розмірність: {books.shape[0]} рядків, {books.shape[1]} стовпців): ")
    print("Перші кілька рядків даних про книги:")
    print(tabulate(books.head(), headers='keys', tablefmt='pretty'))

    print(f"\nДані про рейтинги (розмірність: {ratings.shape[0]} рядків, {ratings.shape[1]} стовпців): ")
    print("Перші кілька рядків даних про рейтинги:")
    print(tabulate(ratings.head(), headers='keys', tablefmt='pretty'))

    print(f"\nДані про користувачів (розмірність: {users.shape[0]} рядків, {users.shape[1]} стовпців): ")
    print("Перші кілька рядків даних про користувачів:")
    print(tabulate(users.head(), headers='keys', tablefmt='pretty'))


def analyzing_data():
    books = DataLoaderFactory.load_data('books')
    ratings = DataLoaderFactory.load_data('ratings')
    users = DataLoaderFactory.load_data('users')

    analyze_dataset(books, "Books")
    analyze_dataset(ratings, "Ratings")
    analyze_dataset(users, "Users")


def main():
    show_data()
    analyzing_data()
