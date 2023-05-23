import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime, timedelta
from items import article_contents

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


class MaeilNewsCrawler:
    def __init__(self, start_date, end_date, max_articles, keyword):
        self.start_date = start_date
        self.end_date = end_date
        self.max_articles = max_articles
        self.articles = []
        self.article_dict = {}
        self.keyword = keyword

    def extract_title_and_link(self, title, url, date):
        article_dict = {}
        article_dict["title"] = title
        article_dict["link"] = url
        # article_dict["contents"] = contents
        article_dict["date"] = date
        return article_dict

    def find_content(self, link):
        detail_page = requests.get(
            link,
            headers=headers,
        )
        soup = bs(detail_page.content, "html.parser")
        content = soup.select_one(
            "#container > section > div.news_detail_body_group > section > div.min_inner > div.sec_body > div.news_cnt_detail_wrap"
        )
        if content:
            content_text = (
                content.get_text().replace("\n", " ").replace("\t", " ").strip()
            )
            return content_text
        else:
            return None

    def crawl_news(self):
        page = 1
        count = 1
        while count == 1:
            if len(self.articles) >= self.max_articles:
                break
            url = f"https://find.mk.co.kr/new/search.php?pageNum={page}&cat=&cat1=&media_eco=&pageSize=20&sub=news&dispFlag=OFF&page=news&s_kwd={self.keyword}&s_page=news&go_page=&ord=1&ord1=1&ord2=0&s_keyword={self.keyword}&s_i_keyword={self.keyword}&s_author=&y1=2020&m1=05&d1=23&y2=2023&m2=05&d2=23&ord=1&area=ttbd"
            print(url)
            res = requests.get(url, headers=headers)
            print(res)
            soup = bs(res.content, "html.parser")
            news_list = soup.find_all("div", {"class": "sub_list"})
            for news in news_list:
                print(len(self.articles))
                if len(self.articles) >= self.max_articles:
                    break
                article_link = news.find("a")["href"]
                article_title = news.find(
                    "span", {"class": "art_tit"}
                ).text.strip()
                article_date = news.find(
                    "span", {"class": "art_time"}
                ).text.strip()
                print(article_title)
                print(article_link)
                article_dict = self.extract_title_and_link(
                    article_title,
                    article_link,
                    article_date,
                )
                self.articles.append(article_dict)
                self.article_dict[article_dict["title"]] = article_link
            page += 1

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.articles, columns=["title", "link", "date"])
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
