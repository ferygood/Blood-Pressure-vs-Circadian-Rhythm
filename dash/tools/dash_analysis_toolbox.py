# !usr/bin/python
# coding=utf-8

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pandas as pd
import numpy as np

# write a function to separate the time data "HH:MM", we just want the hour  
def timechange(t):
    (h,m) = t.split(':')
    result = int(h)
    return result

def heatmap():
	# 這個函式是用 Heatmap 來展示每個 ID 睡覺時間的分布
	# step 1 
    x = input("enter your csv file name(.csv not required): ")
    title = input("enter your heatmap figure title: ")
    file_name = input("enter your save file name: ")

    df = pd.read_csv(x+'.csv')
    df = df[['ID_REL', 'SLEEPFRO', 'SLEEPTO']].drop_duplicates()
    id_list = list(df['ID_REL']) # create id_list

    # change the index
    index = []
    [index.append(i) for i in range(172)]
    df['index'] = index
    df = df.set_index('index')

    # make a new empty dataframe, and input vlaue, but first make a numpy array
    np_empty = np.zeros((172,49))

    # use the numpy array from previous step, df_empty = pd.DataFrame()
    df_empty = pd.DataFrame(np_empty)

    # set column's name 
    empty_dict={}
    [empty_dict.update({i:i}) for i in range(49)]
    df_empty.rename(columns = empty_dict)
    df_new = df_empty.rename(columns = {0:'ID'})
    df_new['ID'] = id_list

    for i in range(len(df['SLEEPFRO'])):
        df_new[df['SLEEPFRO'][i]][i] += 1
        df_new[df['SLEEPTO'][i]][i] += 1
        
    # step 6. fill in the gap with 1


    # a 為睡眠起始，b 為睡眠完成
    '''
    1. 每一個 row 裡面，遇到第一個時間另為 a；第二個時間另為 b
    2. 得到 a,b 之後，在 range (a+1,b) 裡面都放 1
    3. 重新進行一個 loop
    '''

    for i in range(len(df_new['ID'])):
        t = []
        for j in range(1,49):
            if df_new[j][i] == 1:
                t.append(j)
        a = t[0] ; b = t[1]
        for x in range(a+1, b):
            df_new[x][i] += 1
    
    # step 7
    testlist = []
    for i in range(1,49):
        testlist.append(i)

    df_test = df_new[testlist]
    sns.set(font_scale=0.4)
    
    new_x_tick = str([[x for x in range(1,25)] + [x for x in range(1,25)]])
    ax = sns.heatmap(df_test,cmap='BuPu',cbar=False, 
                     linewidths = 0.001,linecolor='gray',
                     yticklabels=False).set_title(title)
    ax.set_xticks(new_x_tick)

    plt.savefig(file_name, dpi=400)
    return

def select_id(csv_file,start_sleep,end_sleep):
    '''
    select id for specific time range
    篩選出特定時間睡眠範圍內的 ID
    並將這些 ID 輸出成一個 list
    '''
    df = pd.read_csv(csv_file)
    df_id_time = df[['ID_REL','SLEEPFRO','SLEEPTO']].drop_duplicates()
    df_id_time = df_id_time.reset_index(drop=True)

    length = len(df_id_time['ID_REL'])
    id_list = []
    for i in range(length):
        if df_id_time['SLEEPFRO'][i] >= start_sleep and df_id_time['SLEEPTO'][i] <= end_sleep:
            id_list.append(df_id_time['ID_REL'][i])

    final_id_list = []
    for i in id_list:
        if i not in final_id_list:
            final_id_list.append(i)

    return final_id_list

def unusual_sleep_lineplot(csv_file, final_id_list, name, start, end):
    '''
    將睡眠不正常的ID畫成線性圖
    csv_file = 輸入的 csv 檔案
    id_list = 睡眠不正常的 id list
    name 檔名
    start 睡眠開始時間
    end 睡眠停止時間
    '''
    df = pd.read_csv(csv_file)
    df = df[["ID_REL", "SBP", "DBP", "TIME"]]
    select_row = []
    for i in final_id_list:
        select_row.append(df[df.ID_REL==i])
    
    df_trim = pd.concat(select_row)
    
    # draw line plot
    df_line = pd.melt(df_trim, id_vars=['ID_REL','TIME'])
    df_line.rename(columns={'TIME':'TIME(o\'clock)', 'variable':'BP','value':'mmHg'}, inplace=True)
    sns.set_style('darkgrid')
    sns.set(font_scale=0.8)
    ax = sns.lineplot(x='TIME(o\'clock)',y='mmHg', hue='BP', data=df_line, markers=True).set_title('%s_lineplot'%(name))
    plt.savefig('%s_unusualsleep_%d_%d.png'%(name,start,end), dpi=480)
    plt.clf() #clear the figure, avoid overwritten when running multiple figures
    return


