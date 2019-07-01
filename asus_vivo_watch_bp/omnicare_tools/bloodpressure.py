#!usr/bin/python
#coding=utf-8
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Blood_pressure():
    
    #1
    def __init__(self, csv_file):
        # read blood pressure csv file 
        self.df = pd.read_csv(csv_file)
    
    #2
    def showhead(self, rows):
        # show rows of dataframe    
        df = self.df.head(rows)
        print (df)
    
    #3
    def preprocess_lineplot(self,name):
        '''
        1. select the columns of interest
        2. eliminate rows when value = -1
        3. adjust 'time' (hours only)
        4. save clean dataframe to csv file with customized name (name)     
        '''
        self.name = name # customized name
        df = self.df[['hr','time','sys','dia']] # select specific columns
        df = df[df.sys != -1] # remove rows by specific value
        
        def time_delete_year(t):
            (y,hm) = t.split() # split year and hour:minute:second
            result = hm # return only hour:minute:second
            return result
        
        def time_delete_minute(t):
            (h,m,s) = t.split(':') # split data by colon ':'
            result = int(h) # return only hour
            return result
        
        df['time'] = df['time'].apply(time_delete_year).apply(time_delete_minute) # adjust time to hour
        df.to_csv('bp_hr/clean/%s_clean.csv'%(name)) # save csv file
        
        clean_csv = pd.read_csv('bp_hr/clean/%s_clean.csv'%(name))
        
        
        #Draw a lineplot: x-axis = hour; y-axis = bp and hr(average sys and dia)
        def lineplot(clean_csv):
            df = clean_csv
            time = df.groupby('time')
            #print(type(time)) # check the data type 
            #print(time.size()) # to know how large is the data in each column
            #print(time.groups) # to know the details of each column and data
            #print(time.get_group(12)) # get specific group e.g.12,

            table = time.mean() #calculate the mean of each time group
            #print(table['hr']) #you can print a single column
            
            plt.title("24 Hours Blood Pressure Plot")
            plt.plot(table['sys'], label='systolic bp')
            plt.plot(table['dia'], label='diastolic bp')
            plt.plot(table['hr'], label='heart rate')
            plt.legend(loc='lower right')
            plt.xlabel('Time(hour)')
            plt.ylabel('mmHg, heart rate/min')
            plt.xticks(np.linspace(0,23,24))
            plt.savefig('bp_hr/fig/%s_bp_hr_lineplot'%(name))
            return
            
        lineplot(clean_csv) #use this function right away