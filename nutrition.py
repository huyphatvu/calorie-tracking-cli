# nutrition.py
# Author: Huy Vu
# Description: Manages logging and retrieval of daily calorie intake.

from data_storage import DataStorage

class CalorieIntakeLog:
    def __init__(self, data_storage):
        self.data_storage = data_storage

    def log_calories_intake(self, date, calories):
        self.data_storage.save_calorie_intake(date, calories)
        print(f"Logged {calories} calories intake on {date}.")

    def get_daily_intake(self, date):
        calories = self.data_storage.get_calorie_intake(date)
        if calories:
            return calories
        else:
            return 0