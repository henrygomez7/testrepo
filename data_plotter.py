import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Update to the location of the data you want to plot.
directory = r'C:\Users\GOMEHEN01\Documents\Rotation_3\Nick\Vine\Analysis_Tools\data\JAN_31_2022_ALL'

for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
        #Update to the location of the data you want to plot.
        csv_directory = directory + "\\" + filename 
        df = pd.read_csv(csv_directory) 
        df.head()
        df = df.set_index(pd.to_datetime(df['datetime']))
        
        well_name = filename.split('.csv')[0] #Update to the well name you are plotting. 
        pt= '1/24/2022' #Update to the beginning date you want to analyze.
        pt_end = '1/31/2022' #Update to the end date you want to analyze. (must be identical to 'month' on  forecast csv to work)

        df['DeltaP'] = df['tubing_pressure']-df['line_pressure']
        df['well_name'].unique()
        
        days = mdates.DayLocator()
        days_fmt = mdates.DateFormatter('%D')
        
        fig, ax = plt.subplots(figsize=(12,6), dpi=120)

        ax.plot(df['flow_rate'][pt:pt_end], color='r', alpha=0.9, label='Rate')
        ax.plot(df['min_flow_rate'][pt:pt_end], color='tomato', linestyle='--', alpha=1, label='Min Rate')
        ax.set_xlabel('Date')
        ax.set_ylabel('Flow Rate [Mscf]')
        
        if (df['DeltaP'][pt:pt_end]).empty == True:
            continue
        
        ax2=ax.twinx() #make a plot with different y-axis using second axis object
        ax2.plot(df['DeltaP'][pt:pt_end], color='b', alpha=0.65, label='Delta Pres')
        ax2.plot(df['max_differential_pressure'][pt:pt_end], color='lightblue', linestyle='--', alpha=1, label='Set Delta Pres')
        #ax2.plot(df['tubing_pressure'][pt:pt_end], color='b', linestyle='--', label='Tubing Pres')
        #ax2.plot(df['line_pressure'][pt:pt_end], color='r', linestyle='--', label='Line Pres')
        ax2.set_ylabel("Pressure [psi]")

        #ax3.plot(df['shut_in_request'][pt:pt_end], linestyle='--', alpha=0.6, color='k')
        ax.set_title(well_name)
        ax.xaxis.set_major_formatter(days_fmt)
        fig.autofmt_xdate()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.margins(x=0.005)
        fig.legend(bbox_to_anchor=(0.975, 0.95), loc='upper left')
        
        #Aligns zeros for both y-axis'
        ax_ylims = ax.axes.get_ylim()           # Find y-axis limits set by the plotter
        ax_yratio = ax_ylims[0] / ax_ylims[1]  # Calculate ratio of lowest limit to highest limit
        ax2_ylims = ax2.axes.get_ylim()           # Find y-axis limits set by the plotter
        ax2_yratio = ax2_ylims[0] / ax2_ylims[1]  # Calculate ratio of lowest limit to highest limit
        if ax_yratio < ax2_yratio: 
            ax2.set_ylim(bottom = ax2_ylims[1]*ax_yratio)
        else:
            ax.set_ylim(bottom = ax_ylims[1]*ax2_yratio)
            
        #Save figures
        plt.tight_layout()
        plt.savefig(well_name+'_jan_24_31', bbox_inches = 'tight') #no backslash are allowed