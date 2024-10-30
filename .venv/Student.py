#TO RUNNING IT SUCCESSFULLY, YOU NEED ADDITIONAL LIBRARIES(pandas and openpyxl)
#TO INSTALL THESE, INPUT THE FOLLOWING COMMAND "pip install pandas" AND "pip install openpyxl" SEPERATELY IN YOUR TERMINAL
import pandas as pd
import random
from datetime import datetime

path = "C:/Users/Hot945/Desktop/info.xlsx"

#Introduce Sequential Search function
def sequential_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

#Introduce a function to gen random num
def generate_num():
    return random.randint(1000000, 9999999)

#Introduce a funtion to transform Excel column data into Python list
def get_column_list(sheet_name_input, column_name_input):
    df = pd.read_excel(path, sheet_name=sheet_name_input)
    return df[column_name_input].tolist()

#Display STUDENT MENU
print("++++ Go Locker – Operations ++++\n1. Rent a lock\n2. Request move\n3. Return locker\n4. Enquire locker location\n5. View usage report\n0. Exit")

option = input("Enter option: ")

# <Rent a lock> Part
if option == "1":
    list1 = get_column_list("students", "Student ID")

    while True:
        studentID = int(input("Enter Student ID: "))
        verification = sequential_search(list1, studentID)

        if verification != -1:
            break
        else:
            print("Invalid student ID, please re-enter.")

    #Judging the number of lockers student had rented
    list2 = get_column_list("lockers", "Student ID")
    num = list2.count(studentID)

    #When rented lockers < 2
    print(num)
    if num < 2:
        while True:
            rentalID = generate_num()
            list3 = get_column_list("lockers", "Rental ID")
            non_repeat_check = sequential_search(list3, rentalID)

            if non_repeat_check == -1:
                break

        startDate = datetime.now()
        df = pd.read_excel(path, sheet_name="lockers", )
        valid_range = df["Locker ID"].notna().sum()

        for index, value in df["Status"].items():
            if index > valid_range:
                break

            if value not in ["Suspended", "Used"]:
                df.at[index, "Rental ID"] = rentalID
                df.at[index, "Student ID"] = studentID
                df.at[index, "Status"] = "Used"
                df["Start Date"] = df["Start Date"].astype(str)
                df.at[index, "Start Date"] = pd.to_datetime(startDate).strftime('%d-%b-%y')
                df['Start Date'] = df['Start Date'].replace('nan', '')

                lockerID = df.at[index, "Locker ID"]
                location = df.at[index, "Location"]

                with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name="lockers", index=False)

                print("-" * 50, "\n")
                print("Locker allocated:", lockerID, " ", "Location:", location, "\n")
                print("Rental ID:", rentalID, "\n")
                print("Start date:", startDate.strftime("%d-%b-%y"), "\n")
                print("$2 is charge to your account.")
                print("-" * 50)
                break

    #When rented lockers = 2
    else:
        print("Sorry, you are already renting 2 lockers.")
        df = pd.read_excel(path, sheet_name="lockers", )
        target = df[df["Student ID"] == studentID]
        for index, row in target.iterrows():
            lockerID = row["Locker ID"]
            location = row["Location"]
            rentalID = row["Rental ID"]
            rentalID_int = int(rentalID)
            startDate = row["Start Date"]
            print("-" * 50, "\n")
            print("Locker allocated:", lockerID, " ", "Location:", location, "\n")
            print("Rental ID:", rentalID_int, "\n")
            print("Start date:", startDate, "\n")
            print("-" * 50)





