#!usr/bin/python
#coding=utf-8

#this script is an example of preprocess 03_bp_df.csv using self-write function: omnicare_tools
import omnicare_tools.bloodpressure as ob
df = ob.Blood_pressure('bp_hr/raw/03_bp_df_new.csv') #make the bp_csv file as a Blood_pressure object
#df.showhead(15) #show the first 15 line of csv file
df.preprocess('03_bp_new') #save preprocess csv file and draw lineplot
df.lineplot(saveFile=True)
df.errorbar(saveFile=True)