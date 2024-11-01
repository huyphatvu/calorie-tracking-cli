# report.py

import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_pdf import PdfPages

def generate_pdf_report(calorie_intake_log, activity_log, user):
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
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        intake = calorie_intake_log.get_daily_intake(date_str)
        burned = activity_log.get_daily_activity(date_str)
        net_cal = intake - burned
        dates.append((date_obj - datetime.datetime.combine(start_date, datetime.datetime.min.time())).days)
        net_calories.append(net_cal)
        expected_calories.append(daily_expected_calorie_change)

    # Get weight entries
    weight_entries = calorie_intake_log.data_storage.get_weight_entries()
    for entry in weight_entries:
        date_str, weight = entry
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        days_since_start = (date_obj - datetime.datetime.combine(start_date, datetime.datetime.min.time())).days
        weight_dates.append(days_since_start)
        weights.append(weight)

    # Generate PDF report
    with PdfPages('dietmaster_report.pdf') as pdf:
        # Title and user information
        fig = plt.figure()
        plt.axis('off')
        user_info = f"DietMaster Report\n\nUser: {user.name}\nAge: {user.age}\nGender: {user.gender}\nHeight: {user.height_cm:.1f} cm\nStarting Weight: {user.weight_kg:.1f} kg\nGoal Weight: {user.goal_weight_kg:.1f} kg\nActivity Level: {user.activity_level}\n"
        plt.text(0.1, 0.5, user_info, fontsize=12)
        pdf.savefig(fig)
        plt.close()

        # Graph 1: Net calories and expected calories
        if dates:
            plt.figure()
            plt.plot(dates, net_calories, marker='o', label='Net Calories Burned')
            plt.plot(dates, expected_calories, marker='x', label='Expected Daily Calorie Change')
            plt.title('Net Calories Burned vs. Expected Calories Over Time')
            plt.xlabel('Days Since Start')
            plt.ylabel('Calories')
            plt.legend()
            plt.grid(True)
            pdf.savefig()
            plt.close()
        else:
            print("No calorie data available for Graph 1.")

        # Graph 2: Weight over time
        if weight_dates:
            plt.figure()
            plt.plot(weight_dates, weights, marker='o')
            plt.title('Weight Over Time')
            plt.xlabel('Days Since Start')
            plt.ylabel('Weight (kg)')
            plt.grid(True)
            pdf.savefig()
            plt.close()
        else:
            print("No weight data available for Graph 2.")

    print("Report exported to 'dietmaster_report.pdf'")