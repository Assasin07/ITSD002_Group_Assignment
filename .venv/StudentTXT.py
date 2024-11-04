from datetime import datetime
import random

#Load student data from txt file
def load_students():
    students_data = []
    try:
        with open('students.txt', 'r') as file:
            for line in file:
                if line.strip():
                    student_data = line.strip().split(':')
                    students_data.append({
                        'Student ID': int(student_data[0]),
                        'Student Name': student_data[1],
                        'Account': student_data[2]
                    })
    except FileNotFoundError:
        return []
    return students_data

#Load locker data from txt file
def load_lockers():
    lockers_data = []
    try:
        with open('lockers.txt', 'r') as file:
            for line in file:
                if line.strip():
                    locker_data = line.strip().split(':')
                    lockers_data.append({
                        'Locker ID': locker_data[0],
                        'Location': locker_data[1],
                        'Status': locker_data[2],
                        'Rental ID': int(locker_data[3]) if len(locker_data) > 3 and locker_data[3] else '',
                        'Student ID': int(locker_data[4]) if len(locker_data) > 4 and locker_data[4] else '',
                        'Start Date': locker_data[5] if len(locker_data) > 5 else ''
                    })
    except FileNotFoundError:
        return []
    return lockers_data

#Load station data from txt file
def load_stations():
    stations_data = []
    try:
        with open('station.txt', 'r') as file:
            for line in file:
                if line.strip():
                    station_data = line.strip().split(':')
                    stations_data.append({
                        'Station Code': int(station_data[0]),
                        'Station Name': station_data[1],
                        'Rows': int(station_data[2]),
                        'Columns': int(station_data[3]),
                        'Status': station_data[4]
                    })
    except FileNotFoundError:
        return []
    return stations_data

#Save locker data to txt file
def save_lockers(lockers):
    with open('lockers.txt', 'w') as file:
        for locker in lockers:
            line = "%s:%s:%s:%s:%s:%s\n" % (
                locker['Locker ID'],
                locker['Location'],
                locker['Status'],
                locker['Rental ID'],
                locker['Student ID'],
                locker['Start Date']
            )
            file.write(line)

#Introduce a function to gen random number
def generate_num():
    return random.randint(1000000, 9999999)



#Display STUDENT MENU
print('++++ Go Locker – Operations ++++\n1. Rent a lock\n2. Request move\n3. Return locker\n4. Enquire locker location\n5. View usage report\n0. Exit')

option = input('Enter option: ')

if option == '1':
    #Load student data
    students = load_students()

    while True:
        studentID = int(input('Enter Student ID: '))
        student_found = False
        for num in students:
            if num['Student ID'] == studentID:
                student_found = True
                break

        if not student_found:
            print('Invalid student ID, please re-enter.')
        else:
            break

    #Load locker data
    lockers = load_lockers()

    #Detect student's current rentals
    student_rentals = sum(1 for locker in lockers if locker['Student ID'] == studentID)

    if student_rentals < 2:
        #Generate unique rental ID
        while True:
            rentalID = generate_num()
            if not any(str(rentalID) == locker['Rental ID'] for locker in lockers):
                break

        startDate = datetime.now()
        found_locker = False

        for locker in lockers:
            if locker['Status'] not in ['Suspended', 'Occupied']:
                locker['Rental ID'] = str(rentalID)
                locker['Student ID'] = studentID
                locker['Status'] = 'Occupied'
                locker['Start Date'] = startDate.strftime('%d-%b-%Y')

                print('-' * 50, '\n')
                print('Locker allocated:', locker['Locker ID'], ' Location:', locker['Location'], '\n')
                print('Rental ID:', rentalID, '\n')
                print('Start date:', startDate.strftime('%d-%b-%Y'), '\n')
                print('$2 is charged to your account.', '\n')
                print('-' * 50)

                found_locker = True
                break

        if found_locker:
            save_lockers(lockers)
        else:
            print('Sorry, all lockers are full')

    else:
        print('Sorry, you are already renting 2 lockers.')
        rented_lockers = [locker for locker in lockers if locker['Student ID'] == studentID]
        for locker in rented_lockers:
            print('-' * 50, '\n')
            print('Locker allocated:', locker['Locker ID'], ' Location:', locker['Location'], '\n')
            print('Rental ID:', locker['Rental ID'], '\n')
            print('Start date:', locker['Start Date'], '\n')
            print('-' * 50)