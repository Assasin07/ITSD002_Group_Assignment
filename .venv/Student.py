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
    list = df[column_name].tolist()

    while True:
        studentID = int(input("Enter Student ID: "))
        verification = sequential_search(list, studentID)

        if verification != -1:
            break
        else:
            print("Invaild student ID, please re-enter.")


