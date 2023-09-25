import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from utils import get_date

driver = webdriver.Chrome(ChromeDriverManager().install())

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Cookie": "x4ok35v1toqp99; PCID=16848447385550013134075; _sas_id.01.646b=8ccdf99344e13d74.1684845360.; __gsas=ID=4efe80e366f37cc7:T=1684846222:S=ALNI_MbQp1BTrU_wr_b5dl1xbqSG7k7-oA; _ga_5XLB868E5V=GS1.1.1684850867.2.1.1684851283.60.0.0; _cc_id=ae689a86aeb7e01f2f3eda28bc58f8be; WMONID=PSIRD8CG96R; token=dmtEdjlLWUlvUDJFMDR3bFp3UmZHR3J0UmlLb1RRWFNGWDIwcEVveUpCUjYwb3pMTk9UNDAwczNlSFdKaHhCZnlMM3ZHNzhOaUV5VmI4UVM4R05DRHE2ZlM1bGttUG85U3Qxem5UU1VXU2RXcU4wdDdnUHhMcVYzVm1qRzlpSU43R3A3OU04WEZ5c3Q3T0RhakNzZGhrTUVkN1kyUGFmS2Zkb2JvUUszajA4PQ; cUserID=wsws1844%40naver.com; cUserID_New=wsws1844%40naver.com; cSequenceID=10090643; cSequenceID_New=10090643; cTokenIndex=90643; cCorp_New=2; login_type=kakao; user_membership_date=2023.07.06; cUserEmail=wsws1844%40naver.com; cUserName_New=%20; _gid=GA1.3.1608248820.1691471825; _sas_ses.01.646b=1; cto_bundle=_mROX18xZm4zMmt4NyUyRnZBNmslMkJKZkpUeHZGV3oycFhXZGl2OVVoQml1QjFaVW1uU052d2hlQ3BENXZoU2xYUlJhOGFXYm1ndGJ4ZWxYem5iRlV0SlZuNiUyRmtDJTJGM3Q4aXlGM1ZxZVl0SUJjTXVMNHJnT050Zm9TTVAzZFFYajZWdW4lMkZIWUtQOSUyRkJmcFdsaUtsNklmdXE4ZFA4ZHclM0QlM0Q; trc_cookie_storage=taboola%2520global%253Auser-id%3Dd28fc627-c1f7-41c6-9e40-c14314999ce4-tuctb569aa7; panoramaId_expiry=1692076937785; panoramaId=a04b875ed72cd0c6219fac22c83616d5393821bfc6342d19b140e0ae8a18bf80; panoramaIdType=panoIndiv; MK_total_search_history=%5B%22%EB%B0%98%EB%8F%84%EC%B2%B4%22%5D; gtm_session_start=1691473947631; gtm_session_threshold=true; _gat_UA-24472307-100=1; _ga=GA1.1.324696011.1684844739; _ga_BT00CPT9ZL=GS1.3.1691471825.6.1.1691475605.60.0.0; _ga_44X8BY3Y81=GS1.1.1691471825.8.1.1691475607.58.0.0; _ga_PCEC2HQM86=GS1.1.1691471825.6.1.1691475607.58.0.0",
}


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
        content = self.find_content(url)
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
            dates = []
            get_date(self.start_date, self.end_date, dates)
            for date in dates:
                url = f"https://www.mk.co.kr/search?word=반도체&dateType=direct&startDate={date}&endDate={date}&page={page}&highlight=Y&page_size=null&id=null"
                res = requests.get(url, headers=headers)
                soup = bs(res.content, "html.parser")
                news_list = soup.find_all("li", {"class": "news_node"})

                for news in news_list:
                    print(len(self.articles))
                    if len(self.articles) >= self.max_articles:
                        break
                    article_link = news.find("a")["href"]
                    article_title = news.find(
                        "h3", {"class": "news_ttl"}
                    ).text.strip()
                    print(article_title)
                    article_date = news.find(
                        "p", {"class": "time_info"}
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
                page += 1

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.articles, columns=["title", "link", "date"])
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
