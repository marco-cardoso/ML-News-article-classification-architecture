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

    It formats the 'The Guardian' URL based on the given category, year, month and day.

    :param category:
    :param year:
    :param month:
    :param day:
    :return: The URL
    """
    return f"https://www.theguardian.com/{category}/{year}/{month}/{day}"


def main():
    pass


if __name__ == '__main__':
    main()
