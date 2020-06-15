import matplotlib.pyplot as plt
from wordcloud import WordCloud


def plot(text, title):
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
