import pandas as pd
import datetime

TIME_VALUE_STRING = 'time_value'
DATE_FORMAT_TS = '%Y-%m-%d %H:%M:%S.%f'


def process_datetime(dataframe_ts):
    dataframe_ts_processed = dataframe_ts.copy()
    dataframe_ts_processed[TIME_VALUE_STRING] = pd.to_datetime(dataframe_ts[TIME_VALUE_STRING], format=DATE_FORMAT_TS)
    dataframe_ts_processed.set_index(pd.DatetimeIndex(dataframe_ts_processed[TIME_VALUE_STRING]), inplace=True)
    return dataframe_ts_processed


def process_datetime_lessons(consolidate_dataframe_ts):
    for key_lesson in consolidate_dataframe_ts:
        consolidate_dataframe_ts[key_lesson] = process_datetime(consolidate_dataframe_ts[key_lesson])
    return consolidate_dataframe_ts


def process_activities(dataframe_ts):
    data_values = dataframe_ts.values
    zone_data = []
    previous_data = "-".join(data_values[0][10:])
    previous_datetime = data_values[0][2]
    i = 1
    while True:
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


def get_most_long_time_series(dataframes_ts_lessons):
    sizes_time_series = {}
    for key_lesson in dataframes_ts_lessons:
        data_ts_len = len(dataframes_ts_lessons[key_lesson])
        sizes_time_series[key_lesson] = data_ts_len
    return max(sizes_time_series, key=sizes_time_series.get)


def get_participant_lessons_activity(participant_lessons_data_ts, activity='VL'):
    dict_lessons_activity = {}
    for key_lesson in participant_lessons_data_ts.keys():
        tmp_array_lesson = []
        df_ts_filter = participant_lessons_data_ts[key_lesson]
        activities = process_activities(df_ts_filter)
        activity_filter_tmp = [activity_info for activity_info in activities if activity_info[0].startswith(activity)]
        for activity_filter in activity_filter_tmp:
            start_date = datetime.datetime.strptime(activity_filter[1], DATE_FORMAT_TS)
            end_date = datetime.datetime.strptime(activity_filter[2], DATE_FORMAT_TS)
            mask = (df_ts_filter['time_value'] > start_date.strftime(DATE_FORMAT_TS)) & \
                   (df_ts_filter['time_value'] <= (end_date - datetime.timedelta(seconds=1)).strftime(DATE_FORMAT_TS))
            filter_data_ts = df_ts_filter.loc[mask]
            tmp_array_lesson.append(filter_data_ts)
        if tmp_array_lesson:
            dict_lessons_activity[key_lesson] = tmp_array_lesson
    return dict_lessons_activity


def process_datetime_lessons_activity(participant_lessons_data_ts):
    dict_lessons_activity = {}
    for key_lesson in participant_lessons_data_ts.keys():
        array_tmp = []
        activities_values = participant_lessons_data_ts[key_lesson]
        for activity_value in activities_values:
            array_tmp.append(process_datetime(activity_value))
        dict_lessons_activity[key_lesson] = array_tmp
    return dict_lessons_activity


def generate_datetime_range(start_date, steps):
    return pd.date_range(start=start_date, periods=steps, freq='1S')


def reset_datetime_index_lessons_activity(participant_activity_lessons_data_ts):
    start_date = datetime.datetime.now()
    dict_lessons_activity = {}
    for key_lesson in participant_activity_lessons_data_ts.keys():
        array_tmp = []
        activities_values = participant_activity_lessons_data_ts[key_lesson]
        for activity_value in activities_values:
            steps_df = len(activity_value)
            new_range_datetime = generate_datetime_range(start_date, steps_df)
            array_tmp.append(activity_value.set_index(new_range_datetime))
        dict_lessons_activity[key_lesson] = array_tmp
    return dict_lessons_activity


def filter_participant_lesson_time_result(dict_participant_results_time, activity_info):
    filter_dict_lesson = {}
    for key_lesson in dict_participant_results_time.keys():
        list_keys_tmp = dict_participant_results_time[key_lesson].keys()
        filter_keys = [key for key in list_keys_tmp if activity_info in key]
        acum_time = 0
        if filter_keys:
            for filter_key in filter_keys:
                acum_time += dict_participant_results_time[key_lesson][filter_key]['time']
            filter_dict_lesson[key_lesson] = acum_time
    return filter_dict_lesson


def filter_participant_lesson_results(dict_participant_results_time, activity_info):
    filter_dict_lesson = {}
    for key_lesson in dict_participant_results_time.keys():
        list_keys_tmp = dict_participant_results_time[key_lesson].keys()
        filter_keys = [key for key in list_keys_tmp if activity_info in key]
        correct_acumulate = 0
        incorrect_acumulate = 0
        total_acumulate = 0
        attemps_acumulate = 0
        if filter_keys:
            for filter_key in filter_keys:
                correct_acumulate += dict_participant_results_time[key_lesson][filter_key]['results']['correct']
                incorrect_acumulate += dict_participant_results_time[key_lesson][filter_key]['results']['incorrect']
                total_acumulate += dict_participant_results_time[key_lesson][filter_key]['results']['total_questions']
                attemps_acumulate += dict_participant_results_time[key_lesson][filter_key]['results']['errors']
            tmp_dict_results = {
                'total_questions': total_acumulate,
                'correct': correct_acumulate,
                'incorrect': incorrect_acumulate,
                'errors': attemps_acumulate,
            }
            filter_dict_lesson[key_lesson] = tmp_dict_results
    return filter_dict_lesson


