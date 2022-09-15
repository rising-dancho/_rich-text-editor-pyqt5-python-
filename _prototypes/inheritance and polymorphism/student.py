# FUNDAMENTALS OF OBJECT ORIENTED PROGRAMMING: 
# https://www.youtube.com/watch?v=e4fwY9ZsxPw&t=3599s

class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house
        
def main():
    first, last, house = get_student()
    print(f"{first}, {last} from {house}")

def get_student():
    first = input("First Name: ")
    last = input("Last Name: ")
    house = input("House: ")
    return first, last, house

if __name__ == "__main__":
    main()