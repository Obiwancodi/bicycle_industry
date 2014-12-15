from bicycle_industry import Bicycle
from bicycle_industry import Shop
from bicycle_industry import Customer

import random

m_one = Bicycle("Luke", 50 , 350, [])
m_two = Bicycle("Leia", 45 , 360, [])
m_three = Bicycle("Vader", 65 , 900, [])
m_four = Bicycle("Han", 60 , 775, [])
m_five = Bicycle("Chewy", 90 , 210, [])
m_six = Bicycle("Jar", 30, 1, [])

c_one = Customer("Frodo", 400, [])
c_two = Customer("Sam", 500, [])
c_three = Customer("Gandaulf", 1000, [])

people = [c_one, c_two, c_three]

pittsburgh = Shop("rei", 20, [])

pittsburgh.add(m_one)
pittsburgh.add(m_two)
pittsburgh.add(m_three)
pittsburgh.add(m_four)
pittsburgh.add(m_five)
pittsburgh.add(m_six)


pittsburgh.set(m_one)
pittsburgh.set(m_two)
pittsburgh.set(m_three)
pittsburgh.set(m_four)
pittsburgh.set(m_five)
pittsburgh.set(m_six)


def yes():
    for person in people:
        print person.name
        for inv in pittsburgh.inventory:
            if person.fund > inv.price:
                print person.name + " can afford " + inv.name
            else:
                pass
def sure():
    for inv in pittsburgh.inventory:
        print inv.name
        
        
def what():
    for person in people:
        while person.own == []:
            person.buy(random.choice(pittsburgh.inventory))
        pittsburgh.money(person.own[0])
    for inv in pittsburgh.inventory:
        print inv.name
    
            


            
if __name__ == '__main__':
    yes()
    sure()
    what()
   


