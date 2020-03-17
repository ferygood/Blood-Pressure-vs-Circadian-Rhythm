# -*- coding: utf-8 -*-
"""
Analysis of ASUS Vivo Watch BP
Create a asus_bp object and analysis the status and blood pressure data
Author: Yao-Chung Chen
Date: 17. 03. 2020 
"""
import pandas as pd
import os

os.chdir("C:/Users/Yao-Chung Chen/OneDrive/NYMU_biomed_lab/asus_vivo_watch/")

class asus_bp:
    
    def __init__(self):
        pass
    
    def status(self, file, sheet):
        """this function take a user's status excel file as input.
        :file: is the file/path include file name. There are two columns, the 
        first column is timestamp (YYYY-MM-DD hr:min:sec) and the second is 
        status (include 起床，睡前)
        :sheet: is the name of sheet in excel, e.g. 89
        """
        df = pd.read_excel(file, sheet_name = sheet, parse_dates=["timestamp"])
        
        # select the timestamp when it is 起床 or 睡前
        df = df.loc[df["status"].isin(["起床", "睡前"])]
        df = df.reset_index(drop = True)
    
        
        # create a time table, we want to display a dataframe include sleep and
        # awake time everyday, df_time
        sleep = []
        awake = []
        for index_num in range(len(df["timestamp"])):
            if index_num % 2== 0:
                sleep.append(df["timestamp"][index_num])
            else:
                awake.append(df["timestamp"][index_num])
        
        df_time = pd.DataFrame(list(zip(sleep, awake)), 
                               columns = ["sleep", "awake"])
        return df_time
    
    def bp_data(self, file):
        """This function will take in a blood pressure file from OmniCare Hub,
        then drop rows with no data, add new columns, pp(pulse pressure), 
        mean_bp, and set index as time value after to output a dataframe 
        after these process.
        :file: a blood pressure csv file download from OmniCare Hub
        """
        # read csv, set time column as pandas timestamp
        df = pd.read_csv(file, parse_dates=["time"]) 
        
        df = df[["hr","time","sys","dia"]] 
        
        # select the rows which systolic blood pressure is not -1 
        df = df[df.sys != -1]    
        
        df["pp"] = df["sys"] - df["dia"] 
        df["mean_bp"] = (df["sys"]*2 + df["dia"])/3
        
        # Here, we will set status as awake temporary, later we will change
        # the rows with sleep
        df["status"] = "awake" 
        
        df = df.set_index(["time"]) 
        
        return df
    
    def pattern(self, df_status, df_bp, month, merge_file = None, 
                save_file="pattern_analysis"):
        """#1 This function indicate status to sleep when the participant is 
        sleeping
        #2 Month is the time period when you conduct this experiment
        #3 Outputs have two files, including a dataframe of that month, and a 
        concat dataframe, therefore, it is recommend to have two output 
        variables
        #4 the concat dataframe will be save as a csv file in the current 
        directory by default (pattern_analysis.csv),but you can also specify 
        the file name and path in the save_file variables
        :df_status: output result from asus_bp.().status()
        :df_bp: output result from asus_bp.().bp_data()
        :month: is a string for labeling column, can be "oct", "nov"
        :merge_file: if you want to merge with exist files, please specify, 
        default is None
        :save_file: you can rename the name of the file, default is 
        pattern_analysis.csv
        """
        # Indicate the row range in df_bp, set the range when the participant
        # is sleeping, and change the value of status from awake to sleep
        for sleep, awake in zip(df_status["sleep"], df_status["awake"]):
            df_bp["status"][sleep:awake] = "sleep"
    
    
        # Calculate the mean (awake vs. sleep) value and save as a dataframe
        health_data = []
        for i, j in zip(df_bp[df_bp["status"] == "awake"].mean(), 
                        df_bp[df_bp["status"] == "sleep"].mean()):
            health_data.extend((i,j))
    
        health_data_df = pd.DataFrame(
                health_data, columns=[str(month)], 
                index = ["hr_sleep", "hr_awake", "sys_sleep", "sys_awake",
                         "dia_sleep","dia_awake", "pp_sleep", "pp_awake",
                         "mean_bp_sleep","mean_bp_awake"])
    
        # We want to concat the result dataframe when we have a new month data
        df_merge = pd.DataFrame()
        if merge_file == None:
            pass
        else:
            df_merge = pd.read_csv(merge_file, index_col=0)
    
        df_merge = pd.concat([df_merge, health_data_df], axis=1)
        df_merge.to_csv(save_file + ".csv")
        return health_data_df, df_merge
    

if __name__ == "__main__":
    # address an example use here
    df_status = asus_bp().status(file = "user_status_Oct19_Feb20.xlsx", sheet = "89")
    df_bp = asus_bp().bp_data("89/ASUSLife-vivowatchbp-NYMU-01_2019-Dec.csv")
    oct_df, df_merge = asus_bp.pattern(df_status, df_bp, month = "oct")
    