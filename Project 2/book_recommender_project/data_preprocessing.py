from tabulate import tabulate


def analyze_dataset(df, name):
    print(f"\n------------------ Аналіз таблиці {name} ------------------")
    print(f"Розмірність: {df.shape[0]} рядків, {df.shape[1]} стовпців")

    # Типи даних
    print("\nТипи даних по стовпцях:")
    dtype_table = [(col, str(dtype)) for col, dtype in df.dtypes.items()]
    print(tabulate(dtype_table, headers=["Стовпець", "Тип"], tablefmt="pretty"))

    # Пропущені значення
    print("\nВідсутні значення по стовпцях:")
    missing_table = [(col, df[col].isnull().sum()) for col in df.columns]
    print(tabulate(missing_table, headers=["Стовпець", "Кількість пропущених"], tablefmt="pretty"))

    # Дублікати
    print("\nКількість дублікатів:")
    print(df.duplicated().sum())

    # Унікальні значення
    print("\nУнікальні значення в кожному стовпці:")
    unique_table = [(col, df[col].nunique()) for col in df.columns]
    print(tabulate(unique_table, headers=["Стовпець", "Кількість унікальних"], tablefmt="pretty"))
