import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def _filter_books(df):
    users_ratings_count = df.groupby('User-ID').count()['ISBN'].reset_index()
    users_ratings_count.columns = ['User-ID', 'No-of-Books-Rated']
    users_200 = users_ratings_count[users_ratings_count['No-of-Books-Rated'] >= 200]

    books_with_users_200 = pd.merge(users_200, df, on='User-ID')
    books_ratings_count = df.groupby('Book-Title').count()['ISBN'].reset_index()
    books_ratings_count.columns = ['Book-Title', 'Number-of-Book-Ratings']
    books_ratings_50 = books_ratings_count[books_ratings_count['Number-of-Book-Ratings'] >= 50]

    filtered_books = pd.merge(books_ratings_50, books_with_users_200, on='Book-Title')
    return filtered_books


class BookRecommender:
    _instance = None

    def __new__(cls, ratings_books_merged):
        if cls._instance is None:
            cls._instance = super(BookRecommender, cls).__new__(cls)
            cls._instance._init_recommender(ratings_books_merged)
        return cls._instance

    def _init_recommender(self, ratings_books_merged):
        self.filtered_books = _filter_books(ratings_books_merged)
        self.pt = self._create_pivot_table()
        self.similarities = cosine_similarity(self.pt)

    def _create_pivot_table(self):
        pt = self.filtered_books.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
        pt.fillna(0, inplace=True)
        return pt

    def recommend(self, book_name, top_n=10):
        if book_name not in self.pt.index:
            return []
        index = np.where(self.pt.index == book_name)[0][0]
        similar_books_list = sorted(
            list(enumerate(self.similarities[index])), key=lambda x: x[1], reverse=True
        )[1:top_n + 1]
        recommended_titles = [self.pt.index[i] for i, _ in similar_books_list]
        result = []
        for title in recommended_titles:
            author = self.filtered_books[self.filtered_books['Book-Title'] == title]['Book-Author'].iloc[0]
            result.append({'title': title, 'author': author})
        return result
