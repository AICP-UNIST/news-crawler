import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime, timedelta
from items import article_contents
import re
import keyword_extractor as ke
import openai
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


def preprocess_data(data):
    data = re.sub(r"[\'\[\]]", "", data)
    words = re.split(r"[,\n]", data)
    preprocessed_words = []
    for word in words:
        word = word.strip()
        word = re.sub(r"\d+\.", "", word)
        if word:
            preprocessed_words.append(word)

    return preprocessed_words


class MaeilNewsCrawler:
    def __init__(self, start_date, end_date, max_articles, keyword):
        self.start_date = start_date
        self.end_date = end_date
        self.max_articles = max_articles
        self.articles = []
        self.article_dict = {}
        self.keyword = keyword
        self.keyword_dict = {}

    def extract_title_and_link(self, title, url, date):
        article_dict = {}
        article_dict["title"] = title
        article_dict["link"] = url
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
            res = requests.get(url, headers=headers)
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
                article_dict = self.extract_title_and_link(
                    article_title,
                    article_link,
                    article_date,
                )
                self.articles.append(article_dict)
                self.article_dict[article_dict["title"]] = article_link
                article_date_key = ""
                pattern = r"\d+년 \d+월 \d+일 \s*\d+:\d+:\d+"
                matches = re.findall(pattern, article_date)
                if matches:
                    date_str = matches[0]
                    date_obj = datetime.strptime(
                        date_str, "%Y년 %m월 %d일 %H:%M:%S"
                    )
                    article_date_key = date_obj.strftime("%Y.%m.%d")
                print(article_date_key, article_title)
                if article_date_key not in self.keyword_dict:
                    self.keyword_dict[article_date_key] = []
                openai.api_key = os.environ.get("API_KEY")
                result = ke.extract_keyword(openai, article_title)
                print("--------------KEYWORD------------")
                print(result)
                print("---------------------------------")
                if result:
                    self.keyword_dict[article_date_key].append(result)
                # 결과물 : 날짜별 키워드 모음
                # 이후에 해야할 것
                # * 날짜별 키워드 맵 만들기
            page += 1

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.articles, columns=["title", "link", "date"])
        df.to_csv(file_name, index=False, encoding="utf-8-sig")

    def save_keywords(self, file_name):
        df = pd.DataFrame(columns=["date", "keywords"])

        for date, keywords in self.keyword_dict.items():
            df = df.append(
                {"date": date, "keywords": keywords},
                ignore_index=True,
            )

        df.to_csv(file_name, index=False, encoding="utf-8-sig")
