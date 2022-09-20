# CLASSES POLYMORPHISM: https://www.programiz.com/python-programming/polymorphism
# PYTHON INHERITANCE: https://www.programiz.com/python-programming/inheritance

# What is Polymorphism?
# -- The literal meaning of polymorphism is the condition of occurrence in different forms.
# -- Polymorphism is a very important concept in programming. 
# -- It refers to the use of a single type entity (method, operator or object) to represent 
# -- different types in different scenarios.

# What is Inheritance?
# -- Inheritance enables us to define a class that takes all the functionality 
# -- from a parent class and allows us to add more. 


# INHERITANCE
class About:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

class Cat(About): # inherits the functionality of the parent class About
    def __init__(self, name, age):
        super().__init__(name, age) # super refers to the parent. we are calling the parent's __init__ function

    def info(self):
        print(f"I am a cat. My name is {self.name}. I am {self.age} years old.")

    def make_sound(self):
        print("Meow")


class Dog(About): # inherits the functionality of the parent class About
    def __init__(self, name, age):
        super().__init__(name, age) # super refers to the parent. we are calling the parent's __init__ function

    def info(self):
        print(f"I am a dog. My name is {self.name}. I am {self.age} years old.")

    def make_sound(self):
        print("Bark")


cat1 = Cat("Kitty", 2.5)
dog1 = Dog("Fluffy", 4)

for animal in (cat1, dog1):
    animal.info()
    animal.make_sound()