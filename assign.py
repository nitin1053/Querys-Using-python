import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Read the CSV file into a DataFrame
file_path = '/home/nitin1053/Documents/projects/aasiment3/Assignment_Timecard.xlsx - Sheet1.csv'
df = pd.read_csv(file_path, quotechar='"')

# Function to check consecutive days worked
def consecutive_days(employee_schedule):
    # Check if the date is not NaN
    if not pd.isna(employee_schedule['Pay Cycle Start Date']):
        # Convert dates to datetime objects
        start_date = datetime.strptime(employee_schedule['Pay Cycle Start Date'], '%m/%d/%Y')
        end_date = datetime.strptime(employee_schedule['Pay Cycle End Date'], '%m/%d/%Y')

        # Calculate the number of days between start and end date
        days_worked = (end_date - start_date).days + 1

        return days_worked >= 7
    else:
        return False

# Function to check hours between shifts
def hours_between_shifts(employee_schedule):
    # Check if the time values are not NaN
    if not pd.isna(employee_schedule['Time']) and not pd.isna(employee_schedule['Time Out']):
        # Convert time strings to datetime objects
        time_out = datetime.strptime(employee_schedule['Time Out'], '%m/%d/%Y %I:%M %p')
        next_time_in = datetime.strptime(employee_schedule['Time'], '%m/%d/%Y %I:%M %p') + timedelta(hours=1)

        # Calculate the time difference
        time_difference = next_time_in - time_out

        return 1 < time_difference.total_seconds() / 3600 < 10
    else:
        return False

# Function to check hours in a single shift
def hours_in_single_shift(employee_schedule):
    # Check if the time values are not NaN
    if not pd.isna(employee_schedule['Time']) and not pd.isna(employee_schedule['Time Out']):
        # Convert time strings to datetime objects
        time_in = datetime.strptime(employee_schedule['Time'], '%m/%d/%Y %I:%M %p')
        time_out = datetime.strptime(employee_schedule['Time Out'], '%m/%d/%Y %I:%M %p')

        # Calculate the time difference
        shift_duration = time_out - time_in

        return shift_duration.total_seconds() / 3600 > 14
    else:
        return False

results = []

# Loop through the DataFrame and apply the functions
for index, row in df.iterrows():
    if consecutive_days(row):
        result = f"{row['Employee Name']} worked for 7 consecutive days at position {row['Position ID']}"
        results.append(result)

    if hours_between_shifts(row):
        result = f"{row['Employee Name']} has less than 10 hours between shifts but greater than 1 hour at position {row['Position ID']}"
        results.append(result)

    if hours_in_single_shift(row):
        result = f"{row['Employee Name']} worked for more than 14 hours in a single shift at position {row['Position ID']}"
        results.append(result)

# Save the results to output.txt
output_path = '/home/nitin1053/Documents/projects/aasiment3/output.txt'
with open(output_path, 'w') as file:
    for result in results:
        file.write(result + '\n')