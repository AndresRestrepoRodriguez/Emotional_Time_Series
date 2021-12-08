import pandas as pd


def process_datetime(dataframe_ts):
    dataframe_ts_processed = dataframe_ts.copy()
    dataframe_ts_processed["time_value"] = pd.to_datetime(dataframe_ts['time_value'], format='%Y-%m-%d %H:%M:%S.%f')
    dataframe_ts_processed.set_index(pd.DatetimeIndex(dataframe_ts_processed['time_value']), inplace=True)
    return dataframe_ts_processed

    
def process_activities(dataframe_ts):
    data_values = dataframe_ts.values
    zone_data = []
    previous_data = "-".join(data_values[0][10:])
    previous_datetime = data_values[0][2]
    i = 1
    while(True):
        if previous_data == "-".join(data_values[i][10:]):
            i += 1
        else:
            data_temp = [previous_data, previous_datetime, data_values[i][2]]
            zone_data.append(data_temp)
            previous_data = "-".join(data_values[i][10:])
            previous_datetime = data_values[i][2]
            i += 1
        
        if i == len(data_values)-1:
            data_temp = ["-".join(data_values[i][10:]), previous_datetime, data_values[i][2]]
            zone_data.append(data_temp)
            break
    return zone_data


def get_unique_activities(data_activities):
    unique_activities = [activity[0] for activity in data_activities]
    return unique_activities
