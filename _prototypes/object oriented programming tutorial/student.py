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