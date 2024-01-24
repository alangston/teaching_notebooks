# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 20:05:58 2021

@author: abby
"""
from IPython import get_ipython
_ipython = get_ipython()
_ipython.run_line_magic("reset","-f")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def import_stuff2_mat(file_name):
    return_df = pd.read_csv(file_name+".csv", parse_dates=['datetime'], index_col=['datetime'])
    return_df["discharge"] = return_df["discharge"] /35.315
    return_df["discharge"] = return_df["discharge"]

    return return_df

def import_stuff2(file_name):
    dataloc = "data/four_rivers/"

    return_df = pd.read_csv(dataloc + file_name+".csv", parse_dates=['datetime'], index_col=['datetime'])
    return_df = return_df.replace({'discharge':0}, 1e-2)    
    precip_df = pd.read_csv(dataloc + file_name+"_precip.csv")

    # return_df["discharge"] = return_df["discharge"] /35.315
    return_df["discharge"] = return_df["discharge"]

    return_df["precip"] = np.array(precip_df["DataValue"])
    return_df = return_df.replace({'precip':-9999}, 0)
    return return_df

#%%
dataloc = "data/four_rivers/"

# hood_river_or = import_stuff2(dataloc+"hood_river_or")

# sanpedro = import_stuff2(dataloc+"sanpedro")

# oleno = import_stuff2(dataloc+"oleno")

# matanuska = import_stuff2_mat(dataloc+"matanuska")

"""
Note, I made the river1,2,3, .csv files with something like this:
    rivers = ["oleano", "mthood", snpedro]
    for i,n in enumerate(rivers):
        datafram = importstuff2(n)
        datafram.to_csv
        
"""
savedataframe = 0

rivers = ["hood_river_or", "sanpedro", "oleno"]
for i, n in enumerate(rivers):
    print(n)
    datafram = import_stuff2(n)
    if savedataframe:
        ## save data frame created above
        dfname = "river"+str(i+1)+".csv"
        datafram.to_csv(dataloc + dfname)


datafram= import_stuff2_mat(dataloc+"matanuska")
if savedataframe:
    ## save data frame created above
    dfname = "river"+str(i+2)+".csv"
    datafram.to_csv(dataloc + dfname)
    print(frog)
#%%
"""
1. San Pedro
2. Mt. Hood
3. Oleno
4. Matanuska
"""

river1 = pd.read_csv(dataloc + "river1.csv", parse_dates=['datetime'], index_col=['datetime'])
river2 = pd.read_csv(dataloc + "river2.csv", parse_dates=['datetime'], index_col=['datetime'])
river3 = pd.read_csv(dataloc + "river3.csv", parse_dates=['datetime'], index_col=['datetime'])
river4 = pd.read_csv(dataloc + "river4.csv", parse_dates=['datetime'], index_col=['datetime'])

river2 = river2.truncate(before='2017-01-01', after='2018-12-30')
river3 = river3.truncate(before='2017-01-01', after='2018-12-30')
river4 = river4.truncate(before='2017-01-01', after='2018-12-30')


#%%
def plot_precip_discharge(df_name, temp_flag=None, label_str=None):
    fig, ax1 = plt.subplots(figsize=(10,5))
#    color = 'tab:blue'
    if temp_flag is not None:
        ax1.set_ylabel('water temperature' , fontsize=14)  # we already handled the x-label with ax1
        ax1.bar(df_name.index,df_name["temp"], width=3)
        ydata=np.array(df_name["temp"])
    else:
        ax1.set_ylabel('precip (mm/day)', fontsize=14 )  # we already handled the x-label with ax1
        ax1.bar(df_name.index,df_name["precip"], width=3, label="precip")
        ydata=np.array(df_name["precip"])
    ax1.invert_yaxis()
    if np.nanmax(ydata)<50.:
        ax1.set_ylim([np.nanmax(ydata)*2, 0])
    else:
        ax1.set_ylim([300, 0])
    ax1.tick_params(axis='y')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_xlabel('time')
    ax2.set_ylabel('discharge (m$^3$/s)', fontsize=14)
    ax2.plot(df_name.index, df_name["discharge"], linewidth=1.75, marker="*", color = "firebrick", label="discharge")
    ax2.set_yscale('log')
    ax2.set_ylim([1, 1000])
    ax2.set_xlim([df_name.index[0], df_name.index[-1]])
    ax2.tick_params(axis='y')
    plt.grid()
    plt.legend(loc=4)
    if label_str is not None:
        plt.title(label_str)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

plot_precip_discharge(river2, label_str="River 2")
plot_precip_discharge(river1, label_str="River 1")
plot_precip_discharge(river3, label_str="River 3")
plot_precip_discharge(river4, temp_flag=1, label_str="River 4")

