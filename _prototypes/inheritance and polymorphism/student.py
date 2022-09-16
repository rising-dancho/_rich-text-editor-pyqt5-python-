# FUNDAMENTALS OF OBJECT ORIENTED PROGRAMMING: 
# https://www.youtube.com/watch?v=e4fwY9ZsxPw&t=3599s


# this Student "class" is kinda like the "soul" of the Student object
class Student: # you can make parameters opational by attaching "None" as in house=None
    def __init__(self, name, house=None): # this allows to pass in parameters into the declaration object
        # Exception Handling codes below
        if name == "":
           raise ValueError("Missing Name")
        
        if house not in ["Gryff","Slyth", "Huff","Raven"]: # not in allows for an array of values
           raise ValueError("Invalid House")
        
        self.name = name # see method "get_student"
        self.house = house # we passed "name" and "house" parameters to the Student class

    # special python method in printing objects on the console
    def __str__(self): # this prevents this error: object at 0x000002CD04FEBEE0
        return f"{self.name} from {self.house}"

def get_student():
    name = input("Name: ") # passing this inputs from the user as an arguments
    house = input("House: ")
    student = Student(name, house) # declaration of the object. or the "body" for my "soul".
    
    return student # see main method where the "get_student" object is declared

def main():
    student = get_student() # this object declaration takes the return statement from the "get_student" method
    # print(f"{student.name} from {student.house}")
    
    print(student)


if __name__ == "__main__":
    main()