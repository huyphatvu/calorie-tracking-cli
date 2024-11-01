# report.py
# Author: Huy Vu
# Description: Generates a PDF report including user information, achievements, and metrics graphs.

import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rcParams
from utils import kg_to_lbs, cm_to_inches

def generate_pdf_report(calorie_intake_log, activity_log, user):
    # Set up font sizes
    rcParams['font.size'] = 10
    title_font = {'fontsize': 16, 'fontweight': 'bold'}
    h1_font = {'fontsize': 14, 'fontweight': 'bold'}
    h2_font = {'fontsize': 12, 'fontweight': 'bold'}
    h3_font = {'fontsize': 11, 'fontweight': 'bold'}
    p_font = {'fontsize': 10}
    
    dates = []
    net_calories = []
    expected_calories = []
    weight_dates = []
    weights = []
    
    # Calculate net calories and expected calories
    all_dates = calorie_intake_log.data_storage.get_all_dates()
    start_date = user.start_date
    if user.goal_weight_kg and user.weekly_weight_change:
        daily_expected_calorie_change = (7700 * user.weekly_weight_change) / 7
    else:
        daily_expected_calorie_change = 0

    for date_str in all_dates:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        intake = calorie_intake_log.get_daily_intake(date_obj)
        burned = activity_log.get_daily_activity(date_obj)
        net_cal = intake - burned
        days_since_start = (date_obj - start_date).days
        dates.append(days_since_start)
        net_calories.append(net_cal)
        expected_calories.append(daily_expected_calorie_change)
    
    # Get weight entries
    weight_entries = calorie_intake_log.data_storage.get_weight_entries()
    for entry in weight_entries:
        date_str, weight_kg = entry
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        days_since_start = (date_obj - start_date).days
        weight_dates.append(days_since_start)
        if user.units == 'imperial':
            weight = kg_to_lbs(weight_kg)
        else:
            weight = weight_kg
        weights.append(weight)
    
    # Calculate achievements
    if weights:
        starting_weight = weights[0]
        latest_weight = weights[-1]
    else:
        if user.units == 'imperial':
            starting_weight = kg_to_lbs(user.weight_kg)
            latest_weight = starting_weight
        else:
            starting_weight = user.weight_kg
            latest_weight = starting_weight
    
    total_weight_change = starting_weight - latest_weight
    
    days_to_goal = user.days_to_goal(current_weight=latest_weight if weights else user.weight_kg)
    if days_to_goal > 0:
        estimated_goal_date = datetime.date.today() + datetime.timedelta(days=days_to_goal)
        achievement_text = (
            f"You have {'lost' if total_weight_change > 0 else 'gained'} {abs(total_weight_change):.2f} "
            f"{'lbs' if user.units == 'imperial' else 'kg'} so far.\n"
            f"Estimated days to reach your goal: {days_to_goal} days (by {estimated_goal_date})."
        )
    else:
        achievement_text = "Congratulations! You have reached your goal weight!"
    
    # Generate PDF report
    with PdfPages('dietmaster_report.pdf') as pdf:
        # Page 1: Title and User Information
        fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 size in inches
        plt.axis('off')
        
        y_position = 1  # Start from the top

        # Title centered
        plt.text(0.5, y_position, "DietMaster Report", ha='center', **title_font)
        y_position -= 0.05

        # H1 Header: User Information, aligned to left with numbering
        plt.text(0.1, y_position, "1. User Information", ha='left', **h1_font)
        y_position -= 0.14

        # User Information Paragraph
        if user.units == 'imperial':
            height = cm_to_inches(user.height_cm)
            height_unit = 'inches'
            weight_unit = 'lbs'
            starting_weight = kg_to_lbs(user.weight_kg)
            goal_weight = kg_to_lbs(user.goal_weight_kg)
        else:
            height = user.height_cm
            height_unit = 'cm'
            weight_unit = 'kg'
            starting_weight = user.weight_kg
            goal_weight = user.goal_weight_kg

        user_info = (
            f"Name: {user.name}\n"
            f"Age: {user.age}\n"
            f"Gender: {user.gender.capitalize()}\n"
            f"Height: {height:.1f} {height_unit}\n"
            f"Starting Weight: {starting_weight:.1f} {weight_unit}\n"
            f"Goal Weight: {goal_weight:.1f} {weight_unit}\n"
            f"Activity Level: {user.activity_level.capitalize()}"
        )
        plt.text(0.1, y_position, user_info, ha='left', **p_font)
        y_position -= 0.1  # Adjust spacing

        # H2 Header: Achievements
        plt.text(0.1, y_position, "2. Achievements", ha='left', **h2_font)
        y_position -= 0.05

        # Achievements Paragraph
        plt.text(0.1, y_position, achievement_text, ha='left', **p_font)
        y_position -= 0.1  # Adjust spacing

        # H3 Header: Metrics
        plt.text(0.1, y_position, "3. Metrics", ha='left', **h3_font)
        y_position -= 0.04

        # Note: Metrics graphs will be on subsequent pages

        # Save the first page
        pdf.savefig(fig)
        plt.close()

        # Page 2: Metrics - Calories Burned and Expected
        fig, ax = plt.subplots()
        if dates:
            ax.plot(dates, net_calories, marker='o', label='Net Calories')
            ax.plot(dates, expected_calories, marker='x', label='Expected Calorie Change')
            ax.set_xlabel('Days Since Start')
            ax.set_ylabel('Calories')
            ax.set_title('Net Calories vs. Expected Calories Over Time', fontsize=12)
            ax.legend()
            ax.grid(True)
            pdf.savefig()
            plt.close()
        else:
            print("No calorie data available for the metrics graph.")

        # Page 3: Metrics - Weight Over Time
        fig, ax = plt.subplots()
        if weight_dates:
            ax.plot(weight_dates, weights, marker='o')
            ax.set_xlabel('Days Since Start')
            ax.set_ylabel(f'Weight ({weight_unit})')
            ax.set_title('Weight Over Time', fontsize=12)
            ax.grid(True)
            pdf.savefig()
            plt.close()
        else:
            print("No weight data available for the weight graph.")

    print("Report exported to 'dietmaster_report.pdf'")