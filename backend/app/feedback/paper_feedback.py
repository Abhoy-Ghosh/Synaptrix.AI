import json
import os

FILE = "paper_feedback.json"


def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


def add_paper_feedback(title, score):
    data = load_data()

    if title not in data:
        data[title] = 0

    data[title] += score  # +1 or -1

    save_data(data)


def get_paper_score(title):
    data = load_data()
    return data.get(title, 0)