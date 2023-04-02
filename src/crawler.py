import requests
from bs4 import BeautifulSoup as bs
import csv
from datetime import datetime, timedelta


class NaverNewsCrawler:
    def __init__(self, start_date, end_date, max_articles):
        self.start_date = start_date
        self.end_date = end_date
        self.max_articles = max_articles
        self.articles = []
        self.article_dict = {}

    def extract_title_and_link(self, url):
        article_dict = {}
        response = requests.get(url)
        html = response.text
        soup = bs(html, "html.parser")
        article_title = soup.select_one("#articleTitle").text
        article_dict["title"] = article_title
        article_dict["link"] = url
        return article_dict

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
        while True:
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
                if "news.naver.com" not in article_link:
                    continue
                article_dict = self.extract_title_and_link(article_link)
                self.articles.append(article_dict)
                self.article_dict[article_dict["title"]] = article_link
                if len(self.articles) >= self.max_articles:
                    break
            count += 1

    def save_to_csv(self, file_name):
        with open(file_name, "w", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["title", "link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for article in self.articles:
                writer.writerow(article)