def add_24(df):
    '''
    這個 function 是用來將睡眠或睡醒時間 +24，以及量測時間如果已經過夜先 + 24
    '''
    df.reset_index(inplace=True, drop=True)
    for i in range(len(df['SLEEPFRO'])):
        if df['SLEEPFRO'][i] == 0:
            df['SLEEPFRO'][i]+=24
        elif df['SLEEPTO'][i] ==0:
            df['SLEEPTO'][i]+=24
    
    for i in range(len(df['SLEEPFRO'])):
        if df['SLEEPTO'][i] < df['SLEEPFRO'][i]:
            df['SLEEPTO'][i] += 24 
        
    for i in range(1,len(df['TIME'])):
        if df['ID_REL'][i] == df['ID_REL'][i-1]:
            if df['TIME'][i] < df['TIME'][i-1]:
                df['TIME'][i] += 24
    
    # for 夜貓子，隔天才睡覺會被漏加
    for i in range(len(df['SLEEPFRO'])):
        if df['SLEEPFRO'][i] < 12:
            df['SLEEPFRO'][i] += 24
            df['SLEEPTO'][i] += 24
    
    return

def sleep_awake(df):
    '''
    將 TIME 和 SLEEPFRO, SLEEPTO 比較
    如果是在睡覺期間標記為 sleep
    如果是睡醒時間標記為 awake
    '''
    status_list = []
    for i in range(len(df['TIME'])):
        if df['TIME'][i] >= df['SLEEPFRO'][i] and df['TIME'][i] < df['SLEEPTO'][i]:
            status_list.append('sleep')
        elif df['TIME'][i] < df['SLEEPFRO'][i] or df['TIME'][i] >= df['SLEEPTO'][i]:
            status_list.append('awake')
    df['sleep_awake'] = status_list
    return

def mean_bp_rate(df):
    '''
    計算睡眠和睡醒時間的平均血壓和心律，並組成新的資料框
    '''
    id_index = df['ID_REL'].drop_duplicates().index
    df_unique = df.iloc[id_index]
    df_unique = df_unique[['ID_REL','DIET','SODIUM','SLEEP_CY',
                       'SLEEPFRO','SLEEPTO']]
    df_unique.reset_index(inplace=True, drop=True) # 把 index 重置
    #計算 mean
    id_list = df['ID_REL'].drop_duplicates()
    mean_sleep_sbp = []
    mean_awake_sbp = []
    mean_sleep_dbp = []
    mean_awake_dbp = []
    mean_sleep_rate = []
    mean_awake_rate = []
    
    for id in id_list:
        each_id_df = df[df['ID_REL']==id]
        each_id_df.reset_index(inplace=True, drop=True)
        sleep_index = each_id_df[each_id_df['sleep_awake']=='sleep'].index
        mean_sleep_sbp.append(each_id_df['SBP'].iloc[sleep_index].mean())
        mean_sleep_dbp.append(each_id_df['DBP'].iloc[sleep_index].mean())
        mean_sleep_rate.append(each_id_df['RATE'].iloc[sleep_index].mean())
        
        awake_index = each_id_df[each_id_df['sleep_awake']=='awake'].index
        mean_awake_sbp.append(each_id_df['SBP'].iloc[awake_index].mean())
        mean_awake_dbp.append(each_id_df['DBP'].iloc[awake_index].mean())
        mean_awake_rate.append(each_id_df['RATE'].iloc[awake_index].mean())
        
    mean_result_df = pd.DataFrame({'ID_REL':id_list, 'mean_sleep_sbp':mean_sleep_sbp,'mean_sleep_dbp':mean_sleep_dbp,
                                   'mean_sleep_rate':mean_sleep_rate, 'mean_awake_sbp':mean_awake_sbp, 
                                   'mean_awake_dbp':mean_awake_dbp,'mean_awake_rate':mean_awake_rate})
    
    return pd.merge(df_unique, mean_result_df, on='ID_REL')