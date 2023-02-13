
# Assumption 1 - make sure to run Sql server before executing the code to prevent DB not found errors.
# Assumption 2 - Student table created with primary key Student_id
# Assumption 3 - Attendance table created with a composite key consist with Student_id and Date
# Assumption 4 - Each time the code will run it will check for already created DB and load existing data from it

import mysql.connector
from mysql.connector import Error

print("*"*10, "Wellcome to Class Student Management System", "*"*10, """\n
\tPress 1 to Enter student data and attendance data
\tPress 2 to Update student details
\tPress 3 to Delete student details
\tPress 4 to Show tables data (View all or Selected)
\tPress 5 to quite
""")

# Keep number of records in Student table under 5
count=0

# Connecting to DB
try:
    connection = mysql.connector.connect(host='localhost', database='Class_Details', user='root', password='')
    cursor = connection.cursor()
except Error as e:
    connection = mysql.connector.connect(host="localhost", user="root", password="")
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE Class_Details")

print("You're connected to database Class_Details :)")

try:
    cursor.execute("CREATE TABLE Student (Student_id INT(30) PRIMARY KEY, first_name VARCHAR(225), last_name VARCHAR(225), Address VARCHAR(225), Tel VARCHAR(225))")
except Error as e:
    print("Table student already created :)")

try:
    cursor.execute("CREATE TABLE Attendance (Student_id INT(30), Date VARCHAR(225), attendance VARCHAR(30), PRIMARY KEY (Student_id, Date))")
except Error as e:
    print("Table attendance already created :)")

# To assign already created rows in Student table
cursor.execute("SELECT COUNT(*) FROM Student;")
result = cursor.fetchone()[0]
count=result
print("Student Table contain ", result, " Rows .....")


# fun 1 (Enter data for student table)
def input_data(s_count):
    print(f"Student {s_count} details ....")
    while True:
        try:
            s_id = int(input("Enter student id : "))
        except ValueError:
            print("Enter a integer")
            continue
        fn = input("Enter student first name : ")
        ln = input("Enter student last name : ")
        ad = input("Enter student address : ")
        tel = input("Enter student Tel : ")
        cursor.execute(f"INSERT INTO Student (Student_id,first_name,last_name,Address,Tel)VALUES('{s_id}','{fn}','{ln}','{ad}','{tel}')")
        # print("\n....Set up attendance....\n")
        print("Data entered successfully")
        break

# fun 2 (Enter data for attendance table)
def input_attendance(s_count, s_id):
    print(f"Student {s_count} attendance ....")
    while True:
        date = input("Enter date : ")
        attendance = input(f"Is student {s_id} present [Y/N] : ")
        attendance=attendance.lower()
        if(attendance=='y') | (attendance=='n'):
            cursor.execute(f"INSERT INTO Attendance (Student_id,Date,attendance)VALUES('{s_id}','{date}','{attendance}')")
            break
        else:
            print("attendance type you entered is not valid")

# fun 3 (Check the Previous student id when updating)
def previous_student_id():
    while True:
        try:
            id = int(input("Enter student id : "))
            return id
        except ValueError:
            print("Enter a integer")
            continue

while True:
    choice = input("Select operation : ")
    if choice == "1":
# Control fun 1 and fun 2 to insert data to the tables
        count=count+1
        if count<=5:
            input_data(count)
            connection.commit()
        else:
            print("Max Student count reached (5)!")
    elif choice == "2.5":
        s_id = previous_student_id()
        input_attendance(count, s_id)
    elif choice == "2":
# Below code for updating a record
        print("What do you want to update ^_^")
        print("""
        0 - Student ID
        1 - First name
        2 - Last name
        3 - Address
        4 - Tel
        """)
        ch = input(">>>")
        if ch == "0":
            print("New ID:")
            st_id = previous_student_id()
            print("Old ID:")
            z = previous_student_id()
            cursor.execute(f"UPDATE Student SET Student_id = {st_id} WHERE Student_id = {z}")
            cursor.execute(f"UPDATE Attendance SET Student_id = {st_id} WHERE Student_id = {z}")
        elif ch == "1":
            fn = input("Enter student new first name : ")
            z = previous_student_id()
            cursor.execute(f"UPDATE Student SET first_name = '{fn}' WHERE Student_id = {z}")
        elif ch == "2":
            ln = input("Enter student new last name : ")
            z = previous_student_id()
            cursor.execute(f"UPDATE Student SET last_name = '{ln}' WHERE Student_id = {z}")
        elif ch == "3":
            ad = input("Enter student new address : ")
            z = previous_student_id()
            cursor.execute(f"UPDATE Student SET Address = '{ad}' WHERE Student_id = {z}")
        elif ch == "4":
            tel = input("Enter student new telephone No  : ")
            z = previous_student_id()
            cursor.execute(f"UPDATE Student SET Tel = '{tel}' WHERE Student_id = {z}")
        else:
            print("Not a valid input")
            continue
        connection.commit()
    elif choice == "3":
# Deleting data from Student table
        print("ID of the student you want to delete from the table")
        st_id = previous_student_id()
        cursor.execute(f"DELETE FROM Student WHERE Student_id = {st_id}")
        cursor.execute(f"DELETE FROM Attendance WHERE Student_id = {st_id}")
        connection.commit()
    elif choice == "4":
# Display Data
        print("""
        Press 1 - See all the Tables with all the data
        Press 2 - Specific data
        """)
        cc = input(">>>>")
        if cc == "1":
            # Display the content of student table
            print("... Table Student ... \n")
            cursor.execute("SELECT * FROM Student")
            result = cursor.fetchall()
            for x in result:
                print(x)
            # Display the content of Attendance table
            print("... Table Attendance ... \n")
            cursor.execute("SELECT * FROM Attendance")
            result = cursor.fetchall()
            for x in result:
                print(x)
        elif cc == "2":
            print("Enter the student id you want fetch data from")
            st_id = previous_student_id()
            cursor.execute(f"SELECT Date, attendance FROM Attendance WHERE Student_id = {st_id}")
            result=cursor.fetchall()
            for x in result:
                print(x)
        else:
            print("Invalid input")
            continue
    elif choice == "5":
# Program termination
        cursor.close()
        print("<-> Program terminated <->")
        break
    else:
        print("Invalid operation try again !")


# reference - https://pynative.com/python-mysql-database-connection/
# reference - https://www.w3schools.com/python/python_mysql_getstarted.asp