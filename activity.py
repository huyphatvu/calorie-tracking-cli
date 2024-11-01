# activity.py

from data_storage import DataStorage

class ActivityLog:
    def __init__(self, data_storage):
        self.data_storage = data_storage

    def log_calories_burned(self, date, calories):
        self.data_storage.save_calories_burned(date, calories)
        print(f"Logged {calories} calories burned on {date}.")

    def get_daily_activity(self, date):
        calories_burned = self.data_storage.get_calories_burned(date)
        if calories_burned:
            return calories_burned
        else:
            return 0