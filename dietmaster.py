# dietmaster.py
# Author: Huy Vu
# Description: Main script and entry point of the DietMaster application.

from user import UserProfile
from activity import ActivityLog
from nutrition import CalorieIntakeLog
from report import generate_pdf_report
from data_storage import DataStorage
from utils import get_float_input, get_int_input, get_choice_input, kg_to_lbs, cm_to_inches, lbs_to_kg, get_date_input
import datetime

def main():
    # Create or load user profile
    print("Welcome to DietMaster!")
    data_storage = DataStorage()
    user = data_storage.load_user_profile()

    if user:
        print(f"Welcome back, {user.name}!")
    else:
        # Measurement system selection
        units = get_choice_input("Choose your measurement system", ['metric', 'imperial'])

        # Collect user information with examples
        name = input("Enter your name (e.g., John Doe): ")
        age = get_int_input("Enter your age", example=30)
        gender = get_choice_input("Enter your gender", ['male', 'female'])
        if units == 'imperial':
            height = get_float_input("Enter your height in inches", example=70, unit='inches')
            weight = get_float_input("Enter your current weight in pounds", example=180, unit='lbs')
        else:
            height = get_float_input("Enter your height in cm", example=175, unit='cm')
            weight = get_float_input("Enter your current weight in kg", example=80, unit='kg')

        print("Activity levels: sedentary, lightly active, moderately active, very active, extra active")
        activity_level = get_choice_input("Enter your activity level", ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'])

        user = UserProfile(name, age, gender, height, weight, activity_level, units)
        data_storage.save_user_profile(user)

    # Set goal weight and weekly weight change if not already set
    if user.goal_weight_kg is None or user.weekly_weight_change is None:
        set_goal_weight(user, data_storage)

    # Calculate and display BMI
    bmi = user.calculate_bmi()
    print(f"\nYour current BMI is: {bmi:.2f}")

    # Recommend healthy weight range
    min_weight, max_weight = user.healthy_weight_range()
    if user.units == 'imperial':
        min_weight = kg_to_lbs(min_weight)
        max_weight = kg_to_lbs(max_weight)
        weight_unit = 'lbs'
    else:
        weight_unit = 'kg'
    print(f"Based on your height, a healthy weight range is {min_weight:.1f} {weight_unit} to {max_weight:.1f} {weight_unit}.")

    # Calculate and display recommended daily caloric intake
    recommended_calories = user.recommended_calorie_intake()
    print(f"\nHello {user.name}! Your recommended daily caloric intake is: {recommended_calories:.2f} calories.")

    # Estimate days to reach goal
    days_to_goal = user.days_to_goal()
    if days_to_goal > 0:
        estimated_goal_date = datetime.date.today() + datetime.timedelta(days=days_to_goal)
        print(f"Estimated days to reach your goal: {days_to_goal} days (by {estimated_goal_date}).")
    else:
        print("You have reached your goal!")

    # Initialize logs
    activity_log = ActivityLog(data_storage)
    calorie_intake_log = CalorieIntakeLog(data_storage)

    while True:
        print("\nPlease select an option:")
        print("1. Log calories intake")
        print("2. Log calories burned")
        print("3. Log weight")
        print("4. View today's summary")
        print("5. Generate PDF report")
        print("6. Check days to reach goal")
        print("7. Update personal information")
        print("8. Reset all data")
        print("9. Exit")
        choice = get_choice_input("Enter your choice", [str(i) for i in range(1, 10)])

        if choice == '1':
            date = get_date_input("Enter date (YYYY-MM-DD) or press Enter for today: ", allow_blank=True)
            calories = get_float_input("Enter total calories intake", example=2000)
            calorie_intake_log.log_calories_intake(date, calories)
        elif choice == '2':
            date = get_date_input("Enter date (YYYY-MM-DD) or press Enter for today: ", allow_blank=True)
            calories = get_float_input("Enter total calories burned", example=500)
            activity_log.log_calories_burned(date, calories)
        elif choice == '3':
            date = get_date_input("Enter date (YYYY-MM-DD) or press Enter for today: ", allow_blank=True)
            if user.units == 'imperial':
                weight = get_float_input("Enter your weight in pounds", example=180, unit='lbs')
                weight_kg = lbs_to_kg(weight)
            else:
                weight = get_float_input("Enter your weight in kg", example=80, unit='kg')
                weight_kg = weight
            data_storage.save_weight_entry(date, weight_kg)
            # Update days to goal based on new weight
            days_to_goal = user.days_to_goal(current_weight=weight_kg)
            if days_to_goal > 0:
                estimated_goal_date = datetime.date.today() + datetime.timedelta(days=days_to_goal)
                print(f"Updated estimated days to reach your goal: {days_to_goal} days (by {estimated_goal_date}).")
            else:
                print("You have reached your goal!")
        elif choice == '4':
            date = datetime.date.today()
            intake = calorie_intake_log.get_daily_intake(date)
            burned = activity_log.get_daily_activity(date)
            net_calories = intake - burned
            if intake == 0 and burned == 0:
                print(f"You did not enter the caloric measure for today.")
                break
            print(f"\nSummary for {date}:")
            print(f"Calories intake: {intake:.2f}")
            print(f"Calories burned: {burned:.2f}")
            print(f"Net calories for the day: {net_calories:.2f}")
            print(f"Recommended daily caloric intake: {recommended_calories:.2f}")
            calorie_diff = round(abs(net_calories-recommended_calories), 2)
            
            if net_calories > recommended_calories:
                print(f"You have exceeded your recommended caloric intake for the day by {calorie_diff}.")
            else:
                print(f"You are within your recommended caloric intake for the day by {calorie_diff}.")
        elif choice == '5':
            generate_pdf_report(calorie_intake_log, activity_log, user)
        elif choice == '6':
            # Get the latest weight entry
            weight_entries = data_storage.get_weight_entries()
            if weight_entries:
                latest_weight = weight_entries[-1][1]
            else:
                latest_weight = user.weight_kg
            days_to_goal = user.days_to_goal(current_weight=latest_weight)
            if days_to_goal > 0:
                estimated_goal_date = datetime.date.today() + datetime.timedelta(days=days_to_goal)
                print(f"Estimated days to reach your goal: {days_to_goal} days (by {estimated_goal_date}).")
            else:
                print("You have reached your goal!")
        elif choice == '7':
            update_user_info(user, data_storage)
            recommended_calories = user.recommended_calorie_intake()
            print(f"Your new recommended daily caloric intake is: {recommended_calories:.2f} calories.")
        elif choice == '8':
            confirm = input("Are you sure you want to reset all data? This action cannot be undone. (yes/no): ").lower()
            if confirm == 'yes':
                data_storage.clear_all_data()
                print("All data has been reset. Restarting the application.")
                main()
                return
            else:
                print("Data reset canceled.")
        elif choice == '9':
            print("Exiting DietMaster. Goodbye!")
            break

def set_goal_weight(user, data_storage):
    # Ask for user's goal weight
    if user.units == 'imperial':
        goal_weight = get_float_input("Enter your desired goal weight in pounds", example=160, unit='lbs')
    else:
        goal_weight = get_float_input("Enter your desired goal weight in kg", example=70, unit='kg')

    # Determine if weight loss or gain is needed
    if (user.units == 'imperial' and user.weight_kg != lbs_to_kg(goal_weight)) or (user.units == 'metric' and user.weight_kg != goal_weight):
        # Ask for desired weekly weight change
        if (user.units == 'imperial' and user.weight_kg > lbs_to_kg(goal_weight)) or (user.units == 'metric' and user.weight_kg > goal_weight):
            print("You need to lose weight to reach your goal.")
            max_weekly_loss = 1.0  # kg per week
            if user.units == 'imperial':
                max_weekly_loss_lbs = kg_to_lbs(max_weekly_loss)
                weekly_weight_change = get_float_input(f"Enter the amount of weight you want to lose per week (max {max_weekly_loss_lbs:.1f} lbs)", example=2, unit='lbs')
                weekly_weight_change_kg = lbs_to_kg(weekly_weight_change)
            else:
                weekly_weight_change = get_float_input(f"Enter the amount of weight you want to lose per week (max {max_weekly_loss} kg)", example=1, unit='kg')
                weekly_weight_change_kg = weekly_weight_change
            if weekly_weight_change_kg > max_weekly_loss:
                print(f"Weekly weight loss should not exceed {max_weekly_loss} kg. Setting to maximum allowable loss.")
                weekly_weight_change_kg = max_weekly_loss
        else:
            print("You need to gain weight to reach your goal.")
            max_weekly_gain = 0.5  # kg per week
            if user.units == 'imperial':
                max_weekly_gain_lbs = kg_to_lbs(max_weekly_gain)
                weekly_weight_change = get_float_input(f"Enter the amount of weight you want to gain per week (max {max_weekly_gain_lbs:.1f} lbs)", example=1, unit='lbs')
                weekly_weight_change_kg = lbs_to_kg(weekly_weight_change)
            else:
                weekly_weight_change = get_float_input(f"Enter the amount of weight you want to gain per week (max {max_weekly_gain} kg)", example=0.5, unit='kg')
                weekly_weight_change_kg = weekly_weight_change
            if weekly_weight_change_kg > max_weekly_gain:
                print(f"Weekly weight gain should not exceed {max_weekly_gain} kg. Setting to maximum allowable gain.")
                weekly_weight_change_kg = max_weekly_gain

        user.set_weight_loss_goal(goal_weight, weekly_weight_change_kg)
        data_storage.update_user_profile(user)
    else:
        print("You are already at your goal weight!")
        user.weekly_weight_change = 0  # Maintenance

def update_user_info(user, data_storage):
    print("\nUpdate Personal Information:")
    print("1. Update goal weight")
    print("2. Update weekly weight change")
    print("3. Update both goal weight and weekly weight change")
    print("4. Cancel")
    choice = get_choice_input("Enter your choice", ['1', '2', '3', '4'])

    if choice == '1':
        set_goal_weight(user, data_storage)
    elif choice == '2':
        if user.goal_weight_kg is not None:
            set_goal_weight(user, data_storage)
        else:
            print("You need to set a goal weight first.")
            set_goal_weight(user, data_storage)
    elif choice == '3':
        set_goal_weight(user, data_storage)
    elif choice == '4':
        print("Update canceled.")
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()