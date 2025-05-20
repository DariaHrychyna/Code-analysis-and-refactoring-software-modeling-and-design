from data_loader import DataLoaderFactory


def save_users_with_age(path='data/Users_with_Age.csv'):
    users_df = DataLoaderFactory.load_data('users')
    users_with_age = users_df.copy()
    users_with_age.to_csv(path, index=False)
    print(f"Файл з колонкою 'Age' збережено як: {path}")


def remove_age_and_save_users(path='data/Users.csv'):
    users_df = DataLoaderFactory.load_data('users')
    if 'Age' in users_df.columns:
        users_df = users_df.drop(columns=['Age'])
        users_df.to_csv(path, index=False)
        print(f"Колонку 'Age' видалено. Таблицю перезаписано як: {path}")
    else:
        print("Колонка 'Age' вже відсутня в таблиці.")
