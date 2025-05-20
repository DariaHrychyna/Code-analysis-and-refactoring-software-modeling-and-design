from data_loader import DataLoaderFactory


def get_authors_with_book_counts():
    df = DataLoaderFactory.load_data('top_books')
    author_counts = df['Book-Author'].value_counts().reset_index()
    author_counts.columns = ['Book-Author', 'Book-Count']
    return author_counts


def get_books_by_author(author_name):
    df = DataLoaderFactory.load_data('top_books')
    return df[df['Book-Author'] == author_name]


def get_books_by_partial_title(partial_title):
    df = DataLoaderFactory.load_data('top_books')
    filtered_books = df[df['Book-Title'].str.contains(partial_title, case=False, na=False, regex=False)]
    return filtered_books


def get_top_rated_books(n=20):
    df = DataLoaderFactory.load_data('top_books')
    df = df.dropna(subset=['Book-Rating'])
    top_books = df.sort_values(by='Book-Rating', ascending=False).drop_duplicates(subset='Book-Title')
    return top_books.head(n)[['Book-Title', 'Book-Author', 'Book-Rating', 'Image-URL-L']]
