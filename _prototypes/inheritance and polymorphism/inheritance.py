# PRINTING FROM SUPER: https://exchangetuts.com/typeerror-descriptor-init-requires-a-super-object-but-received-a-str-1640057224114963

class Employee:
    raise_amount=1.05
    emp_count=0
    def __init__(self,first_name,last_name, amount):
        self.first_name = first_name
        self.last_name  = last_name
        self.amount     = amount
        self.email_id="{0}.{1}@{1}.com" .format(first_name,last_name)
        Employee.emp_count +=1

    def fullname(self):
        print ("%s %s"%(self.first_name,self.last_name))

class Developer(Employee):
    raise_amount = 1.10
    def __init__(self,first,last,amount,programming):
        super().__init__(first,last,amount)
        self.programming= programming

dev1=Developer("John","Wick",500000,"Python")
dev2=Developer('John','Constantine',5688989,'java')
dev2.fullname()
dev1.fullname()

emp1=Employee("Dr Gregory","House",30000)
emp1.fullname()
