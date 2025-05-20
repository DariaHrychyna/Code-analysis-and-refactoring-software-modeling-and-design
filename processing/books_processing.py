from data_loader import DataLoaderFactory
from tabulate import tabulate


def find_missing_values_in_books():
    books = DataLoaderFactory.load_data('books')

    print("\nПропущені значення по стовпцях:")
    print(books.isnull().sum())
    missing_rows = books[books.isnull().any(axis=1)]

    print(f"\nЗнайдено {len(missing_rows)} рядків з пропущеними значеннями у таблиці книг: ")
    print(tabulate(missing_rows.head(10), headers='keys', tablefmt='pretty', showindex=True))


def fix_known_errors_in_books(df):
    df.loc[df['ISBN'] == '078946697X', 'Book-Title'] = 'The Story of the X-Men: How It All Began (Dk Readers, Level 4, Proficient Readers)'
    df.loc[df['ISBN'] == '078946697X', 'Book-Author'] = 'Michael Teitelbaum'
    df.loc[df['ISBN'] == '078946697X', 'Year-Of-Publication'] = 2000
    df.loc[df['ISBN'] == '078946697X', 'Publisher'] = 'DK Publishing Inc'
    df.loc[df['ISBN'] == '078946697X', 'Image-URL-S'] = 'http://images.amazon.com/images/P/078946697X.01.THUMBZZZ.jpg'
    df.loc[df['ISBN'] == '078946697X', 'Image-URL-M'] = 'http://images.amazon.com/images/P/078946697X.01.MZZZZZZZ.jpg'
    df.loc[df['ISBN'] == '078946697X', 'Image-URL-L'] = 'http://images.amazon.com/images/P/078946697X.01.LZZZZZZZ.jpg'

    df.loc[df['ISBN'] == '2070426769', 'Book-Title'] = 'Peuple du ciel, suivi de \'Les Bergers\''
    df.loc[df['ISBN'] == '2070426769', 'Book-Author'] = 'Jean-Marie Gustave Le Clézio'
    df.loc[df['ISBN'] == '2070426769', 'Year-Of-Publication'] = 2003
    df.loc[df['ISBN'] == '2070426769', 'Publisher'] = 'Gallimard'
    df.loc[df['ISBN'] == '2070426769', 'Image-URL-S'] = 'http://images.amazon.com/images/P/2070426769.01.THUMBZZZ.jpg'
    df.loc[df['ISBN'] == '2070426769', 'Image-URL-M'] = 'http://images.amazon.com/images/P/2070426769.01.MZZZZZZZ.jpg'
    df.loc[df['ISBN'] == '2070426769', 'Image-URL-L'] = 'http://images.amazon.com/images/P/2070426769.01.LZZZZZZZ.jpg'

    df.loc[df['ISBN'] == '0789466953', 'Book-Title'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'
    df.loc[df['ISBN'] == '0789466953', 'Book-Author'] = 'James Buckley'
    df.loc[df['ISBN'] == '0789466953', 'Year-Of-Publication'] = 2000
    df.loc[df['ISBN'] == '0789466953', 'Publisher'] = 'DK Publishing Inc'
    df.loc[df['ISBN'] == '0789466953', 'Image-URL-S'] = 'http://images.amazon.com/images/P/0789466953.01.THUMBZZZ.jpg'
    df.loc[df['ISBN'] == '0789466953', 'Image-URL-M'] = 'http://images.amazon.com/images/P/0789466953.01.MZZZZZZZ.jpg'
    df.loc[df['ISBN'] == '0789466953', 'Image-URL-L'] = 'http://images.amazon.com/images/P/0789466953.01.LZZZZZZZ.jpg'

    df.loc[df['ISBN'] == '0751352497', 'Book-Author'] = 'Unknown'

    df.loc[df['ISBN'] == '9627982032', 'Book-Author'] = 'Larissa Anne Downes'

    df.loc[df['ISBN'] == '193169656X', 'Publisher'] = 'Mundania Pr'

    df.loc[df['ISBN'] == '1931696993', 'Publisher'] = 'Bantam'

    return df


def find_missing_values_in_books_fixed():
    books = DataLoaderFactory.load_data('books_fixed')
    print("\nПропущені значення по стовпцях у виправленій таблиці:")
    print(books.isnull().sum())
    missing_rows = books[books.isnull().any(axis=1)]
    print(f"\nЗнайдено {len(missing_rows)} рядків з пропущеними значеннями у виправленій таблиці книг:")
    print(tabulate(missing_rows.head(10), headers='keys', tablefmt='pretty', showindex=True))


def edit_years(df):
    df.loc[df['ISBN'] == '0671746103', 'Year-Of-Publication'] = 1991
    df.loc[df['ISBN'] == '0671746103', 'Book-Author'] = 'Bruce Coville'

    df.loc[df['ISBN'] == '0671791990', 'Year-Of-Publication'] = 2005

    df.loc[df['ISBN'] == '0870449842', 'Year-Of-Publication'] = 2001

    df.loc[df['ISBN'] == '0140301690', 'Year-Of-Publication'] = 2003

    df.loc[df['ISBN'] == '0140201092', 'Year-Of-Publication'] = 1981

    df.loc[df['ISBN'] == '0394701658', 'Year-Of-Publication'] = 1995

    df.loc[df['ISBN'] == '3442436893', 'Year-Of-Publication'] = 2006
    df.loc[df['ISBN'] == '3442436893', 'Book-Title'] = 'Das große Böse - Mädchen- Lesebuch'

    df.loc[df['ISBN'] == '0870446924', 'Year-Of-Publication'] = 2003

    df.loc[df['ISBN'] == '0671266500', 'Year-Of-Publication'] = 1987

    df.loc[df['ISBN'] == '0684718022', 'Year-Of-Publication'] = 1996

    df.loc[df['ISBN'] == '0380000059', 'Year-Of-Publication'] = 1925

    df.loc[df['ISBN'] == '068471809X', 'Year-Of-Publication'] = 1937

    df.loc[df['ISBN'] == '0671740989', 'Year-Of-Publication'] = 1991

    return df


def get_top_authors(df, top_n=50):
    author_book_count = df['Book-Author'].value_counts()
    author_book_count = author_book_count[author_book_count.index != 'Not Applicable (Na )']
    return author_book_count.head(top_n)


def save_fixed_books(df, path='data/Books_fixed.csv'):
    df.to_csv(path, index=False)

