#
# house.py - Contains the class for building houses for the neighbourhood simulation
#
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from datetime import datetime

# List containing all the hours in a day for plotting 
HoursInDay = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
totalstreetusage = []

class House():

    def __init__(self, owner, street, number): 
        self.owner = owner
        self.street = street
        self.number = number
        self.appliancefile = str(number)+' '+str(street)
        self.appliances = [] 
        self.powerratings = [] 
        self.hourlyusage = []
        self.hourlyusagefloat = []
        self.hourlycalcusage = []
        self.totalhourlyusage = []
    
    # Adds all the appliances to the house object 
    def addAppliances(self):
        
        # add errorhandling here in case of wrong filename
        fileobj = open(str('ApplianceReadings/'+self.appliancefile)+'.csv', 'r')
        data = fileobj.readlines()
        fileobj.close()

        # Iterates through each line in the CSV file and appends the data to its respective list
        # 2 used as start value to ignore the comments and resident count on the top of the csv file
        for line in data[2::]:
            splitline = line.split(':')
            self.appliances.append(splitline[0])
            self.powerratings.append(float(splitline[1]))
            self.hourlyusage.append(splitline[2].strip().split(','))
            self.hourlyusagefloat = [list( map(float,i) ) for i in self.hourlyusage] # Converts values in HourlyUsage list to float values for calculations (https://stackoverflow.com/questions/44884976/how-to-convert-2d-string-list-to-2d-int-list-python)

        for i in range(len(self.powerratings)):
            for j in range(len(self.hourlyusagefloat[i])):
                self.hourlycalcusage.append(self.powerratings[i] * self.hourlyusagefloat[i][j])
            
        hourlycalcusagearray = np.array(self.hourlycalcusage).reshape(int(len(self.powerratings)), 24)
            
        for i in range(len(self.hourlyusagefloat[0])):
            self.totalhourlyusage.append(sum([j [i] for j in hourlycalcusagearray]))

    # Prints out essential information of the house object 
    def printHouse(self):
        print('\n')
        print('Owner: ', self.owner, '\n')
        print('Street: ', self.street, '\n')
        print('Streetnumber: ', self.number, '\n')
        print('Appliances: ', self.appliances, '\n')
        print('\n')

    # Plots the hourly usage of each appliance and total usage in the house throughot the day (24 hours)
    def plotResidenceUsage(self):
        plt.figure(figsize=(15,6))
        
        plt.subplot(211)
        plt.title('Hourly Appliance Usage')
        plt.xlabel('Time')
        plt.ylabel('Usage(W)')
        plt.xlim(1, 24)
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1)) # Makes the x-axis to show every iteration of the ticker
            
        # Loops through all the items in the PowerRatings list, plots the hourly usage of each along with the matching appliance name in the legend.
        for j in range(len(self.powerratings)):
            plt.plot(HoursInDay, [i * self.powerratings[j] for i in self.hourlyusagefloat[j][0:24]], label = self.appliances[j])
            
        plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5)) # Places the plot legend next to the plot instead of inside it to make the data more readable
        plt.tight_layout() # Formats the plot to not hit the edges
        plt.grid()
        
        plt.subplot(212)
        plt.plot(HoursInDay, self.totalhourlyusage, '-', label = str(self.number) + ' ' + self.street)
        plt.xlim(1, 24)
        plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.xticks()
        plt.title('Total Hourly Usage Per Day')
        plt.ylabel('Usage(W)')
        plt.xlabel('Time')
        plt.tight_layout() # Formats the plot to not hit the edges
        plt.grid()    
        
        plt.show()

    def findMaxMinUsage(self):

        # https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
        dateTimeObj = datetime.now()
        dateTimeObjStr = dateTimeObj.strftime("%d-%b-%Y(%H:%M:%S)")
 
        # Opens a txt file for writing which has the name of dateTimeObjStr
        maxminoutputfile = open('OutputFiles/' + dateTimeObjStr + ".txt", "a")

        hourlycalcusagearray = np.array(self.hourlycalcusage).reshape(int(len(self.powerratings)), 24)
        
        # https://numpy.org/doc/stable/reference/generated/numpy.sum.html
        idmax = np.argmax(np.sum(hourlycalcusagearray, axis = 1))
        idmin = np.argmin(np.sum(hourlycalcusagearray, axis = 1))
        sumtest = np.sum(hourlycalcusagearray,  axis = 1)

        # https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file-in-python-3
        print('\n Residence: ' + str(self.number), self.street, '\n',  file=maxminoutputfile)
        print('\tHighest daily usage:', self.appliances[idmax],'(' + str(sumtest[idmax]) + ' W)', '\n', file=maxminoutputfile)
        print('\tLowest daily usage:', self.appliances[idmin],'(' + str(sumtest[idmin]) + ' W)', '\n', file=maxminoutputfile)
    
        maxminoutputfile.close()