# data_storage.py

import sqlite3
import json
from datetime import date, datetime
from user import UserProfile
from utils import kg_to_lbs, cm_to_inches

class DataStorage:
    def __init__(self):
        self.conn = sqlite3.connect('dietmaster.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # User profile table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
        # Calorie intake log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calorie_intake_log (
                date TEXT PRIMARY KEY,
                calories REAL
            )
        ''')
        # Activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                date TEXT PRIMARY KEY,
                calories_burned REAL
            )
        ''')
        # Weight log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weight_log (
                date TEXT PRIMARY KEY,
                weight REAL
            )
        ''')
        self.conn.commit()

    def save_user_profile(self, user):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM user_profile')
        # Convert date objects to strings
        user_data = user.__dict__.copy()
        if isinstance(user_data.get('start_date'), date):
            user_data['start_date'] = user_data['start_date'].isoformat()
        data = json.dumps(user_data)
        cursor.execute('INSERT INTO user_profile (data) VALUES (?)', (data,))
        self.conn.commit()

    def update_user_profile(self, user):
        self.save_user_profile(user)

    def load_user_profile(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT data FROM user_profile')
        result = cursor.fetchone()
        if result:
            data = json.loads(result[0])
            user = UserProfile(
                data['name'],
                data['age'],
                data['gender'],
                data['height_cm'] if data['units'] == 'metric' else cm_to_inches(data['height_cm']),
                data['weight_kg'] if data['units'] == 'metric' else kg_to_lbs(data['weight_kg']),
                data['activity_level'],
                data['units']
            )
            user.goal_weight_kg = data.get('goal_weight_kg')
            user.weekly_weight_change = data.get('weekly_weight_change')
            # Convert start_date back to date object
            start_date_str = data.get('start_date')
            if start_date_str:
                user.start_date = datetime.fromisoformat(start_date_str).date()
            else:
                user.start_date = None
            return user
        else:
            return None

    def save_calorie_intake(self, date, calories):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO calorie_intake_log (date, calories) VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET calories = calories + excluded.calories
        ''', (date, calories))
        self.conn.commit()

    def get_calorie_intake(self, date):
        cursor = self.conn.cursor()
        cursor.execute('SELECT calories FROM calorie_intake_log WHERE date = ?', (date,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def save_calories_burned(self, date, calories):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO activity_log (date, calories_burned) VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET calories_burned = calories_burned + excluded.calories_burned
        ''', (date, calories))
        self.conn.commit()

    def get_calories_burned(self, date):
        cursor = self.conn.cursor()
        cursor.execute('SELECT calories_burned FROM activity_log WHERE date = ?', (date,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def get_all_dates(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT date FROM calorie_intake_log UNION SELECT date FROM activity_log UNION SELECT date FROM weight_log')
        dates = sorted(set(row[0] for row in cursor.fetchall()))
        return dates

    def save_weight_entry(self, date, weight):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO weight_log (date, weight) VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET weight = excluded.weight
        ''', (date, weight))
        self.conn.commit()

    def get_weight_entries(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT date, weight FROM weight_log ORDER BY date')
        entries = cursor.fetchall()
        return entries