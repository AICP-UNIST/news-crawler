import csv


def load_csv(filename):
    articles = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            title = row[0]
            link = row[1]
            contents = row[2]
            articles.append(
                {"title": title, "link": link, "contents": contents}
            )
    return articles
