from time import sleep

import requests as re
from bs4 import BeautifulSoup


class ContentNotFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GuardianArticle(object):
    """
    This class is responsible to download and format a news article
    """

    def __init__(self, url: str):
        super().__init__()

        response = re.get(url)
        self.soup = BeautifulSoup(response.text, features="html.parser")

        self.title = self._get_article_title()
        self.content = self._get_article_content()

        self.published_on = self._get_article_published_date()
        self.topics = self._get_article_topics()

        print(url)
        sleep(1)

    def _get_article_title(self) -> str:
        """
        :return: The news title
        """
        h1 = self.soup.find("h1", {"class": "css-rtdfvn"})
        if h1 is not None:
            title = h1.text
        else:
            title = self.soup.find("h1", {"class": "content__headline"}).text

        return title.replace("\n", "")

    def _get_article_content(self):

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
                "This could be happening due to an article with different format...")

        paragraphs = paragraphs.find_all(["p", "blackquote"])

        paragraphs = filter(
            self._filter_paragraphs,
            paragraphs
        )

        paragraphs = map(
            self._clean_paragraph,
            paragraphs
        )
        return paragraphs

    def _get_article_topics(self):
        div = self.soup.find("div", {"class": "submeta"})
        if div is not None:
            return div.find_all("li")
        else:
            main_topic = list(self.soup.find("ul", {"class": "css-o9b79t"}).find_all("li"))
            related_topics = list(self.soup.find("ul", {"class": "css-q1ot1l"}).find_all("li"))
            return main_topic + related_topics

    def _get_article_published_date(self):
        div = self.soup.find("div", {"class": "css-1kkxezg"})
        if div is not None:
            return div.text
        else:
            return self.soup.find("time", {"class": "content__dateline-wpd"}).get("timestamp")

    def _filter_paragraphs(self, paragraph):
        return (
                paragraph.get("class") is None
                or
                (("block-time" not in paragraph.get("class")) and
                 ("liveblog-block-byline__name" not in paragraph.get("class"))
                 )
        )

    def _clean_paragraph(self, paragraph):
        return paragraph.text.replace("\n", "")
