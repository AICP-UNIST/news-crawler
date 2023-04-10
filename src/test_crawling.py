from datetime import datetime, timedelta

from crawler import NaverNewsCrawler

start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 3, 31)
max_articles = 100
query = "삼성전자"

crawler = NaverNewsCrawler(start_date, end_date, max_articles)
crawler.crawl_news(query)
crawler.save_to_csv("samsung.csv")
