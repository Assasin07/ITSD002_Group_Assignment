#TO RUNNING IT SUCCESSFULLY, YOU NEED ADDITIONAL LIBRARIES(pandas and openpyxl)
#TO INSTALL THESE, INPUT THE FOLLOWING COMMAND "pip install pandas" AND "pip install openpyxl" SEPERATELY IN YOUR TERMINAL
from operator import truediv

import pandas as pd

#Introduce Sequential Search function
def sequential_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

#Display STUDENT MENU
print("++++ Go Locker – Operations ++++\n1. Rent a lock\n2. Request move\n3. Return locker\n4. Enquire locker location\n5. View usage report\n0. Exit")

option = input("Enter option: ")

# <Rent a lock> Part
if option == "1":
    df = pd.read_excel("C:/Users/Hot945/Desktop/info.xlsx", sheet_name="students")
    column_name = "Student ID"
    list1 = df[column_name].tolist()

    while True:
        studentID = int(input("Enter Student ID: "))
        verification = sequential_search(list1, studentID)

        if verification != -1:
            break
        else:
            print("Invalid student ID, please re-enter.")

    #Judging the number of lockers student had rented
    df = pd.read_excel("C:/Users/Hot945/Desktop/info.xlsx", sheet_name="lockers")
    column_name = "Student ID"
    list2 = df[column_name].tolist()

    num = 0
    for i in range(len(list2)):
        if sequential_search(list2, studentID) != -1:
            num += 1
    #When rented lockers < 2
    if num < 2:
        print("testing")

    #When rented lockers = 2
    else:
        print("Sorry, you are already renting 2 lockers.")
        df = pd.read_excel("C:/Users/Hot945/Desktop/info.xlsx", sheet_name="lockers", )
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
            print("Start date:", startDate.strftime("%d-%b-%y"), "\n")
            print("-" * 50)





