import pandas as pd
import re


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
    while (True):
        if previous_data == "-".join(data_values[i][10:]):
            i += 1
        else:
            data_temp = [previous_data, previous_datetime, data_values[i][2]]
            zone_data.append(data_temp)
            previous_data = "-".join(data_values[i][10:])
            previous_datetime = data_values[i][2]
            i += 1

        if i == len(data_values) - 1:
            data_temp = ["-".join(data_values[i][10:]), previous_datetime, data_values[i][2]]
            zone_data.append(data_temp)
            break
    return zone_data


def get_unique_activities(data_activities):
    unique_activities = [activity[0] for activity in data_activities]
    return unique_activities


def get_time_diff_activities(activities_info):
    count_activity = 0
    time_data_activities = []
    initial_time = activities_info[0][1]
    final_time = activities_info[-1][-1]
    general_time = (final_time - initial_time).total_seconds()
    time_data_activities.append([count_activity, "general", general_time])
    for activity in activities_info:
        count_activity += 1
        activity_name = activity[0]
        initial_time_activity = activity[1]
        final_time_activity = activity[-1]
        diff_time_activity = (final_time_activity - initial_time_activity).total_seconds()
        time_data_activities.append([count_activity, activity_name, diff_time_activity])

    return time_data_activities


def generate_results_time(time_activities, dataframe_results):
    dict_results_time = dict()
    for activity in time_activities:
        isolated_name_act = activity[1].strip()
        seq_activity = str(activity[0])
        name_activity = seq_activity + "-" + isolated_name_act
        diff_time = activity[-1]
        filter_df = dataframe_results.query("activity == @isolated_name_act & sequence == @seq_activity")
        if not filter_df.empty:
            total_questions = filter_df['total_questions'].values[0]
            correct = filter_df['correct'].values[0]
            incorrect = filter_df['incorrect'].values[0]
            errors = filter_df['errors'].values[0]
            dict_results_time[name_activity] = {'time': diff_time,
                                                'results': {
                                                    'total_questions': total_questions,
                                                    'correct': correct,
                                                    'incorrect': incorrect,
                                                    'errors': errors
                                                }}
        else:
            dict_results_time[name_activity] = {'time': diff_time}
    return dict_results_time
