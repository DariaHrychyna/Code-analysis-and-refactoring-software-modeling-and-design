import pandas as pd


def merge_books_and_ratings(books_df, ratings_df):
    return pd.merge(ratings_df, books_df, on="ISBN")


def drop_image_columns(df):
    return df.drop(columns=['Image-URL-S','Image-URL-M','Image-URL-L'])


def compute_average_rating(book_rating_df):
    avg_rating = book_rating_df.groupby('ISBN')['Book-Rating'].mean().round(1).reset_index()
    avg_rating.rename(columns={'Book-Rating': 'Average-Rating'}, inplace=True)
    return avg_rating

