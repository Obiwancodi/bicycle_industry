


class Bicycle(object):
     def __init__(self, name, weight, cost,price):
        self.name = name
        self.weight = weight
        self.cost = cost
        self.price = price
              
class Shop(object):
    def __init__(self, sname, margin, inventory):
        self.sname = sname
        self.margin = margin
        self.inventory = inventory 
        
        
    def add(self,Bicycle):
        self.inventory.append(Bicycle)
        
                   
    def set(self,Bicycle):
        Bicycle.price = Bicycle.cost + Bicycle.cost * self.margin/100
        print Bicycle.price
        
    
    def money(self,Bicycle):
        profit = Bicycle.price - Bicycle.cost
        self.inventory.remove(Bicycle)
        print profit
        
    
    
class Customer(object):
    def __init__(self, name, fund, own):
        self.name = name
        self.fund = fund
        self.own = own
        
    def buy(self,Bicycle):
        if self.fund > Bicycle.price:
            self.own.append(Bicycle)
            self.fund = self.fund - Bicycle.price
            print self.name + " " + Bicycle.name + " " + str(Bicycle.price) + " " + str(self.fund)
            
        
 



