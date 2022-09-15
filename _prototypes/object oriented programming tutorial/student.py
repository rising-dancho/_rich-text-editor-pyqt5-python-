# FUNDAMENTALS OF OBJECT ORIENTED PROGRAMMING: 
# https://www.youtube.com/watch?v=e4fwY9ZsxPw&t=3599s

class Student: # soul
    def __init__(self, name, house): # this allows to pass in parameters into the declaration object
        self.name = name # see method "get_student"
        self.house = house # we passed "name" and "house" parameters to the Student class

def main():
    student = get_student() # this object declaration takes the return statement from the "get_student" method
    print(f"{student.name} from {student.house}")

def get_student():
    name = input("Name: ")
    house = input("House: ")
    # passing this inputs from user as an arguments
    student = Student(name, house) # declaration of the object. or the "body" for my "soul".

    return student # see main method where the "get_student" object is declared

if __name__ == "__main__":
    main()