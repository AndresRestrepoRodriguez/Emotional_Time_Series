import pandas as pd


def process_datetime(dataframe_ts):
    dataframe_ts_processed = dataframe_ts.copy()
    dataframe_ts_processed["time_value"] = pd.to_datetime(dataframe_ts['time_value'], format='%Y-%m-%d %H:%M:%S.%f')
    dataframe_ts_processed.set_index(pd.DatetimeIndex(dataframe_ts_processed['time_value']), inplace=True)
    return dataframe_ts_processed

    
def process_activities(dataframe_ts):
    data_values = dataframe_ts.values
    datos_zonas = []
    value_anterior = "-".join(data_values[0][10:])
    fecha_anterior = data_values[0][2]
    i = 1
    while(True):
        if value_anterior == "-".join(data_values[i][10:]):
            i += 1
        else:
            data_temp = [value_anterior, fecha_anterior, data_values[i][2]]
            datos_zonas.append(data_temp)
            value_anterior = "-".join(data_values[i][10:])
            fecha_anterior = data_values[i][2]
            i += 1
        
        if i == len(data_values)-1:
            data_temp = ["-".join(data_values[i][10:]), fecha_anterior, data_values[i][2]]
            datos_zonas.append(data_temp)
            break
    return datos_zonas


def get_unique_activities(data_activities):
    unique_actitivities = [act[0] for act in data_activities]
    return unique_actitivities
    

#path_data = "G:\\Maestria\\Tesis\\datos\\records\\id_2\\lesson_1\\data_1secs_extra_exe.csv"

#data = pd.read_csv(path_data)


#data_ts = process_datetime(data)
#activities = process_activities(data)
#unique_act = get_unique_activities(activities)


