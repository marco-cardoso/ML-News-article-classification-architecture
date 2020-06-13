from datetime import datetime, timedelta
from functools import partial
from multiprocessing import Pool
from time import sleep

import requests as re
from bs4 import BeautifulSoup

from utils.article import GuardianArticle, ContentNotFoundException
from database.main import Database

CATEGORIES = [
    'politics',
    'environment',
    'science',
    'global-development',
    'sport',
    'culture',
    'lifeandstyle',
    'tech',
    'business'
]


def format_url(category: str, year: int, month: str, day: str) -> str:
    """

    It returns a URL from The Guardian website with links for the articles of the given date
    and category

    :param category: A String representing the category
    :param year: An integer representing the year
    :param month: A String representing the first three letters of the month in lower case
    :param day: A String representing the day
    :return: The URL
    """
    return f"https://www.theguardian.com/{category}/{year}/{month}/{day}"


def get_articles_urls(url: str) -> list:
    """
    In order to download the articles it's necessary to know their links.
    This method gets the links of the articles from a specific category and date.
    :param url: The URL of the website following a specific format
    :return: A List with the URLs of the articles
    """
    sleep(1)
    response = re.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    content_area = soup.find("div", {'class': "fc-container__inner"})
    anchors = content_area.find_all("a", {'data-link-name': 'article'})
    links = [anchor.get('href') for anchor in anchors]
    return list(set(links))


def get_category_articles(amount_of_articles: int, category: str):
    """
    It downloads and saves N articles from the given category in MongoDB.
    This is the method used by the threads.
    :param amount_of_articles: An integer with the value of N
    :param category: A string with the category
    """
    total_downloaded = 0
    current_date = datetime.now()
    db = Database()

    while total_downloaded < amount_of_articles:
        current_year = current_date.year
        current_month = current_date.strftime("%B")[:3].lower()
        current_day = current_date.day if current_date.day >= 10 else "0" + str(current_date.day)

        url = format_url(category, current_year, current_month, current_day)
        print(url)

        articles_urls = get_articles_urls(url)

        for article_url in articles_urls:

            # This loop is necessary because sometimes the server sends a page
            # with unknown HTML classes. The approach is to try to get a recognizable
            # page three times. If none attempt works then the article is ignored.
            for i in range(3):

                try:
                    article = GuardianArticle(article_url)
                    db.insert_article(
                        {
                            'category': category,
                            'title': article.title,
                            'content': article.get_content_str(),
                            'topics': article.topics,
                            'published_on': current_date
                        }
                    )

                    total_downloaded += 1
                    print(f"{total_downloaded} - Article {article_url} successfully inserted !")
                    break
                except (ContentNotFoundException, AttributeError):
                    # if i == 2:
                    #     print(f"The article {article_url} was ignored due to an unknown format !")
                    pass
                finally:
                    sleep(1)

        current_date -= timedelta(days=1)


def main():
    amount_articles = 1000
    function = partial(get_category_articles, amount_articles, )
    with Pool(len(CATEGORIES)) as p:
        p.map(function,  CATEGORIES)
        p.join()
        p.close()


if __name__ == '__main__':
    main()
