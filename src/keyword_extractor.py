import csv
import openai
from dotenv import load_dotenv
import os

load_dotenv()


def summarize(openai: any, answer: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"이 내용 한국어로 세문장으로 요약해줘 ###\n{answer}\n###",
            }
        ],
    )
    return completion.choices[0].message.content


def extract_keyword(openai: any, answer: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"이 내용의 키워드 하나를 추출해줘 ###\n{answer}\n###",
            }
        ],
    )
    return completion.choices[0].message.content


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


if __name__ == "__main__":
    filename = "mk_news.csv"
    articles = load_csv(filename)
    openai.api_key = os.environ.get("API_KEY")
    messages = []

    for article in articles:
        summarized = summarize(openai, article.title)
        print("------------SUMMARIZED-----------")
        print(summarized)
        print("---------------------------------")

        keyword = extract_keyword(openai, article.title)
        print("--------------KEYWORD------------")
        print(keyword)
        print("---------------------------------")

        messages.append({"role": "assistant", "content": summarized})

        messages.append({"role": "assistant", "content": keyword})

# 여기서 title에 대해서가 아니라 body에 대해서 하는 방식으로 바꿔야할 거 같음
# 일단 시각화하는 방식이 필요함
# 일단 굵직굵직한 키워드들에 대해서 주요 키워드를 뽑아내야함.
# 그 결과 이제 채권 키워드와 코스피의 관계, 부동산 키워드와 코스피의 관계
# 금리와 코스피의 관계 등등 주요 키워드와 코스피의 관계를 알 수 있다.

# 더 진행해야하는 부분
# * 주요 키워드들을 더파악해야함
# *
