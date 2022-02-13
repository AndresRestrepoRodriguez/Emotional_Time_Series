import numpy as np


def generate_data_time_activity(json_data):
    array_data = []
    for key in json_data.keys():
        time_value = json_data[key]['time']
        array_data.append([key, time_value])
    return array_data


def generate_data_time_activity_bar(json_data):
    dict_values = {}
    x_values = []
    y_values = []
    for key in json_data.keys():
        if not key == "0-general":
            time_value = json_data[key]['time']
            x_values.append(key)
            y_values.append(time_value)
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    return dict_values


def generate_data_result_activity(json_data):
    array_data = []
    key_results = 'results'
    for key in json_data.keys():
        filter_data = json_data[key]
        if key_results in filter_data:
            results = list(filter_data[key_results].values())
            temp_data = [key] + results
            array_data.append(temp_data)
    return array_data


def generate_data_result_general(data_results_activities):
    dict_values = {}
    name_activity = data_results_activities[0][0]
    x_values = ["Correct", "Incorrect", "Errors / Attempts"]
    y_values = data_results_activities[0][2:]
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    dict_values['name_activity'] = name_activity
    return dict_values


def generate_data_results_activity_bar_grouped(data_results_activities):
    dict_values = {}
    x_values = []
    y_values = []
    name_values = ["Correct", "Incorrect", "Errors / Attempts"]
    for value in data_results_activities[1:]:
        x_values.append(value[0])
        y_values.append(value[2:])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.array(y_values).T.tolist()
    dict_values['name_values'] = name_values
    return dict_values


def get_general_time_lessons(data_json_consolidate):
    time_general_lessons = []
    for key_lesson in data_json_consolidate:
        lesson_time_general_tmp = [key_lesson, data_json_consolidate[key_lesson]['0-general']['time']]
        time_general_lessons.append(lesson_time_general_tmp)
    return time_general_lessons


def get_general_results_lessons(data_json_consolidate):
    array_data = []
    key_results = 'results'
    for key_lesson in data_json_consolidate.keys():
        filter_data = data_json_consolidate[key_lesson]['0-general']
        print(filter_data)
        results = list(filter_data[key_results].values())
        temp_data = [key_lesson] + results
        array_data.append(temp_data)
    return array_data


def generate_data_results_general_lesson_pie(data_general_results_lessons):
    dict_values = {}
    y_values_tmp = []
    x_values = ["Correct", "Incorrect", "Errors / Attempts"]
    for lesson in data_general_results_lessons:
        y_values_tmp.append(lesson[2:])
    print(y_values_tmp)
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.sum(y_values_tmp, axis=0)
    return dict_values


def generate_data_results_lessons_bar_grouped(data_results_lessons):
    dict_values = {}
    x_values = []
    y_values = []
    name_values = ["Correct", "Incorrect", "Errors / Attempts"]
    for value in data_results_lessons:
        x_values.append(value[0])
        y_values.append(value[2:])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.array(y_values).T.tolist()
    dict_values['name_values'] = name_values
    return dict_values


def generate_data_time_lessons_bar_pie(time_lesson_processed):
    dict_values = {}
    x_values = []
    y_values = []
    for lesson in time_lesson_processed:
        x_values.append(lesson[0])
        y_values.append(lesson[1])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    return dict_values


def get_metric_all_lessons(df_consolidate_time_series, metric):
    array_metrics_data = []
    for lesson in df_consolidate_time_series:
        array_metrics_data.append(df_consolidate_time_series[lesson][metric])
    return np.concatenate(array_metrics_data).tolist()


def get_metric_all_lessons_consolidate(df_consolidate_time_series, metrics):
    metric_lessons_unified = {}
    for metric in metrics:
        metric_lessons_unified[metric] = get_metric_all_lessons(df_consolidate_time_series, metric)
    return metric_lessons_unified


