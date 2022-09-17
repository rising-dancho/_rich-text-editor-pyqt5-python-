# FUNDAMENTALS OF OBJECT ORIENTED PROGRAMMING: 
# https://www.youtube.com/watch?v=e4fwY9ZsxPw&t=3599s

# ABOUT DEFUALT ARGUMENTS: https://bobbyhadz.com/blog/python-syntaxerror-non-default-argument-follows-default-argument#:~:text=The%20Python%20%22SyntaxError%3A%20non%2D,positional%20parameters%20of%20the%20function.


# this Student "class" is kinda like the "soul" of the Student object
class Student: # you can make parameters opational by attaching "None" to a parameter, as in house=None
    def __init__(self, name, house=None, spell=None): # this allows to pass in parameters into the "declaration object"
        # Exception Handling codes below
        if name == "":
           raise ValueError("Missing Name")
        
        if house not in ["gryff","slyth", "huff","raven"]: # "not in" allows for an array of values
           raise ValueError("Invalid House")
        
        # REMEMBER: parameters in the __init__ MUST be IN ORDER! or else it would get jumbled when you use it!!
        # the setters does not have to follow the order in which the parameters are declared
        # also, positional arguments (self, name) should be declared AFTER the default arguments (house, and spell)
        self.name = name # see methodtae "get_student"
        self.house = house # we passed "name" and "house" parameters to the Student class
        self.spell = spell # just added aa 4rth parameter. nothing special

    # special python method in printing objects on the console
    def __str__(self): # this prevents this error: object at 0x000002CD04FEBEE0
        return f"Behold! {self.name} from {self.house} can use the spell {self.spell}! Let it be known!!"

def get_student():
    name = input("Name: ") # passing this inputs from the user as an arguments
    house = input("House: ")
    spell = input("Spell: ")
    student = Student(name, house, spell) # declaration of the object. or the "body" for my "soul".
    
    return student # see main method where the "get_student" object is declared

def main():
    student = get_student() # this object declaration takes the return statement from the "get_student" method
    # print(f"{student.name} from {student.house}")
    
    print(student) # print triggers the __str__ method, because it's looking for a string


if __name__ == "__main__":
    main()