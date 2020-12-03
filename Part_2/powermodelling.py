#
# powermodelling.py - Reads appliance information from a csv file and displays useful information from this.
#
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Opens the chosen CSV file and stores each line from it in the data variable
fileobj = open('ApplianceReadings/25 Swanson Way.csv', 'r')
data = fileobj.readlines()
fileobj.close()

# Create empty lists to store information from the csv file.
ApplianceNames = []
PowerRatings = []
HourlyUsages = []
DailyUsage = []
HourlyCalcUsage = []
TotalHourlyUsage = []

# Iterates through each line in the CSV file and appends the data to its respective list
# 2 used as start value to ignore the comments and resident count on the top of the csv file
for line in data[2::]:
    splitline = line.split(':')
    ApplianceNames.append(splitline[0])
    PowerRatings.append(float(splitline[1]))
    HourlyUsages.append(splitline[2].strip().split(','))

# Converts values in HourlyUsage list to float values for calculations (https://stackoverflow.com/questions/44884976/how-to-convert-2d-string-list-to-2d-int-list-python)
HourlyUsagesFloat = [list( map(float,i) ) for i in HourlyUsages]

# Calculates the daily power usage of each appliance
for i in range(len(PowerRatings)):
    DailyUsage.append(PowerRatings[i] * sum(HourlyUsagesFloat[i][0:24]))

# Calculates the hourly usage of each appliance by multiplying the powerrating for each appliance with each hourly usage that belongs to itand add it to the HourlyCalcUsage list
for i in range(len(PowerRatings)):
        for j in range(len(HourlyUsagesFloat[i])):
                HourlyCalcUsage.append(PowerRatings[i] * HourlyUsagesFloat[i][j])

HourlyCalcUsageArray = np.array(HourlyCalcUsage).reshape(int(len(PowerRatings)), 24)

# List of each hour in the day to be used as X values in plot
HoursInDay = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

# Adds the calculated values to the TotalHourlyUsage array for plotting the expected total hourly usage.
for i in range(len(HourlyUsagesFloat[0])):
        TotalHourlyUsage.append(sum([j [i] for j in HourlyCalcUsageArray]))

choices = 'Enter selected option: \n\n- (1) Print appliances\n- (2) Print total daily usage\n- (3) Total daily usage of each appliance plot\n- (4) Hourly usage of each appliance plot\n- (5) Search appliance and plot hourly usage\n- (6) Total daily usage of each appliance plot\n- (X) Exit\n\n'

userinput = input(choices)

while userinput.upper() != 'X':

        if userinput == '1':
                # Prints out the names of all the appliances in the residence
                print('\nThe appliances in the residence:\n')
                for i in ApplianceNames:
                        print('\t', i)
                print('\n')
        
        elif userinput == '2':
                # Plots the overall power usage in the house based on the csv file
                print('\n\tExpected daily usage is: ', sum(DailyUsage), 'W', '(', (sum(DailyUsage)/1000), 'KW )\n')
        
        elif userinput == '3':
                # Plots the total daily usage of each appliance in the house
                plt.bar(ApplianceNames, DailyUsage)
                plt.xticks(rotation=90)
                plt.title('Daily Appliance Usage')
                plt.ylabel('Usage(W)')
                plt.grid()
                plt.tight_layout() # Prevents content to exceed window
                plt.show()
        
        elif userinput == '4':
                # Plots the hourly usage of each appliance in the house throughot the day (24 hours)
                plt.figure(figsize=(15,5))
                plt.title('Hourly Appliance Usage')
                plt.xlabel('Time')
                plt.ylabel('Usage(W)')
                plt.xlim(1, 24)
                plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1)) # Makes the x-axis to show every iteration of the ticker
                
                # Loops through all the items in the PowerRatings list, plots the hourly usage of each along with the matching appliance name in the legend.(https://stackoverflow.com/questions/35166633/how-do-i-multiply-each-element-in-a-list-by-a-number/35166717)
                for j in range(len(PowerRatings)):
                        plt.plot(HoursInDay, [i * PowerRatings[j] for i in HourlyUsagesFloat[j][0:24]], label = ApplianceNames[j])
                
                plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5)) # Places the plot legend next to the plot instead of inside it to make the data more readable (https://queirozf.com/entries/matplotlib-examples-displaying-and-configuring-legends)
                plt.tight_layout() # Formats the plot to not hit the edges
                plt.grid()
                plt.show()

        elif userinput == '5':
                # Search for an appliance in the list and plots it.
                # User enters item to search for in the list
                searchinput = input('\nEnter item name... ')

                # If the entered item is an appliance in the list, the name of the appliance along with the items power rating is printed. It also plots the daily usage of the selected appliance. (https://www.geeksforgeeks.org/python-ways-to-check-if-element-exists-in-list/)
                if searchinput in ApplianceNames:
                        print('\n\t' + ApplianceNames[ApplianceNames.index(searchinput)] + ' has a power rating of ', PowerRatings[ApplianceNames.index(searchinput)], 'W\n', sep='')
                        plt.figure(figsize=(15,5))
                        plt.xlim(1, 24)
                        plt.title('Hourly Appliance Usage')
                        plt.xlabel('Time')
                        plt.ylabel('Usage(W)')
                        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
                        plt.plot(HoursInDay, [i * PowerRatings[ApplianceNames.index(searchinput)] for i in HourlyUsagesFloat[ApplianceNames.index(searchinput)][0:24]], label = ApplianceNames[ApplianceNames.index(searchinput)])
                        plt.grid()
                        plt.legend(loc="upper right")
                        plt.show()

                else:
                        print('\n\t' + searchinput, 'is not found in list\n')

        elif userinput == '6':
                # Plots the expected total hourly usage throughot the day based on the power ratings and the 
                plt.figure(figsize=(15,5))
                plt.plot(HoursInDay, TotalHourlyUsage, '-o')
                plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
                plt.xticks()
                plt.xlim(1, 24)
                plt.title('Expected hourly usage per day')
                plt.ylabel('Usage(W)')
                plt.xlabel('Time')
                plt.grid()
                plt.show()

        else:
                print('Invalid option, try again')

        userinput = input(choices)

print('\nPROGRAM ENDED\n')

# References:
# 
# https://thispointer.com/python-read-csv-into-a-list-of-lists-or-tuples-or-dictionaries-import-csv-to-list/
# https://stackoverflow.com/questions/35166633/how-do-i-multiply-each-element-in-a-list-by-a-number/35166717
# https://queirozf.com/entries/matplotlib-examples-displaying-and-configuring-legends 