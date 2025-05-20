import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from rec_model import BookRecommender
from top_books_model import (get_authors_with_book_counts, get_books_by_author, get_books_by_partial_title,
                             get_top_rated_books)

from strategy_sorting import (
    NameAscStrategy, NameDescStrategy, CountAscStrategy, CountDescStrategy,
    TitleAscStrategy, TitleDescStrategy, YearAscStrategy, YearDescStrategy
)


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

books_path = os.path.join(BASE_DIR, '..', 'data', 'Books_fixed.csv')
ratings_path = os.path.join(BASE_DIR, '..', 'data', 'Ratings.csv')

books = pd.read_csv(books_path)
ratings = pd.read_csv(ratings_path)

ratings_books_merged = ratings.merge(books, on='ISBN')

recommender = BookRecommender(ratings_books_merged)


@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    book_title = ""
    if request.method == 'POST':
        book_title = request.form['book_title']
        books_by_partial_title = get_books_by_partial_title(book_title)
        if not books_by_partial_title.empty:
            matched_title = books_by_partial_title.iloc[0]['Book-Title']
            recommendations = recommender.recommend(matched_title)
            if not recommendations:
                recommendations = ["Рекомендації не знайдено."]
            book_title = matched_title
        else:
            recommendations = ["Книги за вашим запитом не знайдено."]
    top_books = get_top_rated_books(20).to_dict(orient='records')
    return render_template('index.html', recommendations=recommendations, book_title=book_title,
                           top_books=top_books)


@app.route('/search_titles')
def search_titles():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    matched_books = get_books_by_partial_title(query)
    titles = matched_books['Book-Title'].unique().tolist()
    return jsonify(titles)


@app.route('/catalog')
def catalog():
    sort = request.args.get('sort', 'name_asc')
    authors_df = get_authors_with_book_counts()

    strategy_map = {
        'name_asc': NameAscStrategy(),
        'name_desc': NameDescStrategy(),
        'count_asc': CountAscStrategy(),
        'count_desc': CountDescStrategy()
    }

    strategy = strategy_map.get(sort, NameAscStrategy())
    authors_df = strategy.sort(authors_df)

    authors = authors_df.to_dict(orient='records')
    return render_template('catalog.html', authors=authors, total_authors=len(authors), sort=sort)


@app.route('/author/<author_name>')
def author_books(author_name):
    sort = request.args.get('sort', 'title_asc')
    books_df = get_books_by_author(author_name)

    strategy_map = {
        'title_asc': TitleAscStrategy(),
        'title_desc': TitleDescStrategy(),
        'year_asc': YearAscStrategy(),
        'year_desc': YearDescStrategy()
    }

    strategy = strategy_map.get(sort, TitleAscStrategy())
    books_df = strategy.sort(books_df)

    return render_template('author_books.html', author=author_name,
                           books=books_df.to_dict(orient='records'), sort=sort)


if __name__ == '__main__':
    app.run(debug=True)