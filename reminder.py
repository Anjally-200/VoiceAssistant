import json
import os

FILE_NAME = "reminders.json"


def load_reminders():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


def save_reminders(reminders):
    with open(FILE_NAME, "w") as file:
        json.dump(reminders, file, indent=4)


def add_reminder(reminder):
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)


def delete_reminder(index):
    reminders = load_reminders()

    if 0 <= index < len(reminders):
        reminders.pop(index)
        save_reminders(reminders)


def get_reminders():
    return load_reminders()