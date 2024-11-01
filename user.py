# user.py
# Author: Huy Vu
# Description: Manages the user profile and calculations related to BMI, BMR, and goal tracking.


from utils import lbs_to_kg, inches_to_cm
import datetime

class UserProfile:
    def __init__(self, name, age, gender, height, weight, activity_level, units):
        self.name = name
        self.age = age
        self.gender = gender
        self.units = units  # 'metric' or 'imperial'
        self.height_cm = self.convert_height_to_cm(height)
        self.weight_kg = self.convert_weight_to_kg(weight)
        self.activity_level = activity_level  # Sedentary, Lightly active, etc.
        self.goal_weight_kg = None
        self.weekly_weight_change = None  # kg per week
        self.start_date = datetime.date.today()

    def convert_height_to_cm(self, height):
        if self.units == 'imperial':
            return inches_to_cm(height)
        return height

    def convert_weight_to_kg(self, weight):
        if self.units == 'imperial':
            return lbs_to_kg(weight)
        return weight

    def calculate_bmi(self, weight=None):
        if weight is None:
            weight = self.weight_kg
        height_m = self.height_cm / 100
        bmi = weight / (height_m ** 2)
        return bmi

    def healthy_weight_range(self):
        height_m = self.height_cm / 100
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 24.9 * (height_m ** 2)
        return min_weight, max_weight

    def calculate_bmr(self, weight=None):
        if weight is None:
            weight = self.weight_kg
        # Mifflin-St Jeor Equation
        if self.gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            bmr = 10 * weight + 6.25 * self.height_cm - 5 * self.age - 161
        return bmr

    def calculate_tdee(self, weight=None):
        bmr = self.calculate_bmr(weight)
        activity_factors = {
            'sedentary': 1.2,
            'lightly active': 1.375,
            'moderately active': 1.55,
            'very active': 1.725,
            'extra active': 1.9
        }
        tdee = bmr * activity_factors[self.activity_level.lower()]
        return tdee

    def recommended_calorie_intake(self, weight=None):
        tdee = self.calculate_tdee(weight)
        # Calculate daily caloric deficit/surplus based on weekly weight change
        if self.weekly_weight_change:
            # 1 kg of body weight ~ 7700 calories
            daily_calorie_change = (7700 * self.weekly_weight_change) / 7
            return tdee - daily_calorie_change
        else:
            return tdee  # Maintenance if no goal is set

    def set_weight_loss_goal(self, goal_weight, weekly_weight_change):
        # Enforce safe weight loss/gain limits
        max_weekly_loss = 1.0  # kg per week
        max_weekly_gain = 0.5  # kg per week

        if self.units == 'imperial':
            goal_weight_kg = lbs_to_kg(goal_weight)
        else:
            goal_weight_kg = goal_weight

        if self.weight_kg > goal_weight_kg:
            if weekly_weight_change > max_weekly_loss:
                print(f"Weekly weight loss should not exceed {max_weekly_loss} kg.")
                self.weekly_weight_change = max_weekly_loss
            else:
                self.weekly_weight_change = weekly_weight_change
        elif self.weight_kg < goal_weight_kg:
            if weekly_weight_change > max_weekly_gain:
                print(f"Weekly weight gain should not exceed {max_weekly_gain} kg.")
                self.weekly_weight_change = max_weekly_gain
            else:
                self.weekly_weight_change = weekly_weight_change
        else:
            self.weekly_weight_change = 0  # Maintenance

        self.goal_weight_kg = goal_weight_kg
        self.start_date = datetime.date.today()

    def days_to_goal(self, current_weight=None):
        if current_weight is None:
            current_weight = self.weight_kg
        if self.weekly_weight_change == 0:
            return 0
        total_weight_change = abs(current_weight - self.goal_weight_kg)
        weeks = total_weight_change / abs(self.weekly_weight_change)
        days = weeks * 7
        return int(days)