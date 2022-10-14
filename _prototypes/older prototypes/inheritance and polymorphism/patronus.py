# FUNDAMENTALS OF OBJECT ORIENTED PROGRAMMING: 
# https://www.youtube.com/watch?v=e4fwY9ZsxPw&t=3599s

# LEARNING PYTHON DEFAULT PARAMETERS: https://www.pythontutorial.net/python-basics/python-default-parameters/
# ABOUT DEFUALT ARGUMENTS ERROR: https://bobbyhadz.com/blog/python-syntaxerror-non-default-argument-follows-default-argument#:~:text=The%20Python%20%22SyntaxError%3A%20non%2D,positional%20parameters%20of%20the%20function.

# this Student "class" is kinda like the "soul" of the Student object
class Student: # you can make parameters opational by attaching "None" to a parameter, as in house=None
    def __init__(self, name, house=None, patronus='Unknown'): # this allows to pass in parameters into the "declaration object"
        # Exception Handling codes below
        if name == "":
           raise ValueError("Missing Name")
        
        if house not in ["Gryff","Slyth", "Huff","Raven"]: # "not in" allows for an array of values
           raise ValueError("Invalid House")
        
        # REMEMBER: parameters in the __init__ MUST be IN ORDER! or else it would get jumbled when you use it!!
        # the setters does not have to follow the order in which the parameters are declared
        # also, positional arguments (self, name) should be declared AFTER the default arguments (house, and spell)
        self.name = name # see methodtae "get_student"
        self.house = house # we passed "name" and "house" parameters to the Student class
        self.patronus = patronus # just added aa 4rth parameter. nothing special

    # special python method in printing objects on the console
    def __str__(self): # this prevents this error: object at 0x000002CD04FEBEE0
        return f"Behold! {self.name} from {self.house} has the patronus {self.patronus}! Let it be known!!"

    def charm(self): # "self" is a positional argument that is required for methods that are declared INSIDE a class
        # this "self" argument is allowing access to a method owned by the Student class if in case you are trying to call this function OUTSIDE of the Student class
        # below is the syntax of python for a "switch statement" (if you do java)    
        match self.patronus: 
            case "Stag":
                return "🦌"
            case "Otter":
                return "🦦"
            case "Jack Russel Terrier":
                return "🐕"
            case _: # this is returned if the user did not input anything for the "Patronus:"
                return "💫"

def greet(name, message='Hi'): # we can call this method just by declaring it in our main method and providing the parameters that it is asking for
    return f"{message}, {name}!"


def get_student():
    name = input("\n\nName: ") # passing this inputs from the user as an arguments
    
    house = input("House: ")
    patronus = input("Patronus: ")
    student = Student(name, house, patronus) # declaration of the object. or the "body" for my "soul".
    
    return student # see main method where the "get_student" object is declared

def main():
    student = get_student() # this object declaration takes the return statement from the "get_student" method

    print("\n\nExpecto Patronum!", student.charm()) # calling the charm method of the "Student" class
    print(student,"\n") # print will trigger the __str__ method located inside the Student class, because the "print" method is looking for a "string" input
    # notice that inside the "get_student" method the Student class is referenced and given variables (name, house, patronus) and then returned student

    greeting = greet(student.name)
    print(greeting, "<3 \n")


if __name__ == "__main__":
    main()
    