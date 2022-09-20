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
        return f"Galleons: {self.galleons}, Sickles: {self.sickles}, Knuts: {self.knuts}"

potter = Vault("Potter",100,20,50)
potter.inventory()

weasly = Vault(20,50,6)
print("Weasly: ", weasly)