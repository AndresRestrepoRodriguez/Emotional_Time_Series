import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import re
sns.set()
sns.set_style("whitegrid")

def get_plot_ts(dataframe_ts, metrics_list, colors_metrics, zone_data, dict_colors, unique_actitivities):
    fig, ax = plt.subplots(figsize=(12, 7))
    for i in metrics_list:
                ax.plot(dataframe_ts.index.values,
                                dataframe_ts[i],
                                label=i,
                                color=colors_metrics.get(i))
    ax.set_title('Record Performance Metrics Participant Id. '+str(int(re.findall(r'\d+', dataframe_ts['user_id'].iloc[0])[0])+1)+' \nInteraction with lesson No. '+dataframe_ts['lesson'].iloc[0]+' - language: Portuguese\n', fontsize=16,fontweight='bold')
    ax.set_xlabel('Time', fontsize=14, fontweight='bold')
    ax.set_ylabel('Performance Metrics Values', fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%M:%S"))
    lines = ax.get_lines()
    zones = list()
    for i in zone_data:
        zones.append(ax.axvspan(i[1], i[2], facecolor=dict_colors.get(i[0]), alpha=0.45))
        legend1 = plt.legend([line for line in lines], metrics_list, bbox_to_anchor=(1, 1), loc='upper left',prop={'size': 13})
    legend1.set_title("Metrics",prop={'size': 13, 'weight':'bold'}) 
    by_label = dict(zip(unique_actitivities, zones))
    legend2 = plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1, 0.25), loc='lower left',prop={'size': 13})
    legend2.set_title("Activities",prop={'size': 13, 'weight':'bold'}) 
    ax.add_artist(legend1)
    ax.add_artist(legend2)
    plt.gca().add_artist(legend1)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.show()
