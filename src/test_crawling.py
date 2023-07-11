from datetime import datetime, timedelta

from crawler import MaeilNewsCrawler

start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 7, 10)

crawler = MaeilNewsCrawler(start_date, end_date, max_articles=100, keyword="채권")
crawler.crawl_news()
crawler.save_to_csv("mk_news.csv")
crawler.save_keywords("채권_keyword.csv")
