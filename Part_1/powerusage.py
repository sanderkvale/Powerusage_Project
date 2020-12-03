#
# powerusage.py - Reads power readings from a csv file and displays useful information from this.
#
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.ticker as plticker
import numpy as np

# Reads in the csv file which contains the readings and times.
power_df = pd.read_csv("MeterReadings.csv")

# Converts the ReadingTime column to datetime values.
power_df['ReadingTime'] = pd.to_datetime(power_df['ReadingTime'])

# Action options
choices = 'Enter selected option: \n\n- (1) Table content\n- (2) Max & Min\n- (3) Average overall\n- (4) Daily average per hour plot\n- (5) Hourly bar plot\n- (6) Cumulative usage plot\n- (X) Exit\n\n'

# Prompts user to insert value of wanted action
userinput = input(choices)

while userinput.upper() != 'X':

    if userinput == '1':
        
        # Prints out the dataframe as a table.
        print('\n', power_df.to_string(index=False), '\n') # index=False is used to hide the index for better readability

    elif userinput == '2':
    
        # Creates variables for the max and min values of the increments in the dataframe
        maxreadings = power_df[power_df['Increment']==power_df['Increment'].max()]
        minreadings = power_df[power_df['Increment']==power_df['Increment'].min()]

        # Prints out the max and min increment values from the dataframe
        print('\nMax readings:\n\n', maxreadings.to_string(index=False), '\n') # index=False is used to hide the index for better readability
        print('\nMin reading:\n\n', minreadings.to_string(index=False), '\n') # index=False is used to hide the index for better readability

    elif userinput == '3':
        
        # Prints the average power usage per hour overall.
        print('Average usage per hour:\n\n',power_df['Increment'].mean(),'\n')
    
    elif userinput == '4':

        # Plots the average hourly usage per day in a bar plot
        plt.figure(figsize=(15,5))

        # Groups the increments on the day value
        power_df_grouped = power_df.groupby(power_df['ReadingTime'].dt.day)

        # Loops throug all the increment values that is in the group created above
        # and plots each one of them in their respective bars (https://stackoverflow.com/questions/27405483/how-to-loop-over-grouped-pandas-dataframe/27422749)
        for day, usage in power_df_grouped:
            plt.bar(day, usage.mean()['Increment'], label = str(day), width=0.2)
  
        plt.title('Average hourly usage per day')
        plt.ylabel('Usage (kwh)')
        plt.xlabel('Day (date)')
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1)) # Modifies the tick iteration on the x axis in the plot
        plt.gca().legend(title="Day (date)", loc='center left', bbox_to_anchor=(1, 0.5)) # Positioning legend next to the plot rather than within it
        plt.gca().set_ylim(None,power_df['Increment'].max()) # Sets the top of the y axis to be the maximum of the increments as the average (almost never) will be the same as max value
        plt.tight_layout() # Prevents content to exceed window
        plt.grid()
        plt.show()

    elif userinput == '5':
        
        # Pivots the dataframe to create a new one in a different format 
        pivottable2 = power_df.pivot_table(index=power_df['ReadingTime'].dt.hour, columns=[power_df['ReadingTime'].dt.day], values=['Increment'])

        print(pivottable2.to_string())

        # Plots the new dataframe in a bar plot
        pivottable2.plot.bar(figsize=(15,5), rot=0)
        plt.title('Hourly Usage')
        plt.ylabel('Usage (kwh)')
        plt.xlabel('Time (hour)')
        plt.gca().legend(power_df['ReadingTime'].dt.day.unique(),title="Day (date)", loc='center left', bbox_to_anchor=(1, 0.5)) # Positioning legend next to the plot rather than within it
        plt.grid()
        plt.tight_layout() # Prevents content to exceed window
        plt.show()

    elif userinput == '6':
        
        plt.figure(figsize=(15,5))

        # Groups the readingtimes on the day value
        power_df_grouped = power_df.groupby(power_df['ReadingTime'].dt.day)

        # Loops throug all the KW(h) values that is in the group created above
        # and plots each one of them in their respective bars (https://stackoverflow.com/questions/27405483/how-to-loop-over-grouped-pandas-dataframe/27422749)
        for key, day in power_df_grouped:
            plt.plot(power_df['ReadingTime'].dt.hour.unique(), day['KW(h)'], '-o', label = str(key))

        # Sets annotation on each point in the plot which displays KW(h) for the given point (https://queirozf.com/entries/add-labels-and-text-to-matplotlib-plots-annotation-examples)
        for x, y in zip(power_df['ReadingTime'].dt.hour, power_df['KW(h)']):
            plt.annotate(y, (x,y), textcoords="offset points", xytext=(0,15), ha='center') 
 
        plt.title('Power Usage')
        plt.ylabel('Cumulative Usage (kwh)')
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.legend()
        plt.grid()
        plt.gca().set_ylim(power_df['KW(h)'].iloc[0]*0.9995,power_df['KW(h)'].iloc[-1]*1.0005) # Limits the y-axis to avoid annotations to exceed plot frame
        plt.gca().legend(title="Day (date)", loc='center left', bbox_to_anchor=(1, 0.5)) # Positioning legend next to the plot rather than within it
        plt.tight_layout() # Prevents content to exceed window
        plt.show()
    
    else:
        print('Invalid option, try again')

    # Prompts user to insert a new value of wanted action
    userinput = input(choices)

print('\nPROGRAM ENDED\n')

# References:
#
# Prac02 - Task 3 (For user interaction)
# https://stackoverflow.com/questions/27405483/how-to-loop-over-grouped-pandas-dataframe/27422749 
# https://queirozf.com/entries/add-labels-and-text-to-matplotlib-plots-annotation-examples 