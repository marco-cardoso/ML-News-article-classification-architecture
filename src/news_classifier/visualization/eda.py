import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def plot_wordcloud(text, title):
    """
    It plots a wordcloud based on the text variable
    :param text: A String with the text to be used
    :param title: A String with the plot title
    """
    wordcloud = WordCloud(
        background_color='white',
        scale=3,
        max_words=200,
        max_font_size=40
    ).generate(str(text))

    fig = plt.figure(1, figsize=(10, 7))

    fig.suptitle(title, fontsize=20)
    fig.subplots_adjust(top=1.1)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


def plot_char_amt_bar(df: pd.DataFrame):
    """
    It plots a bar chart comparing the median amount of
    characters of content and title by category
    :param df: A Pandas dataframe with cnt_char_amt|title_char_amt|category
    variables
    """
    group = df.groupby("category")
    content_char_avg = group['cnt_char_amt'].apply(np.median)
    title_char_avg = group['title_char_amt'].apply(np.median)

    fig, ax = plt.subplots(2, 1, figsize=(9, 12))

    content_char_avg.sort_values().plot(kind='barh', ax=ax[0])
    ax[0].set_title("Median amount of content characters by category")

    title_char_avg.sort_values().plot(kind='barh', ax=ax[1])
    ax[1].set_title("Median amount of title characters by category")

    plt.rc('font', size=13)
    plt.show()
