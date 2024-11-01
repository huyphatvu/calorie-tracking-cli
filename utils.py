# utils.py

def lbs_to_kg(pounds):
    return pounds * 0.453592

def inches_to_cm(inches):
    return inches * 2.54

def kg_to_lbs(kg):
    return kg / 0.453592

def cm_to_inches(cm):
    return cm / 2.54

def get_float_input(prompt, example=None, unit=None):
    while True:
        try:
            if example and unit:
                value = float(input(f"{prompt} (e.g., {example} {unit}): "))
            elif example:
                value = float(input(f"{prompt} (e.g., {example}): "))
            else:
                value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def get_int_input(prompt, example=None):
    while True:
        try:
            if example:
                value = int(input(f"{prompt} (e.g., {example}): "))
            else:
                value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def get_choice_input(prompt, choices):
    choices_str = '/'.join(choices)
    while True:
        value = input(f"{prompt} ({choices_str}): ").lower()
        if value in choices:
            return value
        else:
            print(f"Invalid choice. Please enter one of the following: {choices_str}")