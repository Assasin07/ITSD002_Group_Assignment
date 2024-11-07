from datetime import datetime
import random
import os

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
        with open('stations.txt', 'r') as file:
            for line in file:
                if line.strip():
                    station_data = line.strip().split(':')
                    stations_data.append({
                        'Station Code': station_data[0],
                        'Station Name': station_data[1],
                        'Rows': int(station_data[2]),
                        'Columns': int(station_data[3]),
                        'Status': station_data[4]
                    })
    except FileNotFoundError:
        return []
    return stations_data

#Load station log from txt file
def load_station_logs(station_code):
    station_logs = []
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_dir, 'stationlog', '%s.txt' % station_code)

        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    station_log_data = line.strip().split(':')
                    station_logs.append({
                        'Rental ID': int(station_log_data[0]) if station_log_data[0] else '',
                        'Position': station_log_data[1] if len(station_log_data) > 1 else ''
                    })
    except FileNotFoundError:
        return []
    return station_logs

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

#Save station log to txt file
def save_station_logs(station_code, station_logs):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'stationlog', '%s.txt' % station_code)

    with open(filename, 'w') as file:
        for station_log in station_logs:
            line = "%s:%s\n" % (
                station_log['Rental ID'],
                station_log['Position']
            )
            file.write(line)

#Introduce a function to gen random number
def generate_num():
    return random.randint(1000000, 9999999)



