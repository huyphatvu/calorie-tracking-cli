# Development Guide

## Introduction

This document provides guidelines and instructions for developers contributing to the DietMaster application. It covers setting up the development environment, understanding the project structure, coding standards, and the branching strategy used in version control.

## Project Overview

DietMaster is a Python-based application designed to help users manage their dietary habits and fitness goals. The application allows users to:

* Create and update personal profiles.
* Log daily calorie intake and calories burned.
* Track weight changes over time.
* Generate PDF reports with user information and progress graphs.

The application uses SQLite for data storage and matplotlib for generating graphs.

## Development Environment Setup

### Prerequisites

* Python 3.6 or higher
* Git for version control
* pip for package management

### Setting Up the Environment

1.	Clone the Repository

git clone https://github.com/yourusername/dietmaster.git


2.	Navigate to the Project Directory

cd dietmaster


3.	Create a Virtual Environment (Optional but Recommended)
```
python -m venv venv
```

4.	Activate the Virtual Environment
* On Windows:
```
venv\Scripts\activate
```

* On Unix or Linux:
```
source venv/bin/activate
```

5.	Install manually:
```
pip install matplotlib
```

6.	Set Up the Database
* The database (dietmaster.db) is created automatically when you run the application for the first time.

### Project Structure
```
dietmaster/
├── dietmaster.py
├── user.py
├── activity.py
├── nutrition.py
├── data_storage.py
├── report.py
├── utils.py
├── README.md
├── development.md
├── requirements.txt
└── dietmaster.db
```
* dietmaster.py: Main entry point of the application.
* user.py: Manages user profiles and calculations.
* activity.py: Handles logging of activities and calories burned.
* nutrition.py: Manages logging of daily calorie intake.
* data_storage.py: Handles data persistence using SQLite.
* report.py: Generates PDF reports with user data and graphs.
* utils.py: Contains utility functions for input validation and unit conversion.
* requirements.txt: Lists all Python packages required by the application.
* dietmaster.db: SQLite database file (auto-generated).
* README.md: Instructions on how to set up and run the application.
* development.md: This development guide.

## Coding Standards

### General Guidelines

* Write clear, readable, and maintainable code.
* Follow the PEP 8 style guide for Python code.
* Use meaningful variable and function names.
* Include comments and docstrings where appropriate.

### File Headers

At the beginning of each Python file, include a comment block with:

* The filename.
* Author(s).
* A brief description of the file’s purpose.

Example:
```
# filename.py
# Author: DietMaster Development Team
# Description: Brief description of the file.
```

### Function and Class Documentation

* Use docstrings to document the purpose, parameters, and return values of functions and classes.
* Example:
```
def calculate_bmi(weight, height):
    """
    Calculates the Body Mass Index (BMI).

    Parameters:
        weight (float): Weight in kilograms.
        height (float): Height in meters.

    Returns:
        float: Calculated BMI.
    """
    return weight / (height ** 2)
```


### Branching Strategy

We use Git for version control and follow the Gitflow Workflow for branching.

Branch Types

1. Main Branch (main or master)
    * Contains the production-ready code.
    * Should always be stable.
    * Develop Branch (develop)
    * Integration branch for features.
    * Reflects the latest delivered development changes for the next release.
2. Feature Branches (feature/)
    * Used for developing new features.
    * Branches off from develop.
    * Merges back into develop.
    * Release Branches (release/)
    * Used for preparing a new production release.
    * Branches off from develop.
    * Merges into develop and main.
 
## Workflow

1.	Starting a New Feature
* Create a new feature branch from develop:
```
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

2.	Developing the Feature
* Commit changes to your feature branch regularly.
* Keep commits small and focused.
* Write descriptive commit messages.
3.	Completing a Feature
* Ensure your feature is complete and tested.
* Merge develop into your feature branch to resolve any conflicts:
```
git checkout feature/your-feature-name
git pull origin develop
git merge develop
```

* Push your feature branch to the repository:
```
git push origin feature/your-feature-name
```

* Create a Pull Request (PR) to merge your feature into develop.

4.	Code Review and Merging
* Another team member reviews the PR.
* After approval, merge the feature branch into develop.
* Delete the feature branch after merging.
5.	Preparing a Release
* Create a release branch from develop:
```
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0
```

* Perform final testing and bug fixes.
* Update version numbers and documentation as needed.
* Merge the release branch into main and tag the release:

```
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
```
* Merge back into develop:

git checkout develop
git merge release/v1.0.0


* Delete the release branch.

Branch Naming Conventions

* Feature Branches: feature/feature-name
* Release Branches: release/version-number
* Hotfix Branches: hotfix/description
 

### Testing

Running Tests

* Currently, the application may not have automated tests.
* Manual testing is crucial. Test your changes thoroughly.
* Future development should include writing unit tests using frameworks like unittest or pytest.