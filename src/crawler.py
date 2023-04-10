import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime, timedelta
from items import article_contents

headers = {"User-Agent": "Chrome/103.0.0.0"}


class NaverNewsCrawler:
    def __init__(self, start_date, end_date, max_articles):
        self.start_date = start_date
        self.end_date = end_date
        self.max_articles = max_articles
        self.articles = []
        self.article_dict = {}

    def extract_title_and_link(self, title, url, contents):
        article_dict = {}
        article_dict["title"] = title
        article_dict["link"] = url
        article_dict["contents"] = contents
        return article_dict

    def find_content(self, link):
        for domain, content_info in article_contents.items():
            if domain in link:
                detail_page = requests.get(
                    link,
                    headers=headers,
                )
                soup = bs(detail_page.content, "html.parser")
                content = soup.find(*content_info)
                return content
        return None

    def crawl_news(self, query):
        url = (
            "https://search.naver.com/search.naver?where=news&query="
            + query
            + "&sort=0&ds="
            + self.start_date.strftime("%Y.%m.%d")
            + "&de="
            + self.end_date.strftime("%Y.%m.%d")
            + "&nso=so%3Ar%2Cp%3Afrom"
            + self.start_date.strftime("%Y%m%d")
            + "to"
            + self.end_date.strftime("%Y%m%d")
            + "%2Ca%3A&start="
        )
        count = 1
        while count == 1:
            if len(self.articles) >= self.max_articles:
                break
            if count == 1:
                res = requests.get(url)
            else:
                res = requests.get(url + str((count - 1) * 10 + 1))
            html = res.text
            soup = bs(html, "html.parser")
            links = soup.select(".news_area > a")

            for link in links:
                article_link = link["href"]
                article_title = link["title"]
                print(article_link)
                article_contents = self.find_content(article_link)
                article_dict = self.extract_title_and_link(
                    article_title, article_link, article_contents
                )
                self.articles.append(article_dict)
                self.article_dict[article_dict["title"]] = article_link
                if len(self.articles) >= self.max_articles:
                    break
            count += 1

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.articles, columns=["title", "link", "contents"])
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
