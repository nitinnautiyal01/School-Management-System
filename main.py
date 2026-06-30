# SCHOOL MANAGEMENT SYSTEM

import json
from pathlib import Path
from abc import abstractmethod,ABC

database = "school_data.json"

data = {"Students" : [], "Faculty" : []}

if Path(database).exists():
    with open(database,'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)

class School(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class Student(School):
    def get_roles(self):
        return "student"
    
    def register(self):
        name = input("Enter Student Name : ")
        age = int(input("Enter Student Age : "))
        email = input("Enter Student Email : ")
        roll_no = input("Enter Student Roll Number : ")
        
        if not School.validate_email(email):
            print("Please Enter Valid Email")
            return 
        
        for i in data['Students']:
            if i['roll_no'] == roll_no:
                print("Roll No. already exist!")
                return

        data['Students'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "roll_no" : roll_no,
            "grades" : {}
        })
        save()

    def show_details(self):
        roll_no = input("Enter Student Roll Number : ")
        for s in data['Students']:
            if s['roll_no'] == roll_no:
                grades = s['grades']
                avg = sum(grades.values()) / len(grades) if grades else 0

                print(f"\n Name  : {s['name']}")
                print(f" Roll no : {s['roll_no']}")
                print(f" Grades : {grades}")
                print(f" Average : {avg:.1f}%")
                return

    def grades(self):
        roll_no = input("Enter Roll Number : ")
        subject = input("Enter Subject Name  : ")
        marks = float(input("Enter Student Marks : "))

        for i in data['Students']:
            if i['roll_no'] == roll_no:
                 i['grades'][subject] = marks
                 save()
                 print("Marks Added Sucessfully")
                 return
        print("Student not found")

class Faculty(School):
    def get_roles(self):
        return "faculty"
    
    def register(self):
        name = input("Enter Faculty Name : ")
        age = int(input("Enter Faculty Age : "))
        email = input("Enter Faculty Email : ")
        id = input("Enter Faculty ID : ")
        sub = input("Enter Faculty Subject : ")
        
        if not School.validate_email(email):
            print("Please Enter Valid Email")
            return 
        
        for i in data['Faculty']:
            if i['ID'] == id:
                print("ID already exist!")
                return

        data['Faculty'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "ID" : id,
            "Subject" : sub
        })
        save()

    def show_details(self):
        id = input("Enter Faculty ID : ")
        for f in data['Faculty']:
            if f['ID'] == id:
                print(f"\n Name : {f['name']}")
                print(f" ID : {f['ID']}")
                print(f" Subject : {f['Subject']}")
                print(f" Age : {f['age']}")
                print(f" Email : {f['email']}")
                return
            
        print("Teacher Not Found")
  
            

stu = Student()
fac = Faculty()

print("Registered Student, press 1")
print("Registered Faculty, press 2")
print("Add Grade to the student, press 3")
print("Check Student details, press 4")
print("Check Faculty details, press 5")

choice = int(input("What do you want to do? : "))

if choice == 1:
    stu.register()

elif choice == 2:
    fac.register()

elif choice == 3:
    stu.grades()

elif choice == 4:
    stu.show_details()

elif choice == 5:
    fac.show_details()


