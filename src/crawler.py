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
                if content:
                    content_text = (
                        content.get_text()
                        .replace("\n", " ")
                        .replace("\t", " ")
                        .strip()
                    )
                    return content_text
                else:
                    return None
        return None

    def crawl_news(self):
        page = 1
        count = 1
        while count == 1:
            if len(self.articles) >= self.max_articles:
                break

            url = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&listType=summary&range={self.end_date.strftime('%Y%m%d')}|{self.start_date.strftime('%Y%m%d')}&page={page}"
            res = requests.get(url, headers=headers)
            soup = bs(res.content, "html.parser")
            news_list = soup.find("ul", {"class": "type06_headline"}).find_all(
                "li", {"class": ""}
            )
            news_list += soup.find("ul", {"class": "type06"}).find_all(
                "li", {"class": ""}
            )

            for news in news_list:
                print(len(self.articles))
                if len(self.articles) >= self.max_articles:
                    break
                # if news.find("dt", {"class": "photo"}) is not None:
                #     continue
                # if news.find("dt").find("span", {"class": "lede"}) is not None:
                #     continue
                article_link = news.find("a")["href"]
                print(article_link)
                article_title = news.find("a").text.strip()
                article_contents = self.find_content(article_link)
                print(article_contents)
                if article_contents is not None:
                    article_dict = self.extract_title_and_link(
                        article_title, article_link, article_contents
                    )
                    self.articles.append(article_dict)
                    self.article_dict[article_dict["title"]] = article_link
            page += 1

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.articles, columns=["title", "link", "contents"])
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
