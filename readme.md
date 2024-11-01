# DietMaster Application

## Introduction

DietMaster is a comprehensive diet and fitness tracking application designed to help users manage their weight goals effectively. It allows users to:

* Log daily calorie intake and calories burned.

* Track weight changes over time.

* Generate detailed PDF reports with graphs and summaries.

* Estimate the days required to reach weight goals based on user input.

The application supports both metric and imperial units and provides personalized recommendations based on user profiles.

## Features

* User Profile Management: Create and update personal information, including goal weight and weekly weight change.

* Daily Logging: Log calories consumed, calories burned, and weight for specific dates.
	
* Progress Tracking: View summaries of daily activities and check estimated days to reach weight goals.

* PDF Reports: Generate comprehensive reports with user information, achievements, and graphs of metrics.

* Data Persistence: All data is stored locally using SQLite, ensuring data is saved between sessions.

*Units Support: Choose between metric and imperial units for measurements.

## Prerequisites

* Python 3.6 or higher is required to run the application.

* The following Python packages are needed:

```
pip install matplotlib
```

* SQLite is used for data storage (included with Python’s standard library).

## Installation

1.	Clone or Download the Repository
2.	Navigate to the Project Directory:
```
cd dietmaster
```

3.	Install Required Packages:
Install the required Python packages using pip:

```
pip install matplotlib
```

## Running the Application

1. Run the Main Script:
Execute the application by running the dietmaster.py script:
```
python dietmaster.py
```

Make sure you’re in the project directory when running this command.

## Usage

### Initial Setup

1. Create a User Profile:

    * The application will prompt you to enter your personal information, including name, age, gender, height, weight, and activity level.

    * Choose your preferred measurement system (metric or imperial).

    * Set your goal weight and the amount of weight you wish to lose or gain per week.

2. Data Persistence:
	* Your profile and logged data will be saved automatically.
	* The next time you run the application, it will load your existing profile.

#### Main Menu Options

After setting up, you’ll be presented with a menu:
```
1.	Log calories intake: Record the number of calories consumed for a specific date.
2.	Log calories burned: Record the number of calories burned through activities for a specific date.
3.	Log weight: Update your weight for a specific date.
4.	View today’s summary: Display a summary of today’s calorie intake, calories burned, and net calories.
5.	Generate PDF report: Create a PDF report with your information, achievements, and graphs.
6.	Check days to reach goal: Estimate the days remaining to reach your weight goal based on current data.
7.	Update personal information: Modify your goal weight or weekly weight change.
8.	Reset all data: Clear all stored data and start fresh.
9.	Exit: Close the application.
```
### Expected Input and Output

#### Input

* Text Inputs: Names, dates (in YYYY-MM-DD format), and choices from provided options.
* Numeric Inputs: Age, weight, height, calories, and weight changes.
* Numeric inputs are validated. If invalid input is detected, the application will prompt you to enter the value again.
* Date inputs are validated to ensure correct format.

#### Output

* Prompts and Instructions: Clear instructions guiding you through each step.
* Calculations and Summaries:
* BMI calculation.
* Recommended healthy weight range.
* Recommended daily caloric intake.
* Estimated days to reach your goal.
* PDF Report:
* A multi-page PDF including user information, achievements, and graphs.
* Graphs display net calories vs. expected calories and weight over time.

#### Sample Session

Below is an example of how a typical session with the application might look.

Starting the Application
```
$ python dietmaster.py
```
Sample Interaction
```
Welcome to DietMaster!
Choose your measurement system (metric/imperial): metric
Enter your name (e.g., John Doe): Alice Smith
Enter your age (e.g., 30): 28
Enter your gender (male/female): female
Enter your height in cm (e.g., 165 cm): 170
Enter your current weight in kg (e.g., 65 kg): 75
Activity levels: sedentary, lightly active, moderately active, very active, extra active
Enter your activity level (sedentary/lightly active/moderately active/very active/extra active): moderately active

Your current BMI is: 25.95
Based on your height, a healthy weight range is 53.5 kg to 72.0 kg.
Enter your desired goal weight in kg (e.g., 65 kg): 68
You need to lose weight to reach your goal.
Enter the amount of weight you want to lose per week (max 1.0 kg) (e.g., 0.5 kg): 0.5

Hello Alice Smith! Your recommended daily caloric intake is: 2178.57 calories.
Estimated days to reach your goal: 98 days (by 2024-02-07).

Please select an option:
1. Log calories intake
2. Log calories burned
3. Log weight
4. View today's summary
5. Generate PDF report
6. Check days to reach goal
7. Update personal information
8. Reset all data
9. Exit
Enter your choice (1/2/3/4/5/6/7/8/9): 1
Enter date (YYYY-MM-DD) or press Enter for today: 
Enter total calories intake (e.g., 2000): 2200
Logged 2200.0 calories intake on 2023-11-01.

Please select an option:
1. Log calories intake
2. Log calories burned
3. Log weight
...
```

#### Generating a PDF Report

* When you select option 5, the application generates a PDF report:

Generating PDF report...
Report exported to 'dietmaster_report.pdf'


* The report includes:
* Title: DietMaster Report
* Sections:
    1. User Information
    2. Achievements
    3. Metrics
        * Graphs:
        * Net Calories vs. Expected Calories Over Time
        * Weight Over Time

### Project Structure

* dietmaster.py: Main script and entry point of the application.
* user.py: Manages the user profile and related calculations.
* activity.py: Handles logging of calories burned.
* nutrition.py: Handles logging of daily calorie intake.
* data_storage.py: Manages data persistence using SQLite.
* report.py: Generates the PDF report with user data and graphs.
* utils.py: Contains utility functions for input validation and unit conversion.
* dietmaster.db: SQLite database file (created after first run).

## Authors

DietMaster Development Team

## Notes

* Data Storage: All data is stored locally in dietmaster.db. Ensure you have write permissions in the project directory.
* Dependencies: If you encounter issues with dependencies, ensure all required packages are installed and compatible with your Python version.
* Error Handling: The application includes input validation and will prompt you to correct invalid inputs.

## Troubleshooting

* Module Not Found Error: Ensure all Python files are in the same directory and you are running the script from that directory.
* Permission Errors: Check that you have the necessary permissions to read and write files in the project directory.
* Graph Display Issues: Ensure that matplotlib is properly installed. If you’re running the script on a server or environment without a display, you might need to configure matplotlib to use a non-interactive backend.
