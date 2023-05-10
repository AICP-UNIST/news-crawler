from datetime import datetime, timedelta

from crawler import NaverNewsCrawler

start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 4, 24)

crawler = NaverNewsCrawler(start_date, end_date, max_articles=1000)
crawler.crawl_news()
crawler.save_to_csv("naver_news.csv")
