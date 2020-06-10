from datetime import datetime, timedelta

import requests as re
from bs4 import BeautifulSoup

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
    response = re.get(url)
    soup = BeautifulSoup(response.text)

    content_area = soup.find("div", {'class': "fc-container__inner"})
    anchors = content_area.find_all("a", {'data-link-name': 'article'})
    links = [anchor.get('href') for anchor in anchors]
    return links


def download_article(url: str):
    response = re.get(url)
    pass


def main():
    amount_articles = 1000

    for category in CATEGORIES:

        total_downloaded = 0
        current_date = datetime.now()

        while total_downloaded < amount_articles:
            current_year = current_date.year
            current_month = current_date.strftime("%B")[:3].lower()
            current_day = current_date.day if current_date.day >= 10 else "0" + str(current_date.day)

            url = format_url(category, current_year, current_month, current_day)

            articles_urls = get_articles_urls(url)

            # TODO Download the articles and save them somewhere

            total_downloaded = len(articles_urls)
            current_date -= timedelta(days=1)


if __name__ == '__main__':
    main()
