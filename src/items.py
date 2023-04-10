# Item classes for data extraction
article_contents = {
    "naver": ("div", {"id": "newsct_article"}),
    "daum": ("div", {"id": "articleBody"}),
    "chosun": ("section", {"class": "article-body"}),  # 조선일보
    "hani": ("div", {"class": "article-text"}),  # 한겨례
    "khan": ("div", {"class": "article-body"}),  # 경향
    "joongang": ("div", {"id": "article_body"}),  # 중앙일보
    "jtbc": ("div", {"class": "article_content"}),  # JTBC
    "www.newsis.com": ("div", {"class": "viewer"}),  # 뉴시스
    "news.mt.co.kr": ("div", {"id": "textBody"}),  # 머니투데이
    "moneys": ("div", {"class": "article-body"}),  # 머니s
    "bbc": ("div", {"class": "story-body__inner"}),
    "cnn": ("div", {"class": "zn-body__paragraph"}),
    "yna.kr": ("article", {"class": "story-news article"}),
    "www.hankyung.com": (
        "div",
        {
            "class": "article-body",
            "id": "articletxt",
            "itemprop": "articleBody",
        },
    ),
    "news.mk.co.kr": ("div", {"itemprop": "articleBody"}),
    "view.asiae.co.kr": ("div", {"itemprop": "articleBody"}),
    "www.donga.com": ("div", {"class": "article_txt"}),
    "www.edaily.co.kr": ("div", {"class": "news_body"}),
    "www.nocutnews.co.kr": ("div", {"id": "pnlContent"}),
    "www.news1.kr": ("div", {"id": "articles_detail"}),
    "etnews.com": ("div", {"id": "article_txt"}),
    "sbs.co.kr": ("div", {"class": "article_body"}),
    "zdnet.co.kr": ("div", {"id": "articleBody"}),
    "kmib.co.kr": ("div", {"id": "articleBody"}),
}
