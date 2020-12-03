#
# powersimulation.py - Creates a street containing objects of the House class and gives useful information about the street
#
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from house import House

# Create an empty list to store all the house objects
street = []

# List containing all the hours in a day for plotting 
HoursInDay = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
streetusage = []

# Create house objects and append to street list
house = House('Valerie Maxville', 'Python Way', 1)
street.append(house)
house = House('Katrina Hooper', 'Python Way', 2)
street.append(house)
house = House('Ben Sinclair', 'Python Way', 3)
street.append(house)
house = House('Pablo Jose Zarate Chaupin', 'Python Way', 4)
street.append(house)
house = House('Anonymous Calc', 'Python Way', 5)
street.append(house)
house = House('Plato Khisa', 'Python Way', 6)
street.append(house)

# Adds all the appliances to the house objects in the list
for obj in street: 
    obj.addAppliances()

for obj in street: 
    streetusage.append(obj.totalhourlyusage)

# Sums all the matching indexes of the streetusage list 
totalhourlystreetusage = np.sum(streetusage, 0) 

choices = 'Enter selected option: \n\n- (1) Plot hourly usage of each house in street\n- (2) Plot appliance- and total usage for chosen house\n- (3) Print info about all houses in the street\n- (4) Plot daily hourly usage for the entire street\n- (5) Get total daily usage of street\n- (6) Get the most and least power consuming appliance in each residence\n- (7) Create new house\n- (X) Exit\n\n'

userinput = input(choices)

while userinput.upper() != 'X':
    
    if userinput == '1':
        plt.figure(figsize=(15,5))
        
        for obj in street:
            plt.plot(HoursInDay, obj.totalhourlyusage, '-', label = str(obj.number) + ' ' + obj.street)

        plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.xlim(1,24)
        plt.xticks()
        plt.title('Expected hourly usage per day')
        plt.ylabel('Usage(W)')
        plt.xlabel('Time')
        plt.tight_layout() # Formats the plot to not hit the edges
        plt.grid()  
        plt.show()

    elif userinput == '2':
    
        housenumber = int(input('Enter house number of residence to plot: '))

        street[housenumber-1].plotResidenceUsage()
        

    elif userinput == '3':
        for obj in street:
            obj.printHouse()

    elif userinput == '4':

        plt.figure(figsize=(15,5))
        plt.xlim(1, 24)
        plt.plot(HoursInDay, totalhourlystreetusage, '-o')
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.xticks()
        plt.title('Expected Hourly Street Usage Per Day')
        plt.ylabel('Usage(W)')
        plt.xlabel('Time')
        plt.tight_layout() # Formats the plot to not hit the edges
        plt.grid()    
        plt.show()

    elif userinput == '5':

        # https://kite.com/python/answers/how-to-print-a-float-with-two-decimal-places-in-python
        print('\nTotal daily usage of street in watt:', "{:.2f}".format(sum(totalhourlystreetusage)), 'W')
        print('\nTotal daily usage of street in kilowatts:', "{:.2f}".format(sum(totalhourlystreetusage)/1000), 'KW\n')
    
    elif userinput == '6':
        
        for obj in street:
            obj.findMaxMinUsage()
        
    elif userinput == '7':

        newhouseowner = input('Enter owners name: ')
        newhousestreet = input('Enter street name: ')
        newhousestreetnumber = int(input('Enter house number: '))

        house = House(newhouseowner, newhousestreet, newhousestreetnumber)
        street.append(house)

        house.addAppliances()

    else:
        print('Invalid option, try again')

    userinput = input(choices)

print('\nPROGRAM ENDED\n')