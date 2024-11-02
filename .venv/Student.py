#TO RUNNING IT SUCCESSFULLY, ADDITIONAL LIBRARIES IS REQUIRED (pandas and openpyxl)
#TO INSTALL ADDITIONAL LIBRARIES, INPUT THE FOLLOWING COMMANDS "pip install pandas" AND "pip install openpyxl" SEPARATELY IN THE TERMINAL
import pandas as pd
import random
from datetime import datetime

#Please modify this path to make sure that Excel file can be navigated correctly
path = "C:/Users/Hot945/Desktop/info.xlsx"

#Introduce Sequential Search function
def sequential_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

#Introduce a function to gen random number
def generate_num():
    return random.randint(1000000, 9999999)

#Introduce a function to transform Excel column data into Python list
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
    print(num) #This for testing number and will be deleted
    if num < 2:
        while True:
            rentalID = generate_num()
            list3 = get_column_list("lockers", "Rental ID")
            non_repeat_check = sequential_search(list3, rentalID)

            if non_repeat_check == -1:
                break

        startDate = datetime.now()
        df = pd.read_excel(path, sheet_name="lockers")
        valid_range = df["Locker ID"].notna().sum()

        found_locker = False

        for index, value in df["Status"].items():
            if index > valid_range:
                break

            if value not in ["Suspended", "Occupied"]:
                df.at[index, "Rental ID"] = rentalID
                df.at[index, "Student ID"] = studentID
                df.at[index, "Status"] = "Occupied"
                df["Start Date"] = df["Start Date"].astype(str)
                df.at[index, "Start Date"] = pd.to_datetime(startDate).strftime('%d-%b-%Y')
                df['Start Date'] = df['Start Date'].replace('nan', '')

                lockerID = df.at[index, "Locker ID"]
                location = df.at[index, "Location"]

                with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name="lockers", index=False)

                print("-" * 50, "\n")
                print("Locker allocated:", lockerID, " ", "Location:", location, "\n")
                print("Rental ID:", rentalID, "\n")
                print("Start date:", startDate.strftime("%d-%b-%Y"), "\n")
                print("$2 is charge to your account.")
                print("-" * 50)

                found_locker = True
                break

        if not found_locker:
            print("Sorry, all lockers are full")

    #When rented lockers = 2
    else:
        print("Sorry, you are already renting 2 lockers.")
        df = pd.read_excel(path, sheet_name="lockers")
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

# <Request move> Part
if option == "2":
    df = pd.read_excel(path, sheet_name="lockers")
    found_column = "Student ID"
    matching_column = "Rental ID"

    studentID = int(input("Enter Student ID: "))
    found_row = df[df[found_column] == studentID]

    #Judging whether Student ID is in the list
    if found_row.empty:
        print("You haven't rented any lockers.")
    else:
        rentalID = int(input("Enter Locker ID: "))
        matching_row = found_row[found_row[matching_column] == rentalID]

        #Judging whether Rental ID is in the list
        if matching_row.empty:
            print("Sorry,", rentalID, "is not your locker.")
        else:
            target = df[df["Rental ID"] == rentalID]
            for index, row in target.iterrows():
                lockerID = row["Locker ID"]
                location = row["Location"]
                startDate = row["Start Date"]

                print("-" * 50, "\n")
                print("Locker allocated:", lockerID, " ", "Location:", location, "\n")
                print("Rental ID:", rentalID, "\n")
                print("Start date:", startDate, "\n")
                print("-" * 50)

                df = pd.read_excel(path, sheet_name="stations")

                #Judging the input station availability
                while True:
                    stationCode = input("Enter Station code to move to: ")
                    stationInfo = df[df["Station Code"] == stationCode]
                    if stationInfo.empty:
                        print("Invalid station code, please re-enter.")
                        continue
                    if stationInfo["Status"].iloc[0] == 'Closed':
                        print("This station is unavailable, please use other station.")
                        continue
                    else:
                        break

                #Get row and col range
                max_rows = stationInfo["Rows"].iloc[0]
                max_columns = stationInfo["Columns"].iloc[0]

                #Create a list which contains all probability of station position
                available_position = []
                for rows in range(1, max_rows + 1):
                    for cols in range(1, max_columns + 1):
                        position = "%d,%d" % (rows, cols)
                        available_position.append(position)

                station_df = pd.read_excel(path, sheet_name=stationCode)

                #Enquire the existing stored locker list
                position_column = "Position"
                occupied_position = []
                if not station_df.empty and position_column in station_df.columns:
                    occupied_position = station_df[position_column].dropna().tolist()

                #Find the first available position
                empty_position = None
                for position in available_position:
                    if position not in occupied_position:
                        empty_position = position
                        break

                if empty_position is None:
                    print("This station is full. Please use other station.")
                    continue

                row_updated = False
                for index1, row1 in station_df.iterrows():
                    if pd.isna(row1[position_column]) and pd.isna(row1["Rental ID"]):
                        station_df.at[index1, "Rental ID"] = rentalID
                        station_df.at[index1, "Position"] = empty_position
                        row_updated = True
                        break

                #If empty row is not found, add a new row
                if not row_updated:
                    new_row = pd.DataFrame({"Rental ID": [rentalID],"Position": [empty_position]})
                    station_df = pd.concat([station_df, new_row], ignore_index=True)

                with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    station_df.to_excel(writer, sheet_name=stationCode, index=False)
                    print("written")

                print("Locker is moving to",stationCode,"(",empty_position,")")

                #Write to “lockers” sheet
                df = pd.read_excel(path, sheet_name="lockers")
                search_row = df["Rental ID"] == rentalID
                df.loc[search_row, "Location"] = stationCode
                df["Position"] = df["Position"].astype('object')
                df.loc[search_row, "Position"] = empty_position

                with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name="lockers", index=False)

                print("-" * 50, "\n")
                print("Locker allocated:", lockerID, " ", "Location:", "In transit", "\n")
                print("Rental ID:", rentalID, "\n")
                print("Start date:", startDate, "\n")
                print("-" * 50)

# <Return locker> Part
if option == "3":