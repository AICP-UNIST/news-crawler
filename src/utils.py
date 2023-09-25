# Helper functions and utilities
import re
from datetime import datetime, timedelta


def get_date(start_date, end_date, dates):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start
    while current_date <= end:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)


def preprocess_data(data):
    data = re.sub(r"[\'\[\]]", "", data)
    words = re.split(r"[,\n]", data)
    preprocessed_words = []
    for word in words:
        word = word.strip()
        word = re.sub(r"\d+\.", "", word)
        if word:
            preprocessed_words.append(word)

    return preprocessed_words
