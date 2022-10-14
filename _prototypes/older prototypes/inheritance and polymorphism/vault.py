# SOURCE: https://www.youtube.com/watch?v=e4fwY9ZsxPw&list=PLPG6wUjL9QmTKKoO5lrI-l0Tt2bCMRgS2&index=14
# OPERATOR OVERLOADING: https://www.programiz.com/python-programming/operator-overloading

class Name:
    def __init__(self, name): 
        self.name = name

class Vault(Name):
    def __init__(self,name, galleons=0,sickles=0,knuts=0):
        super().__init__(name)
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def inventory(self):
        print (f"{self.name} Galleons: {self.galleons}, Sickles: {self.sickles}, Knuts: {self.knuts}")
    
    def __str__(self):
        return f"{self.name} Galleons: {self.galleons}, Sickles: {self.sickles}, Knuts: {self.knuts}"

    # OPERATOR OVERLOADING
    def __add__(self, other):
        galleons = self.galleons + other.galleons
        sickles = self.sickles + other.sickles
        knuts = self.knuts + other.knuts
        return Vault("", galleons, sickles, knuts)

potter = Vault("Potter: ",100,20,50)
potter.inventory()

weasly = Vault("Weasly: ",20,50,6)
print(weasly)

# galleons = potter.galleons + weasly.galleons
# sickles = potter.sickles + weasly.sickles
# knuts = potter.knuts + weasly.knuts

# total = galleons + sickles + knuts

total = potter + weasly
print("Total: ", total)