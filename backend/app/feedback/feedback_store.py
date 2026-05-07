import json
import os

FEEDBACK_FILE = "feedback.json"


def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return {}
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f)


def add_feedback(topic, feedback):
    data = load_feedback()
    data[topic.lower()] = feedback
    save_feedback(data)


def get_feedback(topic):
    data = load_feedback()
    return data.get(topic.lower())