while True:
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
                if not any(rentalID == locker['Rental ID'] for locker in lockers):
                    break

            startDate = datetime.now()
            found_locker = False

            for locker in lockers:
                if locker['Status'] not in ['Suspended', 'Occupied']:
                    locker['Rental ID'] = rentalID
                    locker['Student ID'] = studentID
                    locker['Status'] = 'Occupied'
                    locker['Start Date'] = startDate.strftime('%d-%b-%Y')

                    #Create a new log txt and write info
                    log_filename = os.path.join('usagelog', str(rentalID) + '.txt')
                    current_time = datetime.now().strftime('%H:%M')
                    log_content = startDate.strftime('%d-%b-%Y') + ';' + current_time + ';Locker rental;' + str(studentID) + ';2.00' + '\n'

                    with open(log_filename, 'w') as log_file:
                        log_file.write(log_content)

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



    elif option == '2':
        #Load locker data
        lockers = load_lockers()

        while True:
            studentID = int(input('Enter Student ID: '))
            student_lockers = [locker for locker in lockers if locker['Student ID'] == studentID]

            if not student_lockers:
                print("You haven't rented any lockers.")
                continue

            rentalID = int(input('Enter Rental ID: '))
            matching_lockers = [locker for locker in student_lockers if locker['Rental ID'] == rentalID]

            if not matching_lockers:
                print('Sorry,', rentalID, 'is not your locker.')
                break

            #Get the info of rented locker
            target_locker = matching_lockers[0]
            lockerID = target_locker['Locker ID']
            location = target_locker['Location']
            startDate = target_locker['Start Date']

            print('-' * 50, '\n')
            print('Locker allocated:', target_locker['Locker ID'], ' Location:', target_locker['Location'], '\n')
            print('Rental ID:', rentalID, '\n')
            print('Start date:', target_locker['Start Date'], '\n')
            print('-' * 50)

            #Load station data
            stations = load_stations()

            current_station = target_locker['Location']

            #Choose station
            while True:
                stationCode = input('Enter Station code to move to: ')
                if stationCode == current_station:
                    print('You cannot move your locker to the same station!')
                    continue

                stationInfo = [station for station in stations if station['Station Code'] == stationCode]

                if not stationInfo:
                    print('Invalid station code, please re-enter.')
                    continue
                if stationInfo[0]['Status'] == 'Closed':
                    print('This station is unavailable, please use other station.')
                    continue

                #Read the max row/column data of station
                stationInfo = stationInfo[0]
                max_rows = stationInfo['Rows']
                max_columns = stationInfo['Columns']

                #Gen all possible position
                available_positions = []
                for rows in range(1, max_rows + 1):
                    for cols in range(1, max_columns + 1):
                        position = "%d,%d" % (rows, cols)
                        available_positions.append(position)

                #Load specific data
                station_logs = load_station_logs(stationCode)
                occupied_positions = [station_log['Position'] for station_log in station_logs if station_log['Position']]

                #Find the first available position
                empty_position = None
                for position in available_positions:
                    if position not in occupied_positions:
                        empty_position = position
                        break

                if empty_position is None:
                    print("This station is full. Please use other station.")

                #Exclude situation when locker is at Central store
                if current_station != 'Central store':

                    old_station_logs = load_station_logs(current_station)

                    #Remove old record
                    new_station_logs = [log for log in old_station_logs if log['Rental ID'] != rentalID]
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    filename = os.path.join(current_dir, 'stationlog', '%s.txt' % current_station)

                    with open(filename, 'w') as file:
                        for log in new_station_logs:
                            file.write(str(log['Rental ID']) + ':' + log['Position'] + '\n')

                #Update data to station log
                station_logs.append({
                    'Rental ID': rentalID,
                    'Position': empty_position
                })
                save_station_logs(stationCode, station_logs)

                print('Locker is moving to',stationCode,'(',empty_position,')')

                #Update data to lockers
                for locker in lockers:
                    if locker['Rental ID'] == rentalID:
                        locker['Location'] = stationCode
                        locker['Position'] = empty_position
                        break

                save_lockers(lockers)

                #Write info to existing log
                current_dir = os.path.dirname(os.path.abspath(__file__))
                rental_log_path = os.path.join(current_dir, 'usagelog', str(rentalID) + '.txt')

                current_time = datetime.now().strftime('%H:%M')
                content = datetime.now().strftime('%d-%b-%Y') + ';' + current_time + ';' + stationCode + ';' + str(studentID) + ';0.20' + '\n'

                with open(rental_log_path, 'a') as file:
                    file.write(content)

                print('-' * 50, '\n')
                print("Locker allocated: ", lockerID, " Location: ", "In transit", "\n")
                print("Rental ID: ", rentalID, "\n")
                print("Start date: ", startDate, "\n")
                print('-' * 50)
                break
            break



    elif option == '3':
            def validate_locker_id_linear(locker_id):
                with open('lockers.txt', 'r') as file:
                    for line in file.readlines():
                        data = line.strip().split(':')
                        if locker_id == data[0]:
                            return True
                    return False


            def validate_student_id_linear(student_id):
                with open('students.txt', 'r') as file:
                    for line in file.readlines():
                        data = line.strip().split(':')
                        if student_id == data[0]:
                            return True
                    return False


            def get_locker_data(locker_id):
                with open('lockers.txt', 'r') as file:
                    for line in file.readlines():
                        data = line.strip().split(':')
                        if locker_id == data[0]:
                            return data
                return None


            def update_locker_file(locker_data):
                updated_lines = []
                with open('lockers.txt', 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        data = line.strip().split(':')
                        if data[0] == locker_data[0]:
                            #Update locker status to available, clear rental ID, student ID and start date
                            locker_data[2] = "Available"
                            locker_data[3] = ""
                            locker_data[4] = ""
                            locker_data[5] = ""
                            updated_lines.append(':'.join(locker_data) + '\n')
                        else:
                            updated_lines.append(line)
                with open('lockers.txt', 'w') as file:
                    file.writelines(updated_lines)


            def update_locker_location(locker_id, new_location):
                print(f"Updating locker {locker_id} location to {new_location}")


            # Get the student ID entered by the user
            while True:
                user_student_id = input("Please enter student ID:")
                if not user_student_id.isdigit() or len(user_student_id) != 8:
                    print("Please enter the correct student ID format")
                else:
                    if validate_student_id_linear(user_student_id):
                        print("The student ID is valid.")
                        break
                    else:
                        print("Invalid student id, please re-enter.")

            # Get the locker ID entered by the user
            while True:
                user_locker_id = input("Please enter locker ID:")
                if not user_locker_id.isdigit() or len(user_locker_id) != 5:
                    print("Please enter the correct locker ID format")
                else:
                    if validate_locker_id_linear(user_locker_id):
                        print('-' * 50)
                        break
                    else:
                        print("Invalid locker id, please re-enter.")

            # Verify that the student ID and locker ID are valid (using the user input ID obtained above).
            if not validate_student_id_linear(user_student_id):
                print("Invalid student ID.")
                exit(1)
            if not validate_locker_id_linear(user_locker_id):
                print("Invalid locker ID.")
                exit(1)
            locker_data = get_locker_data(user_locker_id)
            if locker_data is None:
                print("Locker not found.")
                exit(1)

            # Check if the student ID and locker ID match
            if locker_data[4] and int(locker_data[4]) != int(user_student_id):
                print("This locker is rented by someone else.")
                exit(1)

            state = locker_data[2]
            if state == "Available" or state == "Suspended":
                print("This locker is available.")
                exit(0)
            else:
                print(f"Locker allocated: {user_locker_id}")
                print(f"Location: {locker_data[1]}")
                print(f"Rental ID: {locker_data[3]}")
                print(f"Start date: {locker_data[5]}")

            confirmation = input("Confirm to return the locker? (yes/no): ")
            if confirmation.lower() == "yes":
                # Get the current date as the end date
                end_date = datetime.now().strftime("%d-%b-%Y;%H:%M")

                # Calculate mobile charges and number of moves
                move_charges = 0
                move_count = 0
                rental_log_path = os.path.join('usagelog', str(locker_data[3]) + '.txt')
                with open(rental_log_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines[1:]:  # 从第二行开始计算移动费用，因为第一行是租赁记录
                        if line.strip():
                            data = line.strip().split(';')
                            if len(data) >= 5 and data[4]:
                                move_charges += float(data[4])
                                move_count += 1
                print(f"Move charges: ${move_charges:.2f} ({move_count} moves)")

                # Calculate the total cost
                total_charges = 2 + move_charges
                print(f"Rental charge: $2.00")
                print(f"Total charges for this rental: ${total_charges:.2f}")
                print('-' * 50)

                current_station = locker_data[1]

                if current_station != "Central store":
                    station_log_path = os.path.join('stationlog', f'{current_station}.txt')
                    updated_station_logs = []
                    with open(station_log_path, 'r') as file:
                        for line in file.readlines():
                            if line.strip() and line.split(':')[0] != locker_data[3]:
                                updated_station_logs.append(line)
                    with open(station_log_path, 'w') as file:
                        file.writelines(updated_station_logs)

                # Update locker status to available, clear rental ID, student ID, and start date
                locker_data[2] = "Available"
                locker_data[3] = ""
                locker_data[4] = ""
                locker_data[5] = ""
                locker_data[1] = "Central store"

                # If the current location is at the site, move the lockers back to the central warehouse
                if locker_data[1] != "Central store":
                    print(f"Moving locker back to Central store.")
                    update_locker_location(user_locker_id, "Central store")

                # Update locker information in lockers.txt file
                update_locker_file(locker_data)

                current_station = locker_data[1]


                # Write the end date to the txt file named after the Rental ID, with a separate line
                with open(rental_log_path, 'a') as file:
                    file.write(f"{end_date};Locker return")

                print("End date:", end_date)
                print("Locker returned successfully.")
                print('-' * 50)


    elif option == '4':
        students = load_students()

        while True:
            studentID = int(input('Enter Student ID: '))
            student_found = False
            for num in students:
                if num['Student ID'] == studentID:
                    student_found = True
                    for row in "lockers":
                        if row[0] in "lockers":
                            print("-" * 50, "\n")
                            print("Locker allocated:", lockerID, " ", "Location:", location, "\n")
                            print("Rental ID:", rentalID, "\n")
                            print("Start date:", startDate, "\n")
                            print("-" * 50)

                        else:
                            print("No rental records ")


                if not student_found:
                    print('Invalid student ID, please re-enter.')
    elif option == '0':
        break
