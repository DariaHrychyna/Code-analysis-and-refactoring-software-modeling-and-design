import matplotlib.pyplot as plt
import seaborn as sns


def plot_top_authors(author_counts, top_n=50):
    top_authors = author_counts.head(top_n)
    colors = sns.color_palette("cool", n_colors=len(top_authors))
    plt.figure(figsize=(12, 12))
    sns_plot = sns.barplot(y=top_authors.index, x=top_authors.values, palette=colors, orient='h')
    for i, value in enumerate(top_authors.values):
        sns_plot.text(value, i, int(value), ha="left",
                      va="center", color='black', fontsize=8)
    plt.ylabel("Author Names")
    plt.xlabel("Number of Books Written")
    plt.title(f"Top {top_n} authors with highest number of books written")
    plt.tight_layout()
    plt.show()


def plot_top_publishers(publisher_counts, top_n=50):
    top_publishers = publisher_counts.sort_values(ascending=False).head(top_n)
    colors = sns.color_palette("cool", n_colors=len(top_publishers))
    plt.figure(figsize=(12, 12))
    sns_plot = sns.barplot( y=top_publishers.index, x=top_publishers.values, palette=colors, orient='h')
    for i, value in enumerate(top_publishers.values):
        sns_plot.text(value, i, int(value), ha="left",
                      va="center", color='black', fontsize=8)
    plt.ylabel("Publisher Names")
    plt.xlabel("Number of Books Published")
    plt.title(f"Top {top_n} Publishers with Highest Number of Books Published")
    plt.tight_layout()
    plt.show()
