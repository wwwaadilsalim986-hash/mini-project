import sqlite3
from sqlite3 import IntegrityError
from winreg import error

DB='student_grading.db'

def get_connection():
    conn= sqlite3.connect(DB)
    return conn

def get_connection():
    conn= sqlite3.connect(DB)
    return conn

def student_grade_system():
    conn = get_connection()
    c = conn.cursor()
    conn.execute('PRAGMA foreign_keys=ON')

    c.execute('''CREATE TABLE IF NOT EXISTS students_info(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no INTEGER UNIQUE NOT NULL
    );
  ''')
    conn.commit()

    c.execute('''CREATE TABLE IF NOT EXISTS marks(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       student_id INTEGER UNIQUE,
       major INTEGER,
       minor1 INTEGER,
       minor2 INTEGER,
       mdc INTEGER,
       language INTEGER,
       second_language INTEGER,
       FOREIGN KEY (student_id) REFERENCES students_info(id) ON DELETE CASCADE
       )
  ''')
    conn.commit()

def add_student():
    student_name = input('Enter student name :').strip()
    roll_no_raw = input('Enter student roll.no :').strip()

    if not student_name or not roll_no_raw:
        print('Name and roll_no are required.')
        return

    try:
        roll_no=int(roll_no_raw)
    except ValueError:
        print('Roll number must be an integer.')
        return

    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""INSERT INTO students_info(name,roll_no)
        VALUES(?,?)""", (student_name, roll_no))
        conn.commit()
        print('\n',student_name,'Added to the list')

    except sqlite3.IntegrityError:
        print('roll_no already exists')

def list_students():
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute("""SELECT id,name,roll_no FROM students_info ORDER BY roll_no""").fetchall()

    if not rows:
        print('Student not found.Add Student first !')
        return

    print('\n                 Student list              \n')
    for student in rows:
        student_id = student[0]
        student_name = student[1]
        roll_no = student[2]
        print(student_id,'|' ,'Name=',student_name,"|",'Roll no=',roll_no)
    print()

def get_student_by_roll(user='Enter roll.no of student'):
    roll_no_raw=input(user).strip()
    try:
        roll_no=int(roll_no_raw)
    except ValueError:
        print('Roll number must be an integer.')
        return

    conn = get_connection()
    c = conn.cursor()
    row=c.execute('SELECT id,name FROM students_info WHERE roll_no=?', (roll_no,)).fetchone()
    conn.commit()
    if not row:
        print('Student not found !')
    return row

def validate_marks(name,value):
    if value is None:
        raise ValueError(f"Marks for {name} is required.")
    if value < 0 :
        raise ValueError(f"Marks for {name} cannot be negative.")
    if value > 100 :
        raise ValueError(f"Marks for {name} cannot be greater than 100.")

def add_marks():
    student = get_student_by_roll()
    print('\n                                    Add marks                                    \n')
    if not student:
        print('Student not found.Add Student first ! \n')
        return

    try:
        major = int(input('Enter marks of major subject : '))
        minor1 = int(input('Enter marks of minor1 subject : '))
        minor2 = int(input('Enter marks of minor2 subject : '))
        mdc = int(input('Enter marks of mdc subject : '))
        language = int(input('Enter marks of language subject : '))
        second_language = int(input('Enter marks of second language subject : '))

    except ValueError:
        print('Marks Should be Integer')
        return

    try:
        validate_marks('major',major)
        validate_marks('minor1',minor1)
        validate_marks('minor2',minor2)
        validate_marks('mdc',mdc)
        validate_marks('language',language)
        validate_marks('second_language',second_language)
    except ValueError as e:
        print('Invalid marks.',e)
        return
    student_id,student_name=student

    try:
      conn=get_connection()
      c = conn.cursor()

      cur = conn.cursor()
      if cur.execute("SELECT id FROM students_info WHERE id = ?", (student_id,)).fetchone() is None:
          conn.close()
          return

      c.execute('''INSERT INTO marks(student_id,major,minor1,minor2,mdc,language,second_language)
      VALUES(?,?,?,?,?,?,?)
      ''', (student_id,major,minor1,minor2,mdc,language,second_language))
      conn.commit()
      print('Marks added for',student_name,'\n')

    except IntegrityError:
        print('marks already added')

def edit_marks():
    roll_no=int(input('Enter roll no of student:'))
    conn = get_connection()
    c = conn.cursor()

    student=c.execute('SELECT id,name FROM students_info WHERE roll_no=?', (roll_no,)).fetchone()

    if not(student):
        print('Student not found.Add Student first ! \n')
        conn.close()
        return
    student_id=student[0]
    student_name=student[1]
    try:
        major=int(input('Enter new marks of major subject : '))
        minor1=int(input('Enter new marks of minor1 subject : '))
        minor2=int(input('Enter new marks of minor2 subject : '))
        mdc=int(input('Enter new marks of mdc subject : '))
        language=int(input('Enter new marks of language subject : '))
        second_language=int(input('Enter new marks of second language subject : '))

    except ValueError:
        print('Marks Should be Integer')
        return

    try:
        validate_marks('major',major)
        validate_marks('minor1',minor1)
        validate_marks('minor2',minor2)
        validate_marks('mdc',mdc)
        validate_marks('language',language)
        validate_marks('second_language',second_language)
    except ValueError as e:
        print('Invalid marks.',e)
        return

    c.execute('UPDATE marks SET major=?, minor1=?,minor2=?,mdc=?,language=?,second_language=? WHERE student_id=?', (major,minor1,minor2,mdc,language,second_language,student_id))
    print('\n Marks Updated for ',student_name)
    conn.commit()

def delete_student():
     roll_no=int(input('Enter roll no of student to delete:'))
     conn = get_connection()
     c=conn.cursor()
     student=c.execute('SELECT roll_no FROM students_info WHERE roll_no=?', (roll_no,))

     student_name=c.execute('SELECT name FROM students_info WHERE roll_no=?', (roll_no,)).fetchone()

     if not student:
         print('Student not found.')
         return

     delete_student=c.execute('DELETE FROM students_info WHERE roll_no=?', (roll_no,))
     print(student_name, 'Deleted from list')

     conn.commit()

def main():
    student_grade_system()

    while True:
        print('\n                     STUDENT GRADE SYSTEM                           ')
        print('\nChoose one of the options below\n')
        print('1.Add Students')
        print('2.List Students')
        print('3.Add Marks for student')
        print('4.Edit Marks for student')
        print('5.Delete Student')
        print('0.Exit')

        try:
            choice = int(input('\n Enter your choice:'))
            if choice == 1:
               add_student()
            elif choice == 2:
               list_students()
            elif choice == 3:
               add_marks()
            elif choice == 4:
               edit_marks()
            elif choice == 5:
               delete_student()
            elif choice == 0:
               print('Thank You')
               break
            else:
               print('\n          Invalid Choice           ')
        except ValueError:
            print('\nInvalid Choice')



# main()










    










