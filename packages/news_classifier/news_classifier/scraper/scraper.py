from datetime import datetime, timedelta
from functools import partial
from multiprocessing import Pool
from time import sleep

import requests as re
from bs4 import BeautifulSoup

from news_classifier.database import db
from news_classifier.scraper.article import GuardianArticle, ContentNotFoundException

import logging

_logger = logging.getLogger(__name__)

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

    if content_area is not None:
        anchors = content_area.find_all("a", {'data-link-name': 'article'})
        links = [anchor.get('href') for anchor in anchors]
        return list(set(links))
    return []


def get_category_articles(start_date: datetime.date, end_date: datetime.date, category: str):
    """
    It iterates daily from the start_date to the end_date downloading the articles
    This is the method used by the threads.
    :param start_date: A datetime object with the start date
    :param end_date: A datetime object with the end date
    :param category: A string with the category
    """
    total_downloaded = 0

    while start_date < end_date:
        current_year = start_date.year
        current_month = start_date.strftime("%B")[:3].lower()
        current_day = start_date.day if start_date.day >= 10 else "0" + str(start_date.day)

        _logger.info(f"Current date : {start_date}")

        url = format_url(category, current_year, current_month, current_day)
        _logger.info("Downloading articles at : " + url)

        articles_urls = get_articles_urls(url)
        _logger.info(f"Amount of articles : {len(articles_urls)}")

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
                            'published_on': start_date
                        }
                    )

                    total_downloaded += 1
                    _logger.debug(f"{total_downloaded} - Article {article_url} successfully inserted !")
                except (ContentNotFoundException, AttributeError):
                    # if i == 2:
                    #     print(f"The article {article_url} was ignored due to an unknown format !")
                    pass
                finally:
                    sleep(1)
                break

        start_date += timedelta(days=1)


def main():
    _logger.info("Scraper started !")

    latest_article_date = db.get_last_article_date()

    if latest_article_date is None:
        _logger.info("No stored articles were found in the database.")
        latest_article_date = datetime(2016, 1, 1)

    start_date = latest_article_date + timedelta(days=1)
    end_date = datetime.now()

    _logger.info(f"Articles from {start_date} to {end_date} are going to be downloaded !")

    function = partial(get_category_articles, start_date, end_date, )
    with Pool(len(CATEGORIES)) as p:
        p.map(function, CATEGORIES)
        p.close()
        p.join()

    _logger.info(f"Process finished !")


if __name__ == '__main__':
    main()
