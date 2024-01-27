import csv
import pytz
from datetime import datetime,  timedelta

values =[0]
data =[]
employees = []
prev_emp_name = None

valid_employees = []
prev_end_time = None

emp_with_14hr_timediff = []


def check_consecutive_days(data, consecutive_limit):
    num = data[0] - 1
    count = 0
    # checking for consecutive days in filtered data containing unique digits
    for i in data:
        if i - num == 1:
            count += 1
        else:
            count = 1  # Reset count if not consecutive
        num = i
        if count == consecutive_limit:
            return True
    return count == consecutive_limit


with open('Assignment_Timecard.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:

        # extracting employees data from csv file
        emp_name = str(row['Employee Name'])
        time_in_str = row['Time']
        time_out_str = row['Time Out']
        
        # Finding employee who has worked for 7 consecutive days.

        if time_in_str:
            # converting str date values to objects for comparision
            time_obj = datetime.strptime(time_in_str, "%m/%d/%Y %I:%M %p")

            # Appending days to list(values) for comparision
            if(time_obj.day >= values[-1]):
                values.append(time_obj.day)
                # print(time_in_str , " ", emp_name)

            else:
                # else block to seperate each indivisual employeee data
                # removing duplicate days and 0 digit from the values list
                for item in values:
                    if item not in data and item !=0:
                        data.append(item)
            
                data.sort()
                # print(data)

                # print("-------------------------")
                # print("prev emp = ", time_in_str, " ", prev_emp_name)
               
                if check_consecutive_days(data, 7):
                    employees.append(prev_emp_name)

                values = [0]
                data = []

        prev_emp_name = emp_name

    # --------------------------------------------------------------------

        # finding employees those have shift time diff btw 1 to 10

        if time_in_str and time_out_str:

            # converting str date values to objects for comparision
            start_time = datetime.strptime(time_in_str, "%m/%d/%Y %I:%M %p")
            end_time = datetime.strptime(time_out_str, "%m/%d/%Y %I:%M %p")

            # prev_end_time is present or skip 1st employee 1st row --> startime
            if prev_end_time is not None:
                if(start_time.day >= prev_end_time.day):

                    time_difference = start_time - prev_end_time
                    if 1 < time_difference.total_seconds() / 3600 < 10:
                        valid_employees.append(row['Employee Name'])
                        # print("time_diff :", time_difference, "start_time : ", start_time, "end_time : ", prev_end_time)
                        # print(f"Employee {row['Employee Name']} has a valid shift time difference.")
                else:
                    # time diff can not be calculated btw dates of diff employees
                    # print("-------not evaluated-------")
                    pass
            # getting employee end time for prev shift
            prev_end_time = end_time

    # ------------------------------------------------------------------------

        # Extracting single shift time differences 
        shift_time_diff = row['Timecard Hours (as Time)']
        # print(shift_time_diff)

        if(shift_time_diff):
            # converting time diff of single shift in object for comparision
            time_diff_obj = datetime.strptime(shift_time_diff, "%H:%M").time()

            # comparing time in minutes
            time_diff_mins = time_diff_obj.hour * 60 + time_diff_obj.minute
            target_time_diff_minutes = 14 * 60

            if time_diff_mins >= target_time_diff_minutes:
                emp_with_14hr_timediff.append(emp_name)
                # print("The shift time difference is greater than or equal to 14 hours.")
            else:
                pass
       

    print("\n7 days Consecutive Emp_names :- \n", employees)
    print("\nEmployees which have less than 10 hours of time between shifts but greater than 1 hour :-\n", set(valid_employees), "\n")
    print("Employees whose shift time difference more 14 hours : ", emp_with_14hr_timediff, "\n")

















