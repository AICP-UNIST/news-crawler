from datetime import datetime, timedelta

from crawler import MaeilNewsCrawler

start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 4, 24)

crawler = MaeilNewsCrawler(
    start_date, end_date, max_articles=1000, keyword="채권"
)
crawler.crawl_news()
crawler.save_to_csv("mk_news.csv")
