import matplotlib.pyplot as plt
import seaborn as sns


def plot_average_rating_distribution(ratings_sorted):
    cool = sns.color_palette("cool", n_colors=len(ratings_sorted.values))
    plt.figure(figsize=(25,25))
    ratings_sorted = ratings_sorted.drop(index=0.0).sort_index(ascending=False)
    sns.barplot(x=ratings_sorted.index, y=ratings_sorted.values ,palette=cool)
    plt.xticks(rotation='vertical')
    plt.xlabel("Number of Books")
    plt.ylabel('Average Rating')
    plt.title("Number of books with the average rating")
    plt.show()

