from datetime import datetime, timedelta

from crawler import MaeilNewsCrawler

start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 7, 10)

crawler = MaeilNewsCrawler(
    start_date, end_date, max_articles=100, keyword="반도체"
)
crawler.crawl_news()
crawler.save_to_csv("반도체_keyword.csv")
# crawler.save_keywords("반도체_keyword.csv")
