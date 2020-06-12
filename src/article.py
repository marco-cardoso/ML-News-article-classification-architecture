from datetime import datetime

import requests as re
from bs4 import BeautifulSoup


class ContentNotFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GuardianArticle:
    """
    This class is responsible to download and format a news article
    """

    def __init__(self, url: str):
        super().__init__()

        response = re.get(url)
        self.soup = BeautifulSoup(response.text, features="html.parser")

        self.title = self._get_article_title()
        self.content = self._get_article_content_paragraphs()

        self.published_on = self._get_article_published_date()
        self.topics = self._get_article_topics()

    def _get_article_title(self) -> str:
        """
        It gets the article title from the self.soup class attribute
        :return: The news title
        """
        if self.soup.find("h1", {"class": "css-rtdfvn"}) is not None:
            title = self.soup.find("h1", {"class": "css-rtdfvn"}).text
        elif self.soup.find("h1", {"class": "content__headline"}) is not None:
            title = self.soup.find("h1", {"class": "content__headline"}).text
        elif self.soup.find("h1", {"class": "content__header"}) is not None:
            title = self.soup.find("h1", {"class": "content__header"}).text
        else:
            raise ContentNotFoundException(
                "The title for the given article URL was not found ! \n"
                "This could be happening due to an article with different HTML format...")

        return title.replace("\n", "")

    def _get_article_content_paragraphs(self) -> list:
        """
        It gets the article content from the self.soup class attribute
        :return: The article content paragraphs
        """

        if self.soup.find("div", {"class": "css-o9b79t"}) is not None:
            paragraphs = self.soup.find("div", {"class": "css-o9b79t"})
        elif self.soup.find("div", {"class": "js-article__container"}) is not None:
            paragraphs = self.soup.find("div", {"class": "js-article__container"})
        elif self.soup.find("div", {"class": "content__article-body"}) is not None:
            paragraphs = self.soup.find("div", {"class": "content__article-body"})
        elif self.soup.find("div", {"class": "article-body-commercial-selector"}) is not None:
            paragraphs = self.soup.find("div", {"class": "article-body-commercial-selector"})
        else:
            raise ContentNotFoundException(
                "The content for the given article URL was not found ! \n"
                "This could be happening due to an article with different HTML format...")

        paragraphs = paragraphs.find_all(["p", "blackquote"])

        paragraphs = filter(
            self._filter_paragraphs,
            paragraphs
        )

        paragraphs = map(
            self._clean_paragraph,
            paragraphs
        )
        return list(paragraphs)

    def _get_article_topics(self) -> list:
        """
       It gets the article topics from the self.soup class attribute
       :return: The article topics
       """

        if self.soup.find("div", {"class": "submeta"}) is not None:
            topics = list(map(self._clean_paragraph, self.soup.find("div", {"class": "submeta"}).find_all("li", {"class": "submeta__link-item"})))
            return topics
        else:
            raise ContentNotFoundException(
                "The topics for the given article URL was not found ! \n"
                "This could be happening due to an article with different HTML format...")

    def _get_article_published_date(self) -> datetime:
        """
       It gets the article published date from the self.soup class attribute
       :return: The article content paragraphs
       """

        if self.soup.find("div", {"class": "css-1kkxezg"}) is not None:
            return self.soup.find("div", {"class": "css-1kkxezg"}).text
        elif self.soup.find("time", {"class": "content__dateline-wpd"}) is not None:
            return self.soup.find("time", {"class": "content__dateline-wpd"}).get("timestamp")
        else:
            raise ContentNotFoundException(
                "The published date for the given article URL was not found ! \n"
                "This could be happening due to an article with different HTML format...")

    def _filter_paragraphs(self, paragraph) -> bool:
        """
        It returns true if the paragraph is valid and false otherwise.
        Date of paragraph and author are useless data.
        :param paragraph: A BeautifulSoup object
        :return: A boolean indicating whether the paragraph is valid or not
        """
        return (
                paragraph.get("class") is None
                or
                (("block-time" not in paragraph.get("class")) and
                 ("liveblog-block-byline__name" not in paragraph.get("class"))
                 )
        )

    def _clean_paragraph(self, paragraph) -> str:
        """
        It converts a BeautifulSoup object in a string and
        remove unwanted characters. Such as \n
        :param paragraph: A BeautifulSoup object
        :return: A formatted string representing the paragraph
        """
        return paragraph.text.replace("\n", "")
